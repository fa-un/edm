#!/usr/bin/env python3
"""Build the classic-script data bundle used by knowledge_graph.html."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "knowledge_ontology.json"
TARGET = ROOT / "assets" / "knowledge_ontology_data.js"

data = json.loads(SOURCE.read_text(encoding="utf-8"))
payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
TARGET.write_text(
    "// Generated from assets/knowledge_ontology.json. Do not edit by hand.\n"
    f"window.KNOWLEDGE_ONTOLOGY_DATA = {payload};\n",
    encoding="utf-8",
)
