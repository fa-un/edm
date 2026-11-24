"""Negative and publication-contract tests for the stdlib ontology validator."""

from __future__ import annotations

import copy
import json
from pathlib import Path
import tempfile
import unittest

from ontology.validate_knowledge_ontology import ROOT, validate_ontology


class OntologyValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = ROOT
        cls.data = json.loads((ROOT / "ontology/knowledge_ontology.json").read_text(encoding="utf-8"))
        cls.manifest = json.loads((ROOT / "ontology/source_corpus_manifest.json").read_text(encoding="utf-8"))

    def validate(self, data=None, manifest=None, root=None):
        return validate_ontology(
            data=copy.deepcopy(self.data if data is None else data),
            root=self.root if root is None else root,
            manifest_data=copy.deepcopy(self.manifest if manifest is None else manifest),
        )

    def copy_root_with_crosswalk(self, product: dict, destination: Path) -> Path:
        """Create a lightweight test root with symlinked inputs and an injected crosswalk."""
        for child in self.root.iterdir():
            target = destination / child.name
            if child.name != "ontology":
                target.symlink_to(child, target_is_directory=child.is_dir())
                continue
            target.mkdir()
            for ontology_child in child.iterdir():
                copy_target = target / ontology_child.name
                if ontology_child.name == "erp_product_crosswalk.json":
                    copy_target.write_text(json.dumps(product), encoding="utf-8")
                else:
                    copy_target.symlink_to(ontology_child, target_is_directory=ontology_child.is_dir())
        return destination

    def assert_issue(self, errors: list[str], fragment: str) -> None:
        self.assertTrue(any(fragment in error for error in errors), f"Expected {fragment!r}; got {errors!r}")

    def test_current_repository_passes_complete_publication_validator(self):
        self.assertEqual([], self.validate())

    def test_reviewed_html_count_must_match_source_manifest(self):
        data = copy.deepcopy(self.data)
        data["meta"]["pagesReviewed"] -= 1
        self.assert_issue(self.validate(data=data), "meta.pagesReviewed is stale")

    def test_material_availability_accepts_supported_vocabulary_only(self):
        data = copy.deepcopy(self.data)
        data["coverage"][0]["materialAvailability"]["status"] = "partial"
        self.assertEqual([], self.validate(data=data))
        data["coverage"][0]["materialAvailability"]["status"] = "absent"
        self.assert_issue(self.validate(data=data), "has invalid status")

    def test_coverage_locator_anchor_must_resolve(self):
        data = copy.deepcopy(self.data)
        assertion_id = data["coverage"][0]["materialAvailability"]["sourceAssertionId"]
        assertion = next(row for row in data["sourceAssertions"] if row["id"] == assertion_id)
        assertion["locator"] = "index.html#missing-topic-anchor, material section"
        self.assert_issue(self.validate(data=data), "references missing HTML anchor #missing-topic-anchor")

    def test_duplicate_namespace_id_is_rejected(self):
        data = copy.deepcopy(self.data)
        data["sources"][0]["id"] = data["terms"][0]["id"]
        errors = self.validate(data)
        self.assert_issue(errors, "ID namespaces term/source overlap")

    def test_dangling_method_assertion_reference_is_rejected(self):
        data = copy.deepcopy(self.data)
        data["methodPractices"][0]["sourceAssertionId"] = "assertion-does-not-exist"
        errors = self.validate(data)
        self.assert_issue(errors, "methodPractice")
        self.assert_issue(errors, "missing source assertion")

    def test_unknown_coverage_cannot_carry_evidence(self):
        data = copy.deepcopy(self.data)
        availability = data["coverage"][0]["materialAvailability"]
        availability["status"] = "unknown"
        availability.pop("sourceAssertionId", None)
        availability["evidenceIds"] = [data["sourceAssertions"][0]["id"]]
        errors = self.validate(data)
        self.assert_issue(errors, "unknown coverage topic 1 materialAvailability must not carry evidence")

    def test_non_unknown_coverage_needs_direct_coverage_assertion(self):
        data = copy.deepcopy(self.data)
        data["coverage"][0]["materialAvailability"] = {"status": "available", "evidenceIds": []}
        errors = self.validate(data)
        self.assert_issue(errors, "known coverage topic 1 materialAvailability requires direct evidence")

    def test_manifest_must_include_each_topic_linked_student_page(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["corpus"] = [row for row in manifest["corpus"] if row["path"] != "topic4_warehouse_practicum.html"]
        errors = self.validate(manifest=manifest)
        self.assert_issue(errors, "student-facing topic4_warehouse_practicum.html must be in the source corpus")
        self.assert_issue(errors, "unclassified local HTML link in topic-4")

    def test_teacher_page_must_be_explicitly_excluded(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["exclusions"] = [item for item in manifest["exclusions"] if "topic4_warehouse_teacher_plan.html" not in item.get("paths", [])]
        errors = self.validate(manifest=manifest)
        self.assert_issue(errors, "topic4_warehouse_teacher_plan.html must be excluded explicitly")

    def test_per_file_audit_counts_must_match_reconciled_report(self):
        manifest = copy.deepcopy(self.manifest)
        row = next(row for row in manifest["corpus"] if row["path"] == "topic4_sales_purchasing_lecture.html")
        row["auditCounts"]["relationStatements"] += 1
        errors = self.validate(manifest=manifest)
        self.assert_issue(errors, "per-file auditCounts do not match")

    def test_unregistered_candidate_must_be_explicitly_excluded(self):
        manifest = copy.deepcopy(self.manifest)
        row = next(row for row in manifest["corpus"] if row["path"] == "assets/downloads/erp_concept_v8.pdf")
        row["candidateExclusions"] = [item for item in row["candidateExclusions"] if item["auditCandidateId"] != "PDF-M02"]
        errors = self.validate(manifest=manifest)
        self.assert_issue(errors, "named candidate register mismatch")

    def test_local_source_anchor_must_exist(self):
        data = copy.deepcopy(self.data)
        data["sources"][0]["uri"] = "lecture2_student_guide.html#anchor-that-does-not-exist"
        errors = self.validate(data)
        self.assert_issue(errors, "references missing HTML anchor")

    def test_invalid_relation_direction_is_rejected(self):
        data = copy.deepcopy(self.data)
        data["links"][0]["direction"] = "target_to_source"
        errors = self.validate(data)
        self.assert_issue(errors, "term relation 1 has invalid direction")

    def test_crosswalk_evidence_heading_must_exist(self):
        data = copy.deepcopy(self.data)
        crosswalk_path = self.root / data["meta"]["productCrosswalk"]["path"]
        product = json.loads(crosswalk_path.read_text(encoding="utf-8"))
        product["erpFunctionality"][0]["courseMapping"]["evidence"][0]["heading"] = "A heading that is not in the source page"
        with tempfile.TemporaryDirectory(prefix="ontology-validator-") as temp_dir:
            root = self.copy_root_with_crosswalk(product, Path(temp_dir))
            errors = self.validate(data, root=root)
        self.assert_issue(errors, "heading locator not found")


if __name__ == "__main__":
    unittest.main()
