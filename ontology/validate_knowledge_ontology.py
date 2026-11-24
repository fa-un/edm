#!/usr/bin/env python3
"""Validate the source ontology and its publication dependencies.

This stdlib-only validator is shared by local checks and the Pages workflow.
It proves structural consistency and file/link coverage; it does not prove that
the source statements are semantically true (that remains an audited review).
"""

from __future__ import annotations

import argparse
from collections import Counter
from functools import lru_cache
from html.parser import HTMLParser
import json
from pathlib import Path, PurePosixPath
import re
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
ALLOWED_EVIDENCE = {"direct", "indirect", "not-established", "contradicted", "secondary-only"}
ALLOWED_METHOD_STATUSES = {
    "verified_against_primary_source",
    "secondary_source_only",
    "primary_source_unavailable",
    "mention_does_not_define_verifiable_method",
}
RELATION_TYPES = {
    "conditional", "references", "normative-basis", "comparison", "related-to",
    "hypothesis", "used-in", "computed-by",
}
COVERAGE_STATUSES = {
    "materialAvailability": {"available", "partial", "unavailable", "unknown"},
    "deliveryStatus": {"confirmed", "not_confirmed", "unknown"},
    "assessmentStatus": {"record_present", "record_absent", "unknown"},
}
AUDIT_REPORTS = {
    "ontology/source_audit/html-01-10.md",
    "ontology/source_audit/html-11-20.md",
    "ontology/source_audit/attachments.md",
}


def _path_key(value: str) -> str:
    """Normalize a local URL path into a repository-relative POSIX path."""
    path = unquote(urlsplit(value).path).replace("\\", "/")
    while path.startswith("./"):
        path = path[2:]
    return str(PurePosixPath(path)) if path else ""


def _local_path(reference: str, root: Path, base: str = "") -> tuple[Path, str] | None:
    """Return a local target and fragment, or None for external references."""
    parsed = urlsplit(reference)
    if parsed.scheme or parsed.netloc:
        return None
    path_part = unquote(parsed.path)
    if not path_part:
        path_part = base
    elif base and not path_part.startswith("/"):
        path_part = str(PurePosixPath(base).parent / path_part)
    return (root / path_part.lstrip("/"), unquote(parsed.fragment))


