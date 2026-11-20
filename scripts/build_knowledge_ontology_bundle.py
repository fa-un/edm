#!/usr/bin/env python3
"""Build the classic-script data bundle used by knowledge_graph.html."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "knowledge_ontology.json"
TARGET = ROOT / "assets" / "knowledge_ontology_data.js"

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
for index, link in enumerate(data.get("links", []), start=1):
    missing = {link.get("from"), link.get("to")} - known_ids
    if missing:
        raise SystemExit(f"Ontology link {index} references unknown term ids: {', '.join(sorted(missing))}")
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
TARGET.write_text(
    "// Generated from assets/knowledge_ontology.json. Do not edit by hand.\n"
    f"window.KNOWLEDGE_ONTOLOGY_DATA = {payload};\n",
    encoding="utf-8",
)
