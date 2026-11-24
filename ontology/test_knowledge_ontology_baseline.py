"""Regression guard for the pre-migration ontology baseline.

Run from the repository root with:
    python3 -m unittest ontology.test_knowledge_ontology_baseline -v
The content digests below intentionally cover identity and definition text only;
new schema fields may be added without changing this baseline.
"""

import hashlib
from html.parser import HTMLParser
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
ONTOLOGY_PATH = ROOT / "ontology" / "knowledge_ontology.json"
MANIFEST_PATH = ROOT / "ontology" / "source_corpus_manifest.json"


def canonical_digest(lines):
    """SHA-256 of sorted canonical UTF-8 records, joined with LF."""
    payload = "\n".join(sorted(lines)).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def load_data():
    return json.loads(ONTOLOGY_PATH.read_text(encoding="utf-8"))


def definition_rows(terms):
    """Yield active and archived definition rows with their term identity."""
    for term in terms:
        for field in ("definitions", "legacyDefinitions"):
            for definition in term.get(field, []):
                yield term, definition, field


def assertion_id(assertion):
    return assertion.get("id") if isinstance(assertion, dict) else assertion


def relation_type_catalog(data):
    catalog = data.get("meta", {}).get("relationTypes", [])
    if isinstance(catalog, dict):
        return catalog
    return {
        row if isinstance(row, str) else row["id"]: row
        for row in catalog
        if isinstance(row, str) or (isinstance(row, dict) and row.get("id"))
    }


def vocabulary_values(data, key):
    values = data.get("meta", {}).get(key, [])
    if isinstance(values, dict):
        return set(values)
    return {
        value if isinstance(value, str) else value["id"]
        for value in values
        if isinstance(value, str) or (isinstance(value, dict) and value.get("id"))
    }


def relation_semantics(data, relation_type):
    descriptor = relation_type_catalog(data).get(relation_type, {})
    if isinstance(descriptor, str):
        return descriptor.lower()
    return " ".join(
        str(descriptor.get(key, ""))
        for key in ("label", "description", "meaning", "id")
    ).lower()


class RootIndexHtmlLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paths = set()
        self.topic_headings = {}
        self._topic = None
        self._heading_parts = []
        self._in_heading = False

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "section" and attributes.get("id", "").startswith("topic-"):
            self._topic = attributes["id"]
        elif tag == "h2" and self._topic:
            self._in_heading = True
            self._heading_parts = []
        href = attributes.get("href", "")
        if tag == "a" and href.lower().endswith(".html"):
            self.paths.add(href)

    def handle_endtag(self, tag):
        if tag == "h2" and self._in_heading and self._topic:
            self.topic_headings[self._topic] = " ".join("".join(self._heading_parts).split())
            self._in_heading = False
        elif tag == "section" and self._topic:
            self._topic = None

    def handle_data(self, data):
        if self._in_heading:
            self._heading_parts.append(data)


class HtmlHeadings(HTMLParser):
    def __init__(self):
        super().__init__()
        self.active = False
        self.parts = []
        self.headings = set()

    def handle_starttag(self, tag, attrs):
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self.active = True
            self.parts = []

    def handle_endtag(self, tag):
        if self.active and tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self.headings.add(" ".join("".join(self.parts).split()))
            self.active = False

    def handle_data(self, data):
        if self.active:
            self.parts.append(data)


class OntologyBaselineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = load_data()
        cls.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    def test_json_and_baseline_entity_counts(self):
        data = self.data
        self.assertEqual(7, len(data["clusters"]))
        self.assertEqual(239, len(data["terms"]))
        active_definitions = sum(len(term.get("definitions", [])) for term in data["terms"])
        legacy_definitions = sum(len(term.get("legacyDefinitions", [])) for term in data["terms"])
        self.assertEqual(data["meta"]["sourceDefinitionEntries"], active_definitions)
        self.assertEqual(data["meta"]["legacyDefinitionEntries"], legacy_definitions)
        self.assertEqual(340, sum(
            definition.get("baselineDefinition") is True
            for _, definition, _ in definition_rows(data["terms"])
        ))
        self.assertEqual(29, len(data["actions"]))
        self.assertEqual(4, len(data["functions"]))

    def test_reviewed_html_page_count_matches_source_manifest(self):
        reviewed_html = sum(
            row.get("reviewState") == "reviewed" and row.get("format") in {"html", "htm"}
            for row in self.manifest["corpus"]
        )
        self.assertEqual(20, reviewed_html)
        self.assertEqual(reviewed_html, self.data["meta"]["pagesReviewed"])

    def test_public_graph_omits_nonpublishable_hypothesis_and_unsafe_source_schemes(self):
        links = {row["sourceAssertionId"]: row for row in self.data["links"]}
        hypothesis = links["assert-relation-007"]
        self.assertFalse(hypothesis["publishable"])
        public_links = [row for row in self.data["links"] if row.get("publishable") is True]
        self.assertNotIn(hypothesis, public_links)
        sources = {row["id"]: row for row in self.data["sources"]}
        self.assertEqual("editorial-hypothesis", sources["source-051"]["kind"])

        html = (ROOT / "ontology" / "index.html").read_text(encoding="utf-8")
        self.assertIn("if(link.publishable!==true)continue;", html)
        self.assertNotIn("link.publishable===false", html)
        self.assertNotIn("record.link.publishable===false", html)
        self.assertIn("непубликуемые редакторские гипотезы", html)
        self.assertIn("const hasScheme=/^[a-z][a-z\\d+.-]*:/i.test(path);", html)
        self.assertIn("const localDocument=!hasScheme&&", html)

    def test_stable_entity_ids_and_definition_text(self):
        expected = {
            "terms": "9a9cd87fd6ff26c326083338fd531dea00f246641e341c6b5be77e3a66f25423",
            "actions": "047abae4f4dbe9f14939f458862ef5ca9e41920179beca12e0e8856aa6b3c1ca",
            "functions": "6dfc7112a2c5bbe39bf6d1a6700b8e41898b24399eb2329633b128d5744dfa95",
        }
        for entity, expected_digest in expected.items():
            with self.subTest(entity=entity):
                ids = [item["id"] for item in self.data[entity]]
                self.assertEqual(len(ids), len(set(ids)), f"duplicate {entity} IDs")
                self.assertEqual(expected_digest, canonical_digest(ids))

        # Hash the explicitly marked source-baseline rows, whether they remain
        # published or are preserved as retired legacy entries. New corrected
        # definitions can be added without changing this source digest.
        definition_records = [
            f"{term['id']}\t{definition['text']}\t{definition.get('context', '')}"
            for term, definition, _ in definition_rows(self.data["terms"])
            if definition.get("baselineDefinition") is True
        ]
        self.assertEqual(340, len(definition_records))
        self.assertEqual(
            "de5285861ec43fda1ca92639195e10f9a0c71a41de31a08e575e171d98ed4ec4",
            canonical_digest(definition_records),
        )

    def test_existing_term_links_have_unique_valid_endpoints(self):
        ids = [term["id"] for term in self.data["terms"]]
        self.assertEqual(len(ids), len(set(ids)))
        known = set(ids)
        for link in self.data["links"]:
            self.assertIn(link["from"], known)
            self.assertIn(link["to"], known)

    def test_schema_id_namespaces_and_assertion_source_references(self):
        data = self.data
        term_ids = {term["id"] for term in data["terms"]}
        action_ids = {item["id"] for item in data["actions"]}
        function_ids = {item["id"] for item in data["functions"]}
        source_ids = [item["id"] for item in data["sources"]]
        assertion_ids = [item["id"] for item in data["sourceAssertions"]]

        self.assertEqual(data["meta"]["sourceRecordCount"], len(source_ids))
        self.assertEqual(data["meta"]["sourceAssertionCount"], len(assertion_ids))
        self.assertEqual(len(source_ids), len(set(source_ids)))
        self.assertEqual(len(assertion_ids), len(set(assertion_ids)))
        self.assertTrue(set(source_ids).isdisjoint(assertion_ids))
        self.assertTrue(set(source_ids).isdisjoint(term_ids))
        self.assertTrue(set(assertion_ids).isdisjoint(term_ids))
        self.assertTrue(action_ids.isdisjoint(function_ids))

        sources = set(source_ids)
        assertions = {row["id"]: row for row in data["sourceAssertions"]}
        allowed_evidence = vocabulary_values(data, "evidenceStatusVocabulary")
        for row in data["sourceAssertions"]:
            with self.subTest(assertion=row["id"]):
                self.assertIn(row["sourceId"], sources)
                self.assertIn(row["evidenceStatus"], allowed_evidence)
                self.assertTrue(row["claimType"])
                self.assertTrue(row["claimText"])
                self.assertTrue(row["locator"])
                self.assertTrue(row["modality"])

        term_links = data["links"]
        relation_types = relation_type_catalog(data)
        seen = set()
        for link in term_links:
            key = (link["from"], link["to"], link["relationType"])
            with self.subTest(link=key):
                self.assertIn(link["from"], term_ids)
                self.assertIn(link["to"], term_ids)
                self.assertNotEqual(link["from"], link["to"])
                self.assertNotIn(key, seen, "duplicate typed relation")
                seen.add(key)
                self.assertIn(link["relationType"], relation_types)
                self.assertEqual("source_to_target", link["direction"])
                self.assertIn(link["sourceAssertionId"], assertions)
                self.assertEqual("relation", assertions[link["sourceAssertionId"]]["claimType"])
                self.assertEqual(
                    link["evidenceStatus"],
                    assertions[link["sourceAssertionId"]]["evidenceStatus"],
                )

    def test_published_definitions_have_source_backed_definition_assertions(self):
        data = self.data
        assertions = {row["id"]: row for row in data["sourceAssertions"]}
        sources = {row["id"] for row in data["sources"]}
        for term in data["terms"]:
            for definition in term.get("definitions", []):
                with self.subTest(term=term["id"], text=definition.get("text", "")[:40]):
                    self.assertTrue(definition.get("publishable"))
                    self.assertTrue(definition.get("assertionId"))
                    row = assertions[definition["assertionId"]]
                    self.assertEqual("definition", row["claimType"])
                    self.assertTrue(row.get("publishable"))
                    self.assertIn(row["sourceId"], sources)
                    self.assertTrue(row["locator"])
                    self.assertTrue(row["claimText"])

        for collection, claim_type in (("actions", "action"), ("functions", "function")):
            for item in data[collection]:
                with self.subTest(collection=collection, item=item["id"]):
                    row = assertions[item["sourceAssertionId"]]
                    self.assertEqual(claim_type, row["claimType"])
                    self.assertIn(row["sourceId"], sources)

        for term, definition, field in definition_rows(data["terms"]):
            if field != "legacyDefinitions":
                continue
            with self.subTest(term=term["id"], field=field):
                self.assertFalse(definition.get("publishable", False))
                self.assertTrue(
                    definition.get("retirementReason") or definition.get("reason"),
                    "archived definition needs a reason",
                )

    def test_entity_level_legacy_vocabulary_matches_canonical_vocabulary(self):
        self.assertEqual(self.data["meta"]["entityLevelVocabulary"], self.data["meta"]["entityLevels"])

    def test_unknown_entity_levels_are_not_repeated_in_term_cards(self):
        html = (ROOT / "ontology" / "index.html").read_text(encoding="utf-8")
        unknown_terms = [term for term in self.data["terms"] if term["entityLevel"] == "unknown"]
        self.assertGreater(len(unknown_terms), 200)
        start = html.index("const heading=element('h4','',term.label);")
        end = html.index("if(term.rpdTopics?.length)", start)
        card_heading = html[start:end]
        self.assertIn(
            "if(term.entityLevel!=='unknown')heading.append(element('span','kind-label',`Уровень: ${entityLevelLabel(term.entityLevel)}`))",
            card_heading,
        )
        self.assertIn("if(term.entityLevel!=='unknown'&&term.entityLevelReason)", card_heading)
        self.assertIn("unknown-level-explanation", html)
        self.assertIn("entity-level-filter", html)

    def test_rpd_material_status_labels_are_localized_and_complete(self):
        html = (ROOT / "ontology" / "index.html").read_text(encoding="utf-8")
        statuses = {row["materialStatus"] for row in self.data["meta"]["rpdCrosswalk"]}
        import re
        mapping_match = re.search(r"const materialStatusLabels=\{(.*?)\n \};", html, re.S)
        self.assertIsNotNone(mapping_match)
        mapped_statuses = set(re.findall(r"'([^']+)':'", mapping_match.group(1)))
        self.assertEqual(statuses, mapped_statuses)
        self.assertIn("materialStatusLabel(topic.materialStatus)", html)
        self.assertNotIn("${topic.materialStatus}", html)
        self.assertIn("Статус материалов не классифицирован", html)
        self.assertIn("Материалы подготовлены; проведение занятия не подтверждено", html)
        self.assertIn("Частично: материалы подготовлены; проведение занятия не подтверждено", html)
        self.assertNotIn("выдача не подтверждена", html)

    def test_terms_have_conservative_kind_entity_level_and_source_grounded_topics(self):
        allowed_levels = {"class", "instance", "not-applicable", "unknown"}
        allowed_kinds = vocabulary_values(self.data, "kindVocabulary")
        self.assertIn("instance", allowed_levels)
        for term in self.data["terms"]:
            with self.subTest(term=term["id"]):
                self.assertIn(term["entityLevel"], allowed_levels)
                self.assertIn(term["kind"], allowed_kinds)
                if term["kind"] == "unclassified":
                    self.assertTrue(term.get("kindRationale"))
                topics = term["rpdTopics"]
                self.assertIsInstance(topics, list)
                self.assertEqual(len(topics), len(set(topics)))
                self.assertTrue(all(type(topic) is int and 1 <= topic <= 7 for topic in topics))
                if term.get("definitions"):
                    self.assertTrue(topics, "published definitions must map to at least one sourced RPD topic")

        by_id = {term["id"]: term for term in self.data["terms"]}
        self.assertEqual("class", by_id["zakaz-na-remont"]["entityLevel"])
        self.assertEqual("class", by_id["etap-proizvodstva"]["entityLevel"])
        self.assertIn("instance", vocabulary_values(self.data, "entityLevelVocabulary") or allowed_levels)
        self.assertFalse(
            any(term["label"].startswith("УЧ-") for term in self.data["terms"]),
            "synthetic case records are instances, not reusable concept terms",
        )

    def test_method_practice_registry_uses_only_four_source_verification_statuses(self):
        allowed = {
            "verified_against_primary_source",
            "secondary_source_only",
            "primary_source_unavailable",
            "mention_does_not_define_verifiable_method",
        }
        assertions = {row["id"]: row for row in self.data["sourceAssertions"]}
        sources = {row["id"]: row for row in self.data["sources"]}
        self.assertEqual(self.data["meta"]["methodPracticeCount"], len(self.data["methodPractices"]))
        self.assertTrue(
            self.data["methodPractices"],
            "audited named method/practice candidates must not be left as an empty registry",
        )
        ids = [row["id"] for row in self.data["methodPractices"]]
        self.assertEqual(len(ids), len(set(ids)))
        seen_statuses = set()
        for method in self.data["methodPractices"]:
            with self.subTest(method=method["id"]):
                self.assertIn(method["verificationStatus"], allowed)
                seen_statuses.add(method["verificationStatus"])
                self.assertIn(method["sourceAssertionId"], assertions)
                self.assertTrue(method.get("name"))
                self.assertTrue(method.get("locator"))
                assertion = assertions[method["sourceAssertionId"]]
                self.assertEqual("method_practice", assertion["claimType"])
                self.assertIn(assertion["sourceId"], sources)
                self.assertTrue(assertion["locator"])
                self.assertEqual(method["locator"], assertion["locator"])
                source = sources[assertion["sourceId"]]
                self.assertTrue(source.get("uri"), "method candidate must retain its exact local source ID/path")
                self.assertTrue(
                    source["uri"].split("#", 1)[0].endswith(".html")
                    or source["uri"].split("#", 1)[0].lower().endswith((".pdf", ".pptx")),
                    f"method candidate source must identify a local audited file: {source['uri']}",
                )
                self.assertIn(method["name"].casefold(), assertion["claimText"].casefold())
        self.assertEqual(allowed, seen_statuses, "registry must preserve every verification status represented by audited candidates")

    def test_method_practice_registry_reconciles_per_source_audit_candidates(self):
        assertions = {row["id"]: row for row in self.data["sourceAssertions"]}
        sources = {row["id"]: row for row in self.data["sources"]}
        counts = {}
        for method in self.data["methodPractices"]:
            assertion = assertions[method["sourceAssertionId"]]
            path = unquote(sources[assertion["sourceId"]]["uri"].split("#", 1)[0])
            counts[path] = counts.get(path, 0) + 1

        registered = 0
        raw_candidates = 0
        exclusions = 0
        for item in json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))["corpus"]:
            audit_count = item["auditCounts"]["namedCandidates"]
            excluded_count = len(item.get("candidateExclusions", []))
            expected = audit_count - excluded_count
            registered += expected
            raw_candidates += audit_count
            exclusions += excluded_count
            with self.subTest(source=item["path"]):
                self.assertEqual(expected, counts.get(item["path"], 0))

        self.assertEqual(104, raw_candidates)
        self.assertEqual(12, exclusions)
        self.assertEqual(92, registered)
        self.assertEqual(registered, len(self.data["methodPractices"]))

    def test_second_half_method_locators_point_to_canonical_course_files(self):
        assertions = {row["id"]: row for row in self.data["sourceAssertions"]}
        sources = {row["id"]: row for row in self.data["sources"]}
        methods = {
            row["id"]: row
            for row in self.data["methodPractices"]
            if row["id"].startswith("method-")
            and 45 <= int(row["id"].split("-")[-1]) <= 73
        }
        self.assertEqual(29, len(methods))
        for method_id, method in methods.items():
            with self.subTest(method=method_id):
                locator = method["locator"]
                self.assertNotIn("source-audit", locator.lower())
                self.assertNotIn("audited candidate row", locator.lower())
                assertion = assertions[method["sourceAssertionId"]]
                self.assertEqual(locator, assertion["locator"])
                source = sources[assertion["sourceId"]]
                source_path = source["uri"].split("#", 1)[0]
                self.assertTrue(
                    (ROOT / source_path).is_file(),
                    f"canonical method source must resolve locally: {source_path}",
                )

        scor = assertions[methods["method-063"]["sourceAssertionId"]]["claimText"].lower()
        self.assertIn("external reference links", scor)
        self.assertIn("does not teach or define scor", scor)

    def test_coverage_axes_are_independent_and_unknown_has_no_evidence(self):
        data = self.data
        coverage = data["coverage"]
        self.assertEqual(7, len(coverage))
        self.assertEqual(set(range(1, 8)), {row["rpdTopicId"] for row in coverage})
        assertions = {row["id"]: row for row in data["sourceAssertions"]}
        status_vocabularies = {
            "materialAvailability": {"available", "partial", "unavailable", "unknown"},
            "deliveryStatus": {"confirmed", "not_confirmed", "unknown"},
            "assessmentStatus": {"record_present", "record_absent", "unknown"},
        }
        for row in coverage:
            for axis, allowed in status_vocabularies.items():
                value = row[axis]
                status = value["status"]
                with self.subTest(topic=row["rpdTopicId"], axis=axis):
                    self.assertIn(status, allowed)
                    evidence_ids = value.get("evidenceIds", [])
                    assertion_id_value = value.get("sourceAssertionId")
                    if status == "unknown":
                        self.assertFalse(assertion_id_value)
                        self.assertFalse(evidence_ids)
                    else:
                        self.assertTrue(assertion_id_value or evidence_ids)
                        if assertion_id_value:
                            assertion = assertions[assertion_id_value]
                            self.assertEqual("coverage", assertion["claimType"])
                            self.assertEqual("direct", assertion["evidenceStatus"])

    def test_structured_material_availability_matches_topic_index_evidence(self):
        assertions = {row["id"]: row for row in self.data["sourceAssertions"]}
        crosswalk = {row["number"]: row for row in self.data["meta"]["rpdCrosswalk"]}
        root_index = RootIndexHtmlLinks()
        root_index.feed((ROOT / "index.html").read_text(encoding="utf-8"))
        expected = {
            1: "available", 2: "available", 3: "available", 4: "available",
            5: "partial", 6: "partial", 7: "unavailable",
        }
        self.assertEqual(expected, {
            row["rpdTopicId"]: row["materialAvailability"]["status"]
            for row in self.data["coverage"]
        })
        for row in self.data["coverage"]:
            availability = row["materialAvailability"]
            assertion = assertions[availability["sourceAssertionId"]]
            with self.subTest(topic=row["rpdTopicId"]):
                self.assertEqual("coverage", assertion["claimType"])
                self.assertEqual("direct", assertion["evidenceStatus"])
                self.assertEqual("source-058", assertion["sourceId"])
                mapping = crosswalk[row["rpdTopicId"]]
                self.assertTrue(assertion["locator"].startswith(f"index.html#{mapping['indexSection']},"))
                self.assertIn(f"RPD topic title: «{mapping['title']}»", assertion["locator"])
                index_heading = root_index.topic_headings[mapping["indexSection"]]
                self.assertIn(f"section heading «{index_heading}»", assertion["locator"])

    def test_topic_seven_ui_scopes_unavailable_to_current_index(self):
        html = (ROOT / "ontology" / "index.html").read_text(encoding="utf-8")
        assertion = next(row for row in self.data["sourceAssertions"] if row["id"] == "assert-coverage-topic-7-materials")
        self.assertIn("absence from the current indexed course-material corpus", assertion["claimText"])
        self.assertIn("Отдельные материалы в текущем индексе не представлены", html)
        self.assertIn("topic.number===7&&state.status==='unavailable'", html)

    def test_typed_element_links_resolve_and_use_supported_relations(self):
        data = self.data
        term_ids = {row["id"] for row in data["terms"]}
        action_ids = {row["id"] for row in data["actions"]}
        function_ids = {row["id"] for row in data["functions"]}
        assertions = {row["id"]: row for row in data["sourceAssertions"]}
        sources = {row["id"]: row for row in data["sources"]}
        relation_types = relation_type_catalog(data)
        self.assertTrue(data["elementLinks"], "typed term-to-action/function evidence links must not be empty")
        seen = set()
        for link in data["elementLinks"]:
            source = link["from"]
            target = link["to"]
            key = (source["type"], source["id"], target["type"], target["id"], link["relationType"])
            with self.subTest(link=key):
                self.assertEqual("term", source["type"])
                self.assertIn(source["id"], term_ids)
                self.assertIn(target["type"], {"action", "function"})
                self.assertIn(target["id"], action_ids if target["type"] == "action" else function_ids)
                self.assertNotIn(key, seen, "duplicate typed element relation")
                seen.add(key)
                self.assertIn(link["relationType"], relation_types)
                self.assertEqual("source_to_target", link["direction"])
                assertion = assertions[link["sourceAssertionId"]]
                self.assertEqual("relation", assertion["claimType"])
                self.assertEqual(link["evidenceStatus"], assertion["evidenceStatus"])
                self.assertIn(assertion["sourceId"], sources)
                self.assertTrue(assertion["locator"])
                self.assertTrue(assertion["claimText"])
                self.assertNotEqual("unknown", assertion["evidenceStatus"])

    def test_published_relation_claims_use_precise_locators_and_conservative_scope(self):
        assertions = {row["id"]: row for row in self.data["sourceAssertions"]}
        links = {row["sourceAssertionId"]: row for row in self.data["links"]}

        order_supply = assertions["assert-relation-001"]
        self.assertEqual("indirect", order_supply["evidenceStatus"])
        self.assertIn("11-R16", order_supply["locator"])
        self.assertIn("11-R17", order_supply["locator"])
        self.assertIn("планируют обеспечение", order_supply["claimText"])
        self.assertIn("один из возможных способов", order_supply["claimText"])
        self.assertEqual("indirect", links["assert-relation-001"]["evidenceStatus"])

        expected_locators = {
            "assert-relation-002": "18-R02",
            "assert-relation-003": "L51",
            "assert-relation-004": "#scheme-repair-order",
            "assert-relation-005": "9-R09",
            "assert-relation-006": "16-R02",
        }
        for assertion_id, locator_fragment in expected_locators.items():
            with self.subTest(assertion=assertion_id):
                self.assertIn(locator_fragment, assertions[assertion_id]["locator"])

        specification_order = assertions["assert-relation-003"]
        self.assertEqual("source-023", specification_order["sourceId"])
        self.assertIn("если", links["assert-relation-003"]["label"])
        self.assertEqual("related-to", links["assert-relation-003"]["relationType"])
        self.assertNotIn("задаёт норму", specification_order["claimText"].lower())
        self.assertNotEqual("normative-basis", links["assert-relation-003"]["relationType"])
        self.assertEqual("seminar1_toir_notes.html#scheme-repair-order", links["assert-relation-004"]["source"])
        self.assertEqual("seminar1_toir_notes.html#section-3-3", links["assert-relation-005"]["source"])

        editorial_hypothesis = assertions["assert-relation-007"]
        self.assertEqual("not-established", editorial_hypothesis["evidenceStatus"])
        self.assertFalse(editorial_hypothesis["publishable"])
        self.assertFalse(links["assert-relation-007"]["publishable"])

    def test_element_links_do_not_encode_as_is_output_as_an_action_input(self):
        assertions = {row["id"]: row for row in self.data["sourceAssertions"]}
        linked_assertions = {row["sourceAssertionId"] for row in self.data["elementLinks"]}
        self.assertEqual({"assert-element-analyst-elicit-requirements"}, linked_assertions)
        analyst_relation = assertions["assert-element-analyst-elicit-requirements"]
        self.assertIn("#analyst-work", analyst_relation["locator"])
        self.assertIn("table row «Аналитик»", analyst_relation["locator"])
        self.assertNotIn("assert-element-as-is-model", assertions)

    def test_contrast_cases_preserve_non_equivalent_domain_levels(self):
        data = self.data
        terms = {term["id"]: term for term in data["terms"]}

        # Normative operation vs record of a concrete production operation.
        self.assertNotEqual(terms["tekhnologicheskaya-operatsiya"]["kind"], terms["proizvodstvennaya-operatsiya"]["kind"])
        # Normative specification stage vs an order-specific document stage.
        self.assertNotEqual(terms["etap-v-spetsifikatsii"]["kind"], terms["etap-proizvodstva"]["kind"])
        self.assertEqual("document", terms["etap-proizvodstva"]["kind"])
        # A repair order and its status describe a document/state, not a physical event.
        self.assertEqual("document", terms["zakaz-na-remont"]["kind"])
        self.assertNotEqual("event", terms["zakaz-na-remont"]["kind"])
        self.assertNotEqual("event", terms["status-dokumenta"]["kind"])

        links = data["links"]
        def matching_link(source, target):
            return [row for row in links if row["from"] == source and row["to"] == target]

        payment = matching_link("planiruemyi-platezh", "fakticheskii-platezh")
        self.assertTrue(payment, "planned and actual payment need an explicit comparison link")
        self.assertTrue(any("compar" in relation_semantics(data, row["relationType"]) or "сопостав" in relation_semantics(data, row["relationType"]) for row in payment))

        item_reference = matching_link("stroka-dokumenta", "zapis-spravochnika")
        self.assertTrue(item_reference, "document row references a reusable directory record")
        self.assertTrue(any("refer" in relation_semantics(data, row["relationType"]) or "ссыл" in relation_semantics(data, row["relationType"]) for row in item_reference))
        self.assertFalse(any("contain" in relation_semantics(data, row["relationType"]) or "содерж" in relation_semantics(data, row["relationType"]) for row in item_reference))

    def test_logistics_legacy_claims_are_not_published_from_stale_locator(self):
        terms = {term["id"]: term for term in self.data["terms"]}
        assertions = {row["id"]: row for row in self.data["sourceAssertions"]}
        affected = {
            "dostupnoe-kolichestvo", "inventarizatsiya", "logistika",
            "obespechenie-proizvodstva-materialami", "ostatok",
            "potrebnost-v-zakupke", "potrebnost-v-obespechenii", "rezerv",
            "sklad", "skladskaya-operatsiya",
        }
        stale = "Основные понятия, строка 27"
        for term_id in affected:
            term = terms[term_id]
            for definition in term.get("definitions", []):
                assertion = assertions[definition["assertionId"]]
                record = json.dumps([definition, assertion], ensure_ascii=False).lower()
                with self.subTest(term=term_id):
                    self.assertNotIn(stale.lower(), record)
                    self.assertNotIn("topic4_logistics_lecture.html#common-definitions", record)

        available = terms["dostupnoe-kolichestvo"]
        for definition in available.get("definitions", []):
            assertion = assertions[definition["assertionId"]]
            self.assertNotEqual("direct", assertion["evidenceStatus"])
            self.assertNotIn("свободное количество — это доступное количество", assertion["claimText"].lower())

        purchase = terms["potrebnost-v-zakupke"]
        for definition in purchase.get("definitions", []):
            assertion = assertions[definition["assertionId"]]
            source = next(row for row in self.data["sources"] if row["id"] == assertion["sourceId"])
            self.assertNotIn("topic4_logistics_lecture.html", json.dumps(source, ensure_ascii=False))
            self.assertNotIn("уже выбрало поставщика", assertion["claimText"].lower())

        material = terms["obespechenie-proizvodstva-materialami"]
        for definition in material.get("definitions", []):
            assertion = assertions[definition["assertionId"]]
            self.assertNotEqual("event", assertion["modality"])

    def test_manifest_matches_declared_course_sources_and_local_files(self):
        sources = self.data["meta"]["courseSources"]
        html = [item for item in self.manifest["corpus"] if item["format"] == "html"]
        self.assertEqual(19, len(sources))
        root_index = RootIndexHtmlLinks()
        root_index.feed((ROOT / "index.html").read_text(encoding="utf-8"))
        excluded_paths = {
            path
            for exclusion in self.manifest["exclusions"]
            for path in exclusion.get("paths", [])
        }
        # The only root-index student-facing canonical HTML source not yet
        # declared by meta.courseSources is the warehouse practicum.
        root_index_student_sources = root_index.paths - excluded_paths
        expected = set(sources) | {"topic4_warehouse_practicum.html"}
        self.assertEqual(expected, set(sources) | root_index_student_sources)
        self.assertEqual(expected, {item["path"] for item in html})
        self.assertEqual(len(html), len({item["path"] for item in html}))
        for item in html:
            with self.subTest(path=item["path"]):
                self.assertTrue(item["present"])
                self.assertTrue((ROOT / item["path"]).is_file())
                self.assertEqual("reviewed", item["reviewState"])

    def test_manifest_attachments_are_present_and_reviewed(self):
        attachments = {item["path"]: item for item in self.manifest["corpus"] if item["format"] != "html"}
        expected = {
            "assets/downloads/erp_concept_v8.pdf",
            "assets/downloads/Семинар 1_Драфт 14-10-23.pptx",
            "assets/downloads/Семинар 2_Драфт 21-10-23.pptx",
        }
        self.assertEqual(expected, set(attachments))
        for path, item in attachments.items():
            with self.subTest(path=path):
                self.assertTrue(item["present"])
                self.assertTrue((ROOT / path).is_file())
                self.assertEqual("reviewed", item["reviewState"])
                self.assertTrue(item["topic"])
                self.assertTrue(item["linkedFrom"])

    def test_reviewed_manifest_entries_have_complete_audit_registries(self):
        html = [item for item in self.manifest["corpus"] if item["format"] == "html"]
        attachments = [item for item in self.manifest["corpus"] if item["format"] != "html"]
        self.assertEqual(20, len(html))
        self.assertEqual(3, len(attachments))
        self.assertTrue(all(item["reviewState"] == "reviewed" for item in self.manifest["corpus"]))

        audits = ROOT / "ontology" / "source_audit"
        first = (audits / "html-01-10.md").read_text(encoding="utf-8")
        second = (audits / "html-11-20.md").read_text(encoding="utf-8")
        attached = (audits / "attachments.md").read_text(encoding="utf-8")
        self.assertIn("60 named candidates", first)
        self.assertIn("218 eligible relation source-statements", first)
        self.assertIn("**Total** | **13** | **119**", second)
        self.assertIn("216", attached)
        self.assertIn("148", attached)
        self.assertIn("30", attached)
        self.assertIn("38", attached)

    def test_public_source_audit_contains_no_local_filesystem_paths(self):
        audits = ROOT / "ontology" / "source_audit"
        forbidden = tuple(
            "/" + component + "/"
            for component in ("Users", "tmp", "private/tmp", "var/folders")
        )
        for path in sorted(audits.glob("*.md")):
            text = path.read_text(encoding="utf-8")
            with self.subTest(path=path.name):
                for marker in forbidden:
                    self.assertNotIn(marker, text)

    def test_rpd_crosswalk_baseline_and_navigation_inversion(self):
        crosswalk = self.data["meta"]["rpdCrosswalk"]
        self.assertEqual(7, len(crosswalk))
        by_number = {row["number"]: row["indexSection"] for row in crosswalk}
        self.assertEqual("topic-4", by_number[3])
        self.assertEqual("topic-3", by_number[4])

    def test_manifest_documents_scope_and_exclusions(self):
        self.assertIn("audited inventory", self.manifest["scope"].lower())
        self.assertIn("does not mean every claim was independently verified", self.manifest["completenessBoundary"].lower())
        categories = {item["category"] for item in self.manifest["exclusions"]}
        self.assertTrue(any("teacher-only" in item for item in categories))
        self.assertTrue(any("separate-discipline" in item for item in categories))
        self.assertTrue(any("private" in item for item in categories))
        self.assertTrue(any("redirect" in item for item in categories))
        excluded_paths = {
            path
            for item in self.manifest["exclusions"]
            for path in item.get("paths", [])
        }
        self.assertIn("topic4_warehouse_teacher_plan.html", excluded_paths)

    def test_builder_output_is_reproducible_without_touching_repository(self):
        # The builder is run in an isolated temporary ontology directory so
        # this test verifies its generated bytes without rewriting tracked JS.
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "ontology"
            target.mkdir()
            (target / "knowledge_ontology.json").write_bytes(ONTOLOGY_PATH.read_bytes())
            (target / "build_knowledge_ontology_bundle.py").write_bytes(
                (ROOT / "ontology" / "build_knowledge_ontology_bundle.py").read_bytes()
            )
            subprocess.run(
                ["python3", str(target / "build_knowledge_ontology_bundle.py")],
                cwd=tmp,
                check=True,
                capture_output=True,
                text=True,
            )
            built = (target / "knowledge_ontology_data.js").read_bytes()
        committed = (ROOT / "ontology" / "knowledge_ontology_data.js").read_bytes()
        self.assertEqual(committed, built)

    def test_erp_crosswalk_inventory_and_catalogue_structure(self):
        crosswalk = json.loads((ROOT / "ontology" / "erp_product_crosswalk.json").read_text(encoding="utf-8"))
        self.assertEqual("2026-11-23", crosswalk["checkedDate"])
        entries = crosswalk["erpFunctionality"]
        self.assertEqual(18, len(entries))
        self.assertEqual(list(range(1, 19)), [item["position"] for item in entries])
        ids = [item["id"] for item in entries]
        self.assertEqual(18, len(set(ids)))

        categories = crosswalk["catalogueCategories"]
        self.assertEqual(19, len(categories))
        category_ids = [item["id"] for item in categories]
        self.assertEqual(len(category_ids), len(set(category_ids)))
        by_level = {level: [item for item in categories if item["level"] == level] for level in ("top-level", "subcategory")}
        self.assertEqual(14, len(by_level["top-level"]))
        self.assertEqual(5, len(by_level["subcategory"]))
        for item in by_level["top-level"]:
            self.assertIsNone(item["parentId"])
        for item in by_level["subcategory"]:
            self.assertIn(item["parentId"], {parent["id"] for parent in by_level["top-level"]})

    def test_erp_crosswalk_limits_vendor_its_and_course_evidence(self):
        crosswalk = json.loads((ROOT / "ontology" / "erp_product_crosswalk.json").read_text(encoding="utf-8"))
        release = crosswalk["displayedProductRelease"]
        self.assertTrue(release["version"])
        self.assertIn("not evidence", release["interpretationLimit"].lower())
        allowed_status = set(crosswalk["statusVocabulary"])
        its_status = set(crosswalk["its26AccessStatuses"])
        classifications = {"functional_area", "integration", "inventory_planning_page", "functional_model", "inter_product_use"}
        for entry in crosswalk["erpFunctionality"]:
            with self.subTest(entry=entry["id"]):
                self.assertTrue(entry["vendorUrl"].startswith("https://v8.1c.ru/erp/"))
                self.assertIn(entry["classification"], classifications)
                mapping = entry["courseMapping"]
                self.assertIn(mapping["status"], allowed_status)
                self.assertIn(entry["its26"]["status"], its_status)
                if entry["its26"]["status"] != "no_defensible_page":
                    urls = [bookmark["url"] for bookmark in entry["its26"]["nearestBookmarks"]]
                    self.assertTrue(urls)
                    self.assertTrue(all("/db/erp26doc/" in url for url in urls))
                    self.assertFalse(any("erp25" in url.lower() or "2.5" in url for url in urls))
                if mapping["status"] != "direct":
                    self.assertTrue(mapping.get("gap"), "non-direct coverage needs an explicit gap")
                for evidence in mapping["evidence"]:
                    evidence_path = ROOT / evidence["path"].split("#", 1)[0]
                    self.assertTrue(evidence_path.is_file(), evidence["path"])
                    headings = HtmlHeadings()
                    headings.feed(evidence_path.read_text(encoding="utf-8"))
                    self.assertIn(evidence["heading"], headings.headings, f"heading mismatch: {evidence}")

    def test_erp_crosswalk_rpd_mapping_matches_ontology_metadata(self):
        crosswalk = json.loads((ROOT / "ontology" / "erp_product_crosswalk.json").read_text(encoding="utf-8"))
        ontology = self.data["meta"]["rpdCrosswalk"]
        expected = {
            row["number"]: (row["title"], row["indexSection"], row["materialStatus"])
            for row in ontology
        }
        actual = {
            row["rpdNumber"]: (row["rpdTitle"], row["indexTopic"], row["materialStatus"])
            for row in crosswalk["rpdTopicToIndexTopic"]
        }
        self.assertEqual(7, len(actual))
        self.assertEqual(expected, actual)

    def test_warehouse_map_links_both_practicums_and_scopes_read_only_claim(self):
        html = (ROOT / "ontology" / "index.html").read_text(encoding="utf-8")
        warehouse_branch = html.split('<h3>Склад, запасы и обеспечение</h3>', 1)[1].split('</article>', 1)[0]
        self.assertIn('href="../topic4_logistics_practicum.html">Практикум: обеспечение производства материалами', warehouse_branch)
        self.assertIn('href="../topic4_warehouse_practicum.html">Практикум: запасы и отгрузка', warehouse_branch)
        self.assertIn("Лекция + два практикума", warehouse_branch)
        self.assertIn("чтение подготовленного рабочего места, без проведения складской операции", warehouse_branch)
        self.assertIn("Отдельный складской кейс разбирает условные выписки", warehouse_branch)
        self.assertIn("студент не создаёт и не проводит складские документы", warehouse_branch)
        source = (ROOT / "topic4_warehouse_practicum.html").read_text(encoding="utf-8")
        self.assertIn("не означает физическое подчинение и не является инструкцией создавать эти документы в базе", source)
        self.assertIn("Студент не создаёт и не проводит инвентаризационные документы в общей базе", source)

    def test_crm_crosswalk_records_direct_lecture_definition_without_claiming_workflow(self):
        crosswalk = json.loads((ROOT / "ontology" / "erp_product_crosswalk.json").read_text(encoding="utf-8"))
        self.assertIn("functions or workflows in 1C:ERP", crosswalk["statusVocabulary"]["adjacent-only"])
        self.assertIn("may still define the concept", crosswalk["statusVocabulary"]["adjacent-only"])
        crm = next(row for row in crosswalk["erpFunctionality"] if row["id"] == "customer-relationship-management")
        self.assertEqual("adjacent-only", crm["courseMapping"]["status"])
        evidence = next(item for item in crm["courseMapping"]["evidence"] if item["path"] == "lecture1_student_guide.html#common-definitions")
        source = (ROOT / "lecture1_student_guide.html").read_text(encoding="utf-8")
        self.assertIn('id="common-definitions"', source)
        self.assertIn("CRM (Customer Relationship Management", source)
        self.assertIn("Общие понятия", source)
        self.assertEqual("Общие понятия", evidence["heading"])
        gap = crm["courseMapping"]["gap"].lower()
        self.assertIn("dedicated crm workflow", gap)
        self.assertNotIn("no direct crm content", gap)

    def test_ontology_metadata_references_the_g2_product_crosswalk(self):
        reference = self.data["meta"]["productCrosswalk"]
        crosswalk_path = ROOT / reference["path"]
        self.assertEqual("ontology/erp_product_crosswalk.json", reference["path"])
        self.assertTrue(crosswalk_path.is_file())
        crosswalk = json.loads(crosswalk_path.read_text(encoding="utf-8"))
        self.assertEqual(reference["checkedDate"], crosswalk["checkedDate"])
        self.assertEqual(reference["title"], crosswalk["title"])

    def test_corrected_its_26_toc_labels_remain_exact(self):
        crosswalk = json.loads((ROOT / "ontology" / "erp_product_crosswalk.json").read_text(encoding="utf-8"))
        entries = {entry["id"]: entry for entry in crosswalk["erpFunctionality"]}
        expected = {
            "monitoring-analysis": [("12. Отчеты и мониторинг", "ReportsAndMonitoring/ReportsAndMonitoring")],
            "international-financial-accounting": [("14. Международный финансовый учет", "IFRSAccounting/IFRSAccounting")],
            "regulated-accounting": [("16. Регламентированный учет", "RegulatoryAccounting/RegulatoryAccounting")],
            "cost-management-costing": [("11. Управленческий учет затрат и финансовый результат", "MAFinRes/MAFinRes")],
            "hr-payroll": [("20. Кадровый учет и расчет заработной платы", "HRM/HRM")],
            "repairs": [("9.13. Ремонты", "Repairs/Repairs")],
        }
        for entry_id, expected_bookmarks in expected.items():
            with self.subTest(entry=entry_id):
                actual = entries[entry_id]["its26"]["nearestBookmarks"]
                for title, path in expected_bookmarks:
                    matches = [bookmark for bookmark in actual if bookmark["title"] == title]
                    self.assertEqual(1, len(matches))
                    self.assertEqual(f"https://its.1c.ru/db/erp26doc/bookmark/{path}", matches[0]["url"])


if __name__ == "__main__":
    unittest.main()