class HtmlIndex(HTMLParser):
    """Collect anchors, IDs, visible text, and local links by course topic."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.text: list[str] = []
        self.topic_links: dict[str, set[str]] = {f"topic-{i}": set() for i in range(1, 8)}
        self.attachments: set[str] = set()
        self._topic: str | None = None
        self._topic_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        element_id = values.get("id")
        if element_id:
            self.ids.add(element_id)
        if tag == "section" and element_id in self.topic_links and self._topic is None:
            self._topic = element_id
            self._topic_depth = 1
        elif tag == "section" and self._topic is not None:
            self._topic_depth += 1
        if tag == "a":
            href = values.get("href") or ""
            parsed = urlsplit(href)
            if parsed.scheme or parsed.netloc:
                return
            key = _path_key(href)
            if not key:
                return
            suffix = PurePosixPath(key).suffix.lower()
            if suffix in {".pdf", ".pptx"}:
                self.attachments.add(key)
            elif suffix in {".html", ".htm"} and self._topic:
                self.topic_links[self._topic].add(key)

    def handle_endtag(self, tag: str) -> None:
        if tag == "section" and self._topic is not None:
            self._topic_depth -= 1
            if self._topic_depth == 0:
                self._topic = None

    def handle_data(self, data: str) -> None:
        self.text.append(data)


@lru_cache(maxsize=512)
def _parse_html(path: Path) -> HtmlIndex | None:
    if not path.is_file() or path.suffix.lower() not in {".html", ".htm"}:
        return None
    parser = HtmlIndex()
    try:
        parser.feed(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError) as exc:
        raise ValueError(f"cannot read HTML {path}: {exc}") from exc
    return parser


def _ids(rows: list[dict], label: str, errors: list[str]) -> set[str]:
    values = [row.get("id") for row in rows]
    if any(not isinstance(value, str) or not value for value in values):
        errors.append(f"{label} must have non-empty string IDs")
    duplicates = sorted(value for value, count in Counter(values).items() if value and count > 1)
    if duplicates:
        errors.append(f"duplicate {label} IDs: {', '.join(duplicates)}")
    return {value for value in values if isinstance(value, str) and value}


def validate_ontology(
    data: dict | None = None,
    root: Path = ROOT,
    manifest_data: dict | None = None,
) -> list[str]:
    """Return all structural/publication errors found in an ontology tree."""
    errors: list[str] = []
    if data is None:
        try:
            data = json.loads((root / "ontology/knowledge_ontology.json").read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            return [f"cannot load ontology/knowledge_ontology.json: {exc}"]
    if not isinstance(data, dict):
        return ["ontology root must be a JSON object"]

    required_arrays = ("clusters", "terms", "sources", "sourceAssertions", "actions", "functions", "links", "elementLinks", "methodPractices", "coverage")
    for key in required_arrays:
        if not isinstance(data.get(key), list):
            errors.append(f"{key} must be a JSON array")
    if not isinstance(data.get("meta"), dict):
        errors.append("meta must be a JSON object")
        return errors
    if any(not isinstance(data.get(key), list) for key in required_arrays):
        return errors

    meta = data["meta"]
    clusters = data["clusters"]
    terms = data["terms"]
    sources = data["sources"]
    assertions = data["sourceAssertions"]
    actions = data["actions"]
    functions = data["functions"]
    links = data["links"]
    element_links = data["elementLinks"]
    methods = data["methodPractices"]
    coverage = data["coverage"]

    term_ids = _ids(terms, "term", errors)
    source_ids = _ids(sources, "source-record", errors)
    assertion_ids = _ids(assertions, "source-assertion", errors)
    action_ids = _ids(actions, "action", errors)
    function_ids = _ids(functions, "function", errors)
    for left, right, label in ((term_ids, source_ids, "term/source"), (term_ids, assertion_ids, "term/assertion"), (source_ids, assertion_ids, "source/assertion"), (action_ids, function_ids, "action/function")):
        if left & right:
            errors.append(f"ID namespaces {label} overlap: {', '.join(sorted(left & right))}")
    if len(clusters) != len({row.get("id") for row in clusters}):
        errors.append("cluster IDs must be unique")

    sources_by_id = {row.get("id"): row for row in sources if row.get("id")}
    assertions_by_id = {row.get("id"): row for row in assertions if row.get("id")}
    terms_by_id = {row.get("id"): row for row in terms if row.get("id")}
    actions_by_id = {row.get("id"): row for row in actions if row.get("id")}
    functions_by_id = {row.get("id"): row for row in functions if row.get("id")}

    for key, expected in (("distinctConceptNodes", len(terms)), ("sourceRecordCount", len(sources)), ("sourceAssertionCount", len(assertions)), ("methodPracticeCount", len(methods))):
        if meta.get(key) != expected:
            errors.append(f"meta.{key} is stale: expected {expected}, got {meta.get(key)!r}")
    active_count = sum(len(term.get("definitions", [])) for term in terms)
    explicit_count = sum(bool(definition.get("explicit")) for term in terms for definition in term.get("definitions", []))
    legacy_count = sum(len(term.get("legacyDefinitions", [])) for term in terms)
    if meta.get("sourceDefinitionEntries") != active_count:
        errors.append(f"meta.sourceDefinitionEntries is stale: expected {active_count}")
    if meta.get("explicitDefinitions") != explicit_count:
        errors.append(f"meta.explicitDefinitions is stale: expected {explicit_count}")
    if meta.get("legacyDefinitionEntries") != legacy_count:
        errors.append(f"meta.legacyDefinitionEntries is stale: expected {legacy_count}")

    allowed_evidence = set(meta.get("evidenceStatusVocabulary", [])) or ALLOWED_EVIDENCE
    if allowed_evidence != ALLOWED_EVIDENCE:
        errors.append("meta.evidenceStatusVocabulary does not match the supported evidence status vocabulary")
    relation_catalog = meta.get("relationTypes", [])
    relation_types = {row if isinstance(row, str) else row.get("id") for row in relation_catalog}
    if not relation_types or not relation_types <= RELATION_TYPES:
        errors.append("meta.relationTypes contains unsupported values or is empty")
    kinds = set(meta.get("kindVocabulary", []))
    if not kinds or "unclassified" not in kinds:
        errors.append("meta.kindVocabulary must include unclassified")
    levels = meta.get("entityLevelVocabulary", [])
    if set(levels) != {"class", "instance", "not-applicable", "unknown"}:
        errors.append("meta.entityLevelVocabulary has an invalid value set")
    if meta.get("entityLevels") != levels:
        errors.append("meta.entityLevels must exactly match meta.entityLevelVocabulary")
    if set(meta.get("methodPracticeVerificationStatuses", [])) != ALLOWED_METHOD_STATUSES:
        errors.append("meta.methodPracticeVerificationStatuses must contain exactly the four supported statuses")

    # Source records and all source-assertion fields are foreign-key checked.
    for source in sources:
        if not all(source.get(key) for key in ("uri", "kind")):
            errors.append(f"source {source.get('id')} is missing uri/kind")
    for assertion in assertions:
        if assertion.get("sourceId") not in source_ids:
            errors.append(f"source assertion {assertion.get('id')} has dangling sourceId")
        if assertion.get("claimType") not in {"definition", "action", "function", "relation", "method_practice", "coverage"}:
            errors.append(f"source assertion {assertion.get('id')} has invalid claimType")
        if assertion.get("evidenceStatus") not in allowed_evidence:
            errors.append(f"source assertion {assertion.get('id')} has invalid evidenceStatus")
        if not all(assertion.get(key) for key in ("claimText", "locator", "modality")):
            errors.append(f"source assertion {assertion.get('id')} is missing claimText/locator/modality")
        if assertion.get("publishable") and assertion.get("evidenceStatus") in {"not-established", "contradicted", "secondary-only"}:
            errors.append(f"source assertion {assertion.get('id')} is publishable despite non-confirming evidence")

    def require_assertion(assertion_id: str | None, claim_type: str, owner: str) -> dict | None:
        assertion = assertions_by_id.get(assertion_id)
        if not assertion:
            errors.append(f"{owner} references missing source assertion {assertion_id!r}")
        elif assertion.get("claimType") != claim_type:
            errors.append(f"{owner} references assertion of wrong type (expected {claim_type})")
        return assertion

    for term in terms:
        if term.get("cluster") not in {cluster.get("id") for cluster in clusters}:
            errors.append(f"term {term.get('id')} has unknown cluster")
        if term.get("kind") not in kinds:
            errors.append(f"term {term.get('id')} has invalid kind")
        if term.get("entityLevel") not in levels:
            errors.append(f"term {term.get('id')} has invalid entityLevel")
        if term.get("kind") == "unclassified" and not (term.get("kindRationale") or term.get("kindReason")):
            errors.append(f"unclassified term {term.get('id')} lacks rationale")
        if not term.get("entityLevelReason"):
            errors.append(f"term {term.get('id')} lacks entityLevelReason")
        topics = term.get("rpdTopics")
        if not isinstance(topics, list) or len(topics) != len(set(topics)) or any(type(topic) is not int or topic not in range(1, 8) for topic in topics):
            errors.append(f"term {term.get('id')} has invalid rpdTopics")
        term_assertions = set(term.get("sourceAssertionIds", []))
        for definition_field in ("definitions", "legacyDefinitions"):
            for definition in term.get(definition_field, []):
                aid = definition.get("sourceAssertionId") or definition.get("assertionId")
                assertion = require_assertion(aid, "definition", f"term {term.get('id')} {definition_field}")
                if assertion:
                    if definition_field == "definitions" and aid not in term_assertions:
                        errors.append(f"term {term.get('id')} omits definition assertion {aid} from sourceAssertionIds")
                    if definition_field == "definitions":
                        if not definition.get("publishable") or not assertion.get("publishable"):
                            errors.append(f"active definition {term.get('id')} / {aid} is not publishable")
                    elif definition.get("publishable") or assertion.get("publishable"):
                        errors.append(f"legacy definition {term.get('id')} / {aid} must remain non-publishable")
                    if definition.get("text") != assertion.get("claimText") and definition_field == "definitions":
                        errors.append(f"active definition {term.get('id')} / {aid} text differs from assertion claimText")
                    if not assertion.get("locator"):
                        errors.append(f"definition assertion {aid} lacks locator")
        if term.get("definitions") and (not term_assertions or not topics):
            errors.append(f"published term {term.get('id')} lacks source assertions or RPD topic mapping")
        if not term_assertions <= assertion_ids:
            errors.append(f"term {term.get('id')} has dangling sourceAssertionIds")

    for collection, claim_type in ((actions, "action"), (functions, "function")):
        for item in collection:
            assertion = require_assertion(item.get("sourceAssertionId"), claim_type, f"{claim_type} {item.get('id')}")
            if assertion and (assertion.get("evidenceStatus") != "direct" or not assertion.get("locator")):
                errors.append(f"published {claim_type} {item.get('id')} lacks direct evidence/locator")
            if not item.get("source"):
                errors.append(f"{claim_type} {item.get('id')} lacks source path")

    seen_relations: set[tuple[str, str, str]] = set()
    for index, link in enumerate(links, start=1):
        owner = f"term relation {index}"
        if link.get("from") not in term_ids or link.get("to") not in term_ids:
            errors.append(f"{owner} has dangling term endpoint")
        if link.get("from") == link.get("to"):
            errors.append(f"{owner} is a self-link")
        relation_type = link.get("relationType")
        key = (link.get("from"), link.get("to"), relation_type)
        if key in seen_relations:
            errors.append(f"{owner} duplicates a typed relation")
        seen_relations.add(key)
        if relation_type not in relation_types or relation_type not in RELATION_TYPES:
            errors.append(f"{owner} has invalid relationType")
        if link.get("direction") != "source_to_target":
            errors.append(f"{owner} has invalid direction")
        assertion = require_assertion(link.get("sourceAssertionId"), "relation", owner)
        if assertion:
            if assertion.get("evidenceStatus") != link.get("evidenceStatus"):
                errors.append(f"{owner} evidenceStatus differs from its assertion")
            if not assertion.get("locator") or assertion.get("sourceId") not in source_ids:
                errors.append(f"{owner} lacks source/locator provenance")
            if assertion.get("evidenceStatus") == "not-established" and link.get("publishable"):
                errors.append(f"{owner} publishes a non-established hypothesis")

    for index, link in enumerate(element_links, start=1):
        owner = f"element link {index}"
        source = link.get("from", {})
        target = link.get("to", {})
        if source.get("type") != "term" or source.get("id") not in term_ids:
            errors.append(f"{owner} has wrong-type/dangling term source")
        valid_target = (target.get("type") == "action" and target.get("id") in action_ids) or (target.get("type") == "function" and target.get("id") in function_ids)
        if not valid_target:
            errors.append(f"{owner} has wrong-type/dangling action/function target")
        if link.get("relationType") not in relation_types or link.get("relationType") not in {"used-in", "computed-by"}:
            errors.append(f"{owner} has unsupported relationType")
        if link.get("direction") != "source_to_target":
            errors.append(f"{owner} has invalid direction")
        assertion = require_assertion(link.get("sourceAssertionId"), "relation", owner)
        if assertion and (assertion.get("evidenceStatus") != link.get("evidenceStatus") or assertion.get("evidenceStatus") != "direct"):
            errors.append(f"{owner} is not supported by matching direct evidence")
    if not element_links:
        errors.append("typed term-to-action/function elementLinks must not be empty")

    # Four-way method/practice status registry and source file locators.
    seen_method_ids: set[str] = set()
    audit_counts: Counter[str] = Counter()
    for method in methods:
        mid = method.get("id")
        if not mid or mid in seen_method_ids:
            errors.append(f"methodPractice has missing or duplicate id {mid!r}")
        seen_method_ids.add(mid)
        if not method.get("name") or method.get("verificationStatus") not in ALLOWED_METHOD_STATUSES:
            errors.append(f"methodPractice {mid} has missing name or invalid verification status")
        assertion = require_assertion(method.get("sourceAssertionId"), "method_practice", f"methodPractice {mid}")
        if assertion and (not method.get("locator") or method.get("locator") != assertion.get("locator")):
            errors.append(f"methodPractice {mid} locator differs from its source assertion")
        audit_record = method.get("auditRecord", "")
        audit_path = audit_record.rsplit(":", 1)[0] if ":" in audit_record else audit_record
        if audit_path not in AUDIT_REPORTS or not (root / audit_path).is_file():
            errors.append(f"methodPractice {mid} has missing/unrecognized auditRecord {audit_record!r}")
        else:
            audit_counts[audit_path] += 1
    if len(methods) != meta.get("methodPracticeCount"):
        errors.append("methodPracticeCount does not match methodPractices")
    # Reconcile method registrations to manifest candidate inventory, rather than
    # freezing report totals here. Per-file source reconciliation below separately
    # requires every audited candidate to be registered or explicitly excluded.

    # The unknown state is absence of evidence; known values require direct source evidence.
    coverage_by_topic = {row.get("rpdTopicId"): row for row in coverage}
    if len(coverage_by_topic) != len(coverage) or set(coverage_by_topic) != set(range(1, 8)):
        errors.append("coverage must contain exactly one row for each RPD topic 1–7")
    for row in coverage:
        topic_id = row.get("rpdTopicId")
        for axis, allowed_statuses in COVERAGE_STATUSES.items():
            value = row.get(axis)
            if not isinstance(value, dict) or value.get("status") not in allowed_statuses:
                errors.append(f"coverage topic {topic_id} {axis} has invalid status")
                continue
            status = value["status"]
            evidence_ids = value.get("evidenceIds") or []
            assertion_id = value.get("sourceAssertionId")
            if status == "unknown":
                if evidence_ids or assertion_id:
                    errors.append(f"unknown coverage topic {topic_id} {axis} must not carry evidence")
            else:
                refs = list(evidence_ids) + ([assertion_id] if assertion_id else [])
                if not refs:
                    errors.append(f"known coverage topic {topic_id} {axis} requires direct evidence")
                for ref in refs:
                    assertion = assertions_by_id.get(ref)
                    if not assertion or assertion.get("claimType") != "coverage" or assertion.get("evidenceStatus") != "direct":
                        errors.append(f"coverage topic {topic_id} {axis} references non-direct/missing coverage assertion {ref!r}")

    # Seven RPD topics, valid current index anchors, and 3/4 inversion.
    crosswalk = meta.get("rpdCrosswalk", [])
    if len(crosswalk) != 7 or {row.get("number") for row in crosswalk} != set(range(1, 8)):
        errors.append("meta.rpdCrosswalk must contain exactly RPD topics 1–7")
    rpd_by_number = {row.get("number"): row for row in crosswalk}
    if rpd_by_number.get(3, {}).get("indexSection") != "topic-4" or rpd_by_number.get(4, {}).get("indexSection") != "topic-3":
        errors.append("RPD topic 3/4 index-section inversion is incorrect")
    root_index = root / "index.html"
    index_info = _parse_html(root_index)
    if not index_info:
        errors.append("root index.html is missing/unreadable")
        index_info = HtmlIndex()
    for row in crosswalk:
        anchor = row.get("indexSection")
        if anchor not in index_info.ids:
            errors.append(f"RPD topic {row.get('number')} index anchor #{anchor} is missing")

    for row in coverage:
        availability = row.get("materialAvailability", {})
        if availability.get("status") == "unknown":
            continue
        assertion = assertions_by_id.get(availability.get("sourceAssertionId"), {})
        locator = assertion.get("locator", "")
        match = re.match(r"^([^,\s]+\.html(?:#[^,\s]+)?)", locator)
        if not match:
            errors.append(f"coverage topic {row.get('rpdTopicId')} material locator must start with a local HTML path/anchor")
            continue
        resolved = _local_path(match.group(1), root)
        if resolved is None:
            errors.append(f"coverage topic {row.get('rpdTopicId')} material locator is not local")
            continue
        target, fragment = resolved
        if not target.is_file():
            errors.append(f"coverage topic {row.get('rpdTopicId')} material locator references missing file {match.group(1)}")
        elif fragment:
            page = _parse_html(target)
            if not page or fragment not in page.ids:
                errors.append(f"coverage topic {row.get('rpdTopicId')} material locator references missing HTML anchor #{fragment}")

    # Exact closed student source set: meta course sources plus unexcluded topic-section links.
    manifest_path = root / "ontology/source_corpus_manifest.json"
    if manifest_data is None:
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"cannot read source corpus manifest: {exc}")
            manifest = {}
    else:
        manifest = manifest_data
    corpus_rows = manifest.get("corpus", []) if isinstance(manifest, dict) else []
    reviewed_html_count = sum(
        row.get("reviewState") == "reviewed" and row.get("format") in {"html", "htm"}
        for row in corpus_rows
    )
    if meta.get("pagesReviewed") != reviewed_html_count:
        errors.append(
            f"meta.pagesReviewed is stale: expected {reviewed_html_count} reviewed HTML files"
        )
    exclusions = manifest.get("exclusions", []) if isinstance(manifest, dict) else []
    excluded_paths: set[str] = set()
    for item in exclusions:
        reason = item.get("reason")
        paths = item.get("paths", [])
        if paths and not reason:
            errors.append(f"source exclusion {item.get('category')} has no reason")
        excluded_paths.update(_path_key(path) for path in paths)
    corpus_by_path = {_path_key(row.get("path", "")): row for row in corpus_rows if row.get("path")}
    if len(corpus_by_path) != len(corpus_rows):
        errors.append("corpus manifest contains duplicate or empty paths")
    course_sources = {_path_key(path) for path in meta.get("courseSources", [])}
    corpus_html = {path for path, row in corpus_by_path.items() if row.get("format") in {"html", "htm"}}
    student_index_links: set[str] = set()
    for topic, paths in index_info.topic_links.items():
        for path in paths:
            if path in excluded_paths:
                continue
            if path not in corpus_by_path:
                errors.append(f"unclassified local HTML link in {topic}: {path}")
                continue
            student_index_links.add(path)
    expected_html = course_sources | student_index_links
    if corpus_html != expected_html:
        missing = sorted(expected_html - corpus_html)
        extra = sorted(corpus_html - expected_html)
        errors.append(f"corpus HTML set differs from meta.courseSources ∪ root topic sources (missing={missing}; extra={extra})")
    if "topic4_warehouse_practicum.html" not in corpus_html:
        errors.append("student-facing topic4_warehouse_practicum.html must be in the source corpus")
    teacher_path = "topic4_warehouse_teacher_plan.html"
    if teacher_path in corpus_html or teacher_path in course_sources or teacher_path not in excluded_paths:
        errors.append("topic4_warehouse_teacher_plan.html must be excluded explicitly and absent from sources")
    for path in course_sources:
        if path not in corpus_html:
            errors.append(f"meta.courseSources entry {path} is not in the corpus manifest")

    counts_by_audit: dict[str, Counter] = {}
    named_counts_by_path: dict[str, int] = {}
    candidate_exclusions_by_path: dict[str, set[str]] = {}
    for path, row in corpus_by_path.items():
        audit_record = row.get("auditRecord")
        audit_path = audit_record if isinstance(audit_record, str) else ""
        if audit_path not in AUDIT_REPORTS or not (root / audit_path).is_file():
            errors.append(f"corpus file {path} has missing/unrecognized auditRecord {audit_record!r}")
            continue
        counts = row.get("auditCounts")
        if not isinstance(counts, dict):
            errors.append(f"corpus file {path} lacks per-file auditCounts")
            continue
        expected_keys = {"namedCandidates", "relationStatements", "eligibleRelationStatements", "productObservations", "excludedRelationStatements"}
        if not expected_keys <= set(counts):
            errors.append(f"corpus file {path} has incomplete auditCounts")
            continue
        if any(type(counts.get(key)) is not int or counts[key] < 0 for key in expected_keys):
            errors.append(f"corpus file {path} auditCounts must be non-negative integers")
            continue
        if counts["relationStatements"] != sum(counts[key] for key in ("eligibleRelationStatements", "productObservations", "excludedRelationStatements")):
            errors.append(f"corpus file {path} relation candidate partitions do not sum")
        aggregate = counts_by_audit.setdefault(audit_path, Counter())
        for key in expected_keys:
            aggregate[key] += counts[key]
        named_counts_by_path[path] = counts["namedCandidates"]
        exclusions_for_file = row.get("candidateExclusions", [])
        excluded_ids: set[str] = set()
        for exclusion in exclusions_for_file:
            candidate_id = exclusion.get("auditCandidateId")
            reason = exclusion.get("reason")
            if not candidate_id or not reason or candidate_id in excluded_ids:
                errors.append(f"corpus file {path} has invalid/duplicate candidate exclusion")
                continue
            excluded_ids.add(candidate_id)
            report_text = (root / audit_path).read_text(encoding="utf-8")
            if candidate_id not in report_text:
                errors.append(f"candidate exclusion {candidate_id} for {path} is absent from its audit report")
        candidate_exclusions_by_path[path] = excluded_ids

    # Every corpus file is present/reviewed and in the expected local format.
    for path, row in corpus_by_path.items():
        target = root / path
        if not target.is_file():
            errors.append(f"corpus file is missing: {path}")
        if row.get("present") is not True or row.get("reviewState") != "reviewed":
            errors.append(f"corpus file {path} is not explicitly present and reviewed")
        suffix = PurePosixPath(path).suffix.lower().lstrip(".")
        if row.get("format") != suffix:
            errors.append(f"corpus format mismatch for {path}: {row.get('format')!r} vs .{suffix}")
    for path in course_sources:
        target = root / path
        if PurePosixPath(path).suffix.lower() not in {".html", ".htm"} or not target.is_file():
            errors.append(f"meta.courseSources is not a present local HTML source: {path}")

    # Confirm local linked PDF/PPTX sources are all represented in the corpus.
    teaching_html = course_sources | student_index_links
    linked_attachments: set[str] = set()
    for relpath in teaching_html:
        page = _parse_html(root / relpath)
        if page:
            # The parser reports links relative to the page; rebase those to repo root.
            for attachment in page.attachments:
                linked_attachments.add(str(PurePosixPath(relpath).parent / attachment))
    asset_index = _parse_html(root / "assets/index.html")
    if asset_index:
        linked_attachments.update(str(PurePosixPath("assets") / item) for item in asset_index.attachments)
    corpus_attachments = {path for path, row in corpus_by_path.items() if row.get("format") in {"pdf", "pptx"}}
    if corpus_attachments != linked_attachments:
        errors.append(f"attachment corpus differs from linked local PDF/PPTX set (missing={sorted(linked_attachments-corpus_attachments)}; extra={sorted(corpus_attachments-linked_attachments)})")

    # Verify local files/anchors referenced by source records, definitions, actions, functions and crosswalk.
    local_references: list[tuple[str, str]] = []
    local_references.extend(
        (f"source {row.get('id')}", row.get("uri", ""))
        for row in sources
        if PurePosixPath(urlsplit(row.get("uri", "")).path).suffix.lower() in {".html", ".htm", ".pdf", ".pptx"}
    )
    local_references.extend((f"term {term.get('id')} definition", definition.get("source", "")) for term in terms for definition in term.get("definitions", []) + term.get("legacyDefinitions", []))
    local_references.extend((f"action {item.get('id')}", item.get("source", "")) for item in actions)
    local_references.extend((f"function {item.get('id')}", item.get("source", "")) for item in functions)
    local_references.extend((f"term relation {index}", item.get("source", "")) for index, item in enumerate(links, start=1) if item.get("publishable") is not False)
    for owner, reference in local_references:
        if not reference:
            errors.append(f"{owner} has empty source reference")
            continue
        resolved = _local_path(reference, root)
        if resolved is None:
            continue
        target, fragment = resolved
        if not target.is_file():
            errors.append(f"{owner} references missing local file {reference}")
            continue
        if fragment and target.suffix.lower() in {".html", ".htm"}:
            parser = _parse_html(target)
            if parser and fragment not in parser.ids:
                errors.append(f"{owner} references missing HTML anchor #{fragment} in {reference}")

    # Crosswalk evidence must resolve to an actual file and its cited heading/anchor.

    crosswalk_ref = meta.get("productCrosswalk")
    if not isinstance(crosswalk_ref, dict) or not crosswalk_ref.get("path") or not crosswalk_ref.get("checkedDate"):
        errors.append("meta.productCrosswalk must provide path and checkedDate")
    else:
        crosswalk_file = root / crosswalk_ref["path"]
        if not crosswalk_file.is_file():
            errors.append(f"product crosswalk file is missing: {crosswalk_ref['path']}")
        else:
            try:
                product = json.loads(crosswalk_file.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                errors.append(f"cannot load product crosswalk: {exc}")
                product = {}
            if product.get("checkedDate") != crosswalk_ref.get("checkedDate") or product.get("title") != crosswalk_ref.get("title"):
                errors.append("meta.productCrosswalk title/date do not match the referenced crosswalk")
            product_rows = product.get("erpFunctionality", [])
            product_ids = [row.get("id") for row in product_rows]
            if not product_ids or any(not value for value in product_ids) or len(product_ids) != len(set(product_ids)):
                errors.append("product crosswalk ERP functionality entries need unique non-empty IDs")
            for entry in product_rows:
                if not entry.get("vendorUrl", "").startswith("https://"):
                    errors.append(f"product crosswalk {entry.get('id')} lacks an HTTPS vendor URL")
                mapping = entry.get("courseMapping", {})
                for evidence in mapping.get("evidence", []):
                    evidence_path = evidence.get("path", "")
                    if not evidence_path:
                        continue
                    evidence_target = _local_path(evidence_path, root)
                    if evidence_target is None:
                        errors.append(f"product crosswalk {entry.get('id')} has non-local evidence path {evidence_path}")
                        continue
                    evidence_file, evidence_fragment = evidence_target
                    if not evidence_file.is_file():
                        errors.append(f"product crosswalk {entry.get('id')} references missing course evidence {evidence_path}")
                        continue
                    heading = evidence.get("heading", "")
                    page = _parse_html(evidence_file)
                    if evidence_fragment and page and evidence_fragment not in page.ids:
                        errors.append(f"product crosswalk {entry.get('id')} references missing anchor #{evidence_fragment} in {evidence_path}")
                    if page and heading:
                        page_text = " ".join(" ".join(page.text).split()).casefold()
                        normalized_heading = " ".join(str(heading).split()).casefold()
                        if normalized_heading not in page_text:
                            errors.append(f"product crosswalk {entry.get('id')} heading locator not found in {evidence_path}: {heading}")

    # Reconcile every per-file inventory with the independently enumerated report totals.
    for path in AUDIT_REPORTS:
        report = root / path
        if not report.is_file():
            errors.append(f"required source audit report is missing: {path}")
    html_first = root / "ontology/source_audit/html-01-10.md"
    html_second = root / "ontology/source_audit/html-11-20.md"
    attachments_report = root / "ontology/source_audit/attachments.md"
    first_text = html_first.read_text(encoding="utf-8") if html_first.is_file() else ""
    second_text = html_second.read_text(encoding="utf-8") if html_second.is_file() else ""
    attachment_text = attachments_report.read_text(encoding="utf-8") if attachments_report.is_file() else ""
    report_totals: dict[str, dict[str, int]] = {}
    first_match = re.search(r"Fresh reconciled totals:.*?\*\*(\d+) named candidates\*\* and \*\*(\d+) eligible relation source-statements\*\*", first_text, re.S)
    second_match = re.search(
        r"\|\s*\*\*Total\*\*\s*\|\s*\*\*(\d+)\*\*\s*\|\s*\*\*(\d+)\*\*\s*\|\s*\*\*(\d+)\*\*\s*\|\s*\*\*(\d+)\*\*\s*\|\s*\*\*(\d+)\*\*\s*\|",
        second_text,
    )
    attachment_match = re.search(r"\|\s*\*\*Total\*\*\s*\|\s*\*\*(\d+)\*\*\s*\|\s*\*\*(\d+)\*\*\s*\|\s*\*\*(\d+)\*\*\s*\|\s*\*\*(\d+)\*\*\s*\|", attachment_text)
    if not first_match:
        errors.append("ontology/source_audit/html-01-10.md lacks reconciled named-candidate/relation totals")
    else:
        first_named, first_relations = int(first_match.group(1)), int(first_match.group(2))
        report_totals["ontology/source_audit/html-01-10.md"] = {
            "namedCandidates": first_named,
            "eligibleRelationStatements": first_relations,
            "productObservations": 0,
            "excludedRelationStatements": 0,
            "relationStatements": first_relations,
        }
    if not second_match:
        errors.append("ontology/source_audit/html-11-20.md lacks reconciled statement-row totals")
    else:
        second_named, second_eligible, second_product, second_excluded, second_total = map(int, second_match.groups())
        report_totals["ontology/source_audit/html-11-20.md"] = {
            "namedCandidates": second_named,
            "eligibleRelationStatements": second_eligible,
            "productObservations": second_product,
            "excludedRelationStatements": second_excluded,
            "relationStatements": second_total,
        }
        if second_eligible + second_product + second_excluded != second_total:
            errors.append("HTML 11–20 relation/product/exclusion partitions do not sum to statement-row total")
    if not attachment_match:
        errors.append("attachment audit lacks its five-column relation accounting total")
    else:
        report_totals["ontology/source_audit/attachments.md"] = {
            "eligibleRelationStatements": int(attachment_match.group(1)),
            "productObservations": int(attachment_match.group(2)),
            "excludedRelationStatements": int(attachment_match.group(3)),
            "relationStatements": int(attachment_match.group(4)),
        }
        if sum(report_totals["ontology/source_audit/attachments.md"][key] for key in ("eligibleRelationStatements", "productObservations", "excludedRelationStatements")) != report_totals["ontology/source_audit/attachments.md"]["relationStatements"]:
            errors.append("attachment relation partitions do not sum to the audited row total")
    for audit_path, report_counts in report_totals.items():
        manifest_counts = counts_by_audit.get(audit_path, Counter())
        for key, expected in report_counts.items():
            if manifest_counts.get(key) != expected:
                errors.append(f"manifest per-file counts do not reconcile to {audit_path} {key}: expected {expected}, got {manifest_counts.get(key, 0)}")

    # Cross-check per-file counts against the detailed HTML 11–20 and attachment tables.
    for row in corpus_rows:
        path = _path_key(row.get("path", ""))
        counts = row.get("auditCounts", {})
        audit_path = row.get("auditRecord")
        if audit_path == "ontology/source_audit/html-11-20.md":
            filename = PurePosixPath(path).name
            match = re.search(
                rf"\|\s*\d+\s+`{re.escape(filename)}`\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|",
                second_text,
            )
            actual = (
                counts.get("namedCandidates"), counts.get("eligibleRelationStatements"),
                counts.get("productObservations"), counts.get("excludedRelationStatements"),
                counts.get("relationStatements"),
            )
            if not match or actual != tuple(map(int, match.groups())):
                errors.append(f"per-file auditCounts do not match the HTML 11–20 reconciliation row for {path}")
        elif audit_path == "ontology/source_audit/attachments.md":
            basename = PurePosixPath(path).name
            alias = "PDF" if path.endswith(".pdf") else ("Seminar 1" if "Семинар 1_" in basename else "Seminar 2")
            row_match = re.search(rf"\|\s*{re.escape(alias)}\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|", attachment_text)
            candidate_prefix = {"PDF": "PDF-M", "Seminar 1": "S1-M", "Seminar 2": "S2-M"}[alias]
            candidate_count = len(re.findall(rf"\|\s*{candidate_prefix}\d+\s*\|", attachment_text))
            if not row_match:
                errors.append(f"attachment audit lacks a per-file relation row for {path}")
            else:
                expected_values = (int(row_match.group(4)), int(row_match.group(1)), int(row_match.group(2)), int(row_match.group(3)))
                actual_values = (counts.get("relationStatements"), counts.get("eligibleRelationStatements"), counts.get("productObservations"), counts.get("excludedRelationStatements"))
                if actual_values != expected_values:
                    errors.append(f"per-file relation auditCounts do not match attachment report for {path}")
            if counts.get("namedCandidates") != candidate_count:
                errors.append(f"per-file named candidate count does not match attachment audit rows for {path}: expected {candidate_count}")
        elif audit_path == "ontology/source_audit/html-01-10.md":
            file_name = PurePosixPath(path).name
            expected: tuple[int, int] | None = None
            if file_name in {"lecture1_student_guide.html", "seminar1_analyst_case.html"}:
                row_match = re.search(rf"\|\s*`{re.escape(file_name)}`\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|", first_text)
                if row_match:
                    expected = (int(row_match.group(2)), int(row_match.group(1)))
            elif file_name in {"ai_analyst_tools.html", "lecture2_student_guide.html", "seminar2_production_case.html"}:
                prefix = {"ai_analyst_tools.html": "A", "lecture2_student_guide.html": "L", "seminar2_production_case.html": "S"}[file_name]
                named = len(re.findall(rf"^\|{prefix}-M\d+\|", first_text, re.M))
                relations = len(re.findall(rf"^\|{prefix}\d+\|", first_text, re.M))
                expected = (named, relations)
            elif file_name in {"Практикумы №1–2 — разбор.html", "Практикум №3–6 — разбор.html"}:
                relation_match = re.search(rf"^## `{re.escape(file_name)}` — (\d+) rows$", first_text, re.M)
                candidate_key = "Practice 1–2" if file_name.startswith("Практикумы №1–2") else "Practice 3–6"
                candidate_match = re.search(rf"{re.escape(candidate_key)}:\s*(\d+)(?: candidates)?", first_text)
                if relation_match and candidate_match:
                    expected = (int(candidate_match.group(1)), int(relation_match.group(1)))
            elif file_name in {"Практикумы №7–8 — разбор.html", "seminar1_toir_notes.html", "seminar2_toir_execution.html"}:
                row_match = re.search(rf"^## \d+\. `{re.escape(file_name)}` — (\d+) named candidates; (\d+) relations$", first_text, re.M)
                if row_match:
                    expected = (int(row_match.group(1)), int(row_match.group(2)))
            if expected is None or (counts.get("namedCandidates"), counts.get("relationStatements")) != expected:
                errors.append(f"per-file auditCounts do not match the HTML 01–10 source-audit table for {path}")

    # Every named audit candidate is either represented in the structured register or explicitly excluded with a reason.
    method_counts_by_source: Counter[str] = Counter()
    for method in methods:
        assertion = assertions_by_id.get(method.get("sourceAssertionId"), {})
        source = sources_by_id.get(assertion.get("sourceId"), {})
        source_path = _path_key(source.get("uri", ""))
        method_counts_by_source[source_path] += 1
    for path, row in corpus_by_path.items():
        expected_registry_rows = named_counts_by_path.get(path)
        if expected_registry_rows is None:
            continue
        excluded_ids = candidate_exclusions_by_path.get(path, set())
        if len(excluded_ids) > expected_registry_rows:
            errors.append(f"candidate exclusions exceed named candidate count for {path}")
            continue
        expected_registry_rows -= len(excluded_ids)
        actual_registry_rows = method_counts_by_source.get(path, 0)
        if actual_registry_rows != expected_registry_rows:
            errors.append(f"named candidate register mismatch for {path}: audit requires {expected_registry_rows} candidate rows after explicit exclusions, got {actual_registry_rows}")

    expected_method_counts_by_audit: Counter[str] = Counter()
    for path, row in corpus_by_path.items():
        audit_path = row.get("auditRecord")
        expected_method_counts_by_audit[audit_path] += max(
            0, named_counts_by_path.get(path, 0) - len(candidate_exclusions_by_path.get(path, set()))
        )
    for audit_path in AUDIT_REPORTS:
        expected = expected_method_counts_by_audit[audit_path]
        if audit_counts[audit_path] != expected:
            errors.append(f"methodPractice audit-count mismatch for {audit_path}: expected {expected}, got {audit_counts[audit_path]}")

    # Publication allowlist: Pages must copy all source-linked ontology data files.
    workflow = root / ".github/workflows/pages.yml"
    if not workflow.is_file():
        errors.append("Pages workflow is missing")
    else:
        workflow_text = workflow.read_text(encoding="utf-8")
        for target in ("ontology/validate_knowledge_ontology.py", "ontology/build_knowledge_ontology_bundle.py"):
            if target not in workflow_text:
                errors.append(f"Pages workflow does not run {target}")
        validate_pos = workflow_text.find("ontology/validate_knowledge_ontology.py")
        build_pos = workflow_text.find("ontology/build_knowledge_ontology_bundle.py")
        if validate_pos < 0 or build_pos < 0 or validate_pos > build_pos:
            errors.append("Pages workflow must run ontology validation before bundle generation")
        if crosswalk_ref and crosswalk_ref.get("path"):
            rel = crosswalk_ref["path"]
            if rel not in workflow_text:
                errors.append(f"Pages workflow does not publish {rel}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="repository root (defaults to this checkout)")
    args = parser.parse_args()
    errors = validate_ontology(root=args.root.resolve())
    if errors:
        print("Ontology validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Ontology validation passed: schema, evidence references, corpus, crosswalk and publication paths are consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
