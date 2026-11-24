#!/usr/bin/env python3
"""Build the classic-script data bundle used by ontology/index.html."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "ontology" / "knowledge_ontology.json"
TARGET = ROOT / "ontology" / "knowledge_ontology_data.js"

data = json.loads(SOURCE.read_text(encoding="utf-8"))
terms = data.get("terms", [])
term_ids = [term.get("id") for term in terms]
if not all(term_ids) or len(term_ids) != len(set(term_ids)):
    raise SystemExit("Ontology terms must have unique, non-empty ids.")
known_ids = set(term_ids)
definition_entries = [definition for term in terms for definition in term.get("definitions", [])]
explicit_definitions = sum(bool(definition.get("explicit")) for definition in definition_entries)
expected_counts = {
    "distinctConceptNodes": len(terms),
    "sourceDefinitionEntries": len(definition_entries),
    "explicitDefinitions": explicit_definitions,
}
for key, actual in expected_counts.items():
    if data.get("meta", {}).get(key) != actual:
        raise SystemExit(f"Ontology meta.{key} is stale: expected {actual}.")
source_ids = [source.get("id") for source in data.get("sources", [])]
assertions = data.get("sourceAssertions", [])
assertion_ids = [item.get("id") for item in assertions]
if len(source_ids) != len(set(source_ids)) or not all(source_ids):
    raise SystemExit("Ontology sources must have unique, non-empty ids.")
if len(assertion_ids) != len(set(assertion_ids)) or not all(assertion_ids):
    raise SystemExit("Ontology sourceAssertions must have unique, non-empty ids.")
known_sources = set(source_ids)
known_assertions = set(assertion_ids)
for item in assertions:
    if item.get("sourceId") not in known_sources:
        raise SystemExit(f"Source assertion {item.get('id')} has a dangling source reference.")
    if not all(item.get(key) for key in ("claimType", "claimText", "locator", "modality", "evidenceStatus")):
        raise SystemExit(f"Source assertion {item.get('id')} is missing required claim/evidence fields.")
for term in terms:
    for definition in term.get("definitions", []) + term.get("legacyDefinitions", []):
        assertion_id = definition.get("assertionId")
        if assertion_id not in known_assertions:
            raise SystemExit(f"Term {term.get('id')} definition references unknown assertion {assertion_id}.")
        if definition.get("publishable") and not next(x for x in assertions if x["id"] == assertion_id).get("publishable"):
            raise SystemExit(f"Term {term.get('id')} publishes a non-publishable assertion.")
if set(source_ids) & (known_ids | set(assertion_ids)):
    raise SystemExit("Source, assertion, and term ID namespaces must be disjoint.")
if set(assertion_ids) & known_ids:
    raise SystemExit("Source assertion and term ID namespaces must be disjoint.")
if data.get("meta", {}).get("methodPracticeCount") != len(data.get("methodPractices", [])):
    raise SystemExit("Ontology meta.methodPracticeCount is stale.")
method_statuses = set(data.get("meta", {}).get("methodPracticeVerificationStatuses", []))
for method in data.get("methodPractices", []):
    assertion = next((row for row in assertions if row.get("id") == method.get("sourceAssertionId")), None)
    if not assertion or assertion.get("claimType") != "method_practice":
        raise SystemExit(f"Method/practice {method.get('id')} has no method_practice assertion.")
    if method.get("locator") != assertion.get("locator") or method.get("verificationStatus") not in method_statuses:
        raise SystemExit(f"Method/practice {method.get('id')} has an invalid locator/status.")
relation_types = {row if isinstance(row, str) else row.get("id") for row in data.get("meta", {}).get("relationTypes", [])}
for term in terms:
    if term.get("entityLevel") not in {"class", "instance", "not-applicable", "unknown"}:
        raise SystemExit(f"Term {term.get('id')} has invalid entityLevel.")
    if not isinstance(term.get("rpdTopics"), list) or any(topic not in range(1, 8) for topic in term["rpdTopics"]):
        raise SystemExit(f"Term {term.get('id')} has invalid RPD topic references.")
if data.get("meta", {}).get("sourceRecordCount") != len(source_ids):
    raise SystemExit("Ontology meta.sourceRecordCount is stale.")
if data.get("meta", {}).get("sourceAssertionCount") != len(assertion_ids):
    raise SystemExit("Ontology meta.sourceAssertionCount is stale.")
seen_relations = set()
for index, link in enumerate(data.get("links", []), start=1):
    if link.get("from") == link.get("to"):
        raise SystemExit(f"Ontology relation {index} is a self-link.")
    relation_key = (link.get("from"), link.get("to"), link.get("relationType"))
    if relation_key in seen_relations:
        raise SystemExit(f"Ontology relation {index} duplicates a typed relation.")
    seen_relations.add(relation_key)
    assertion_id = link.get("sourceAssertionId")
    assertion = next((row for row in assertions if row.get("id") == assertion_id), None)
    if not assertion or assertion.get("claimType") != "relation":
        raise SystemExit(f"Ontology relation {index} has no relation source assertion.")
    if assertion.get("evidenceStatus") != link.get("evidenceStatus"):
        raise SystemExit(f"Ontology relation {index} evidence status differs from its assertion.")
    if link.get("relationType") not in relation_types:
        raise SystemExit(f"Ontology relation {index} has an unknown relation type.")
    if link.get("direction") != "source_to_target":
        raise SystemExit(f"Ontology relation {index} has invalid direction.")
for index, link in enumerate(data.get("links", []), start=1):
    missing = {link.get("from"), link.get("to")} - known_ids
    if missing:
        raise SystemExit(f"Ontology link {index} references unknown term ids: {', '.join(sorted(missing))}")
for index, link in enumerate(data.get("elementLinks", []), start=1):
    source = link.get("from", {})
    target = link.get("to", {})
    if source.get("type") != "term" or source.get("id") not in known_ids:
        raise SystemExit(f"Element link {index} references unknown/wrong-type term source.")
    target_ids = {item.get("id") for key in ("actions", "functions") for item in data.get(key, [])}
    if target.get("type") not in {"action", "function"} or target.get("id") not in target_ids:
        raise SystemExit(f"Element link {index} references unknown/wrong-type action/function target.")
    assertion = next((row for row in assertions if row.get("id") == link.get("sourceAssertionId")), None)
    if not assertion or assertion.get("claimType") != "relation":
        raise SystemExit(f"Element link {index} has no relation source assertion.")
for row in data.get("coverage", []):
    for axis in ("materialAvailability", "deliveryStatus", "assessmentStatus"):
        status = row.get(axis, {})
        if status.get("status") == "unknown" and (status.get("sourceAssertionId") or status.get("evidenceIds")):
            raise SystemExit(f"Unknown coverage cannot cite evidence at topic {row.get('rpdTopicId')} {axis}.")
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
TARGET.write_text(
    "// Generated from ontology/knowledge_ontology.json. Do not edit by hand.\n"
    f"window.KNOWLEDGE_ONTOLOGY_DATA = {payload};\n",
    encoding="utf-8",
)
