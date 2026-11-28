import json
import unittest
from pathlib import Path

from govcheck import vcs_provenance as provenance


DIGEST = "sha256:" + "a" * 64
BASE_DIGEST = "sha256:" + "b" * 64
GOV_DIGEST = "sha256:" + "c" * 64


class VcsProvenanceTests(unittest.TestCase):
    def git_args(self):
        return dict(
            repository_id="repo:12345",
            repository_uri="https://example.invalid/repo",
            target_ref="refs/heads/main",
            candidate_commit="c" * 40,
            candidate_content_digest=DIGEST,
            base_commit="b" * 40,
            base_content_digest=BASE_DIGEST,
            governance_scope_id="repo:example/project",
            governance_revision="gov-17",
            governance_digest=GOV_DIGEST,
            adapter_id="govcheck.git-pre-receive",
            adapter_version="1.0.0",
            observed_at="2026-11-28T12:00:00Z",
        )

    def pijul_args(self):
        return dict(
            repository_id="repo:12345",
            repository_uri="https://nest.pijul.com/example/project",
            target_channel="main",
            candidate_channel_hash="3WW3T5GBOOR3OCU2IDEVHHA7GGXMOHJDOYHCH7L5BWUGHUBHHQIQC",
            candidate_content_digest=DIGEST,
            base_channel_hash="5HWYGVSSDKMEQP43H3JDSURPS7FJB4TXMAGMUAKSKWIFH6QRZN3QC",
            base_content_digest=BASE_DIGEST,
            native_change_hashes=[
                "GBO3OSMXODHKWDCJRYG3SFVKZH6LZLHJY7L7VUPDQKXO2266P3EQC",
                "F5CAUHH7IA2QMSRPNMX7LDQLCMKJKKKEGGACTZ7OXTSHYPDE3WFAC",
            ],
            governance_scope_id="repo:example/project",
            governance_revision="gov-17",
            governance_digest=GOV_DIGEST,
            adapter_id="govcheck.pijul-remote",
            adapter_version="1.0.0",
            observed_at="2026-11-28T12:00:00Z",
        )

    def test_git_record_preserves_commit_and_full_ref(self):
        record = provenance.build_git_provenance(**self.git_args())
        self.assertEqual(record["vcs"]["kind"], "git")
        self.assertEqual(record["target"], {"kind": "ref", "name": "refs/heads/main"})
        self.assertEqual(record["candidate"]["nativeRevision"], "c" * 40)
        self.assertEqual(record["changeSet"]["nativeIds"], ["c" * 40])
        self.assertEqual(record["base"]["nativeRevision"], "b" * 40)

    def test_git_sha256_object_ids_are_supported(self):
        args = self.git_args()
        args["candidate_commit"] = "c" * 64
        args["base_commit"] = "b" * 64
        record = provenance.build_git_provenance(**args)
        self.assertEqual(len(record["candidate"]["nativeRevision"]), 64)

    def test_git_bootstrap_base_is_explicit_null(self):
        args = self.git_args()
        args["base_commit"] = None
        args["base_content_digest"] = None
        record = provenance.build_git_provenance(**args)
        self.assertIsNone(record["base"])

    def test_pijul_record_preserves_channel_and_native_change_hashes(self):
        record = provenance.build_pijul_provenance(**self.pijul_args())
        self.assertEqual(record["target"], {"kind": "channel", "name": "main"})
        self.assertEqual(record["candidate"]["nativeRevision"], self.pijul_args()["candidate_channel_hash"])
        self.assertEqual(record["changeSet"]["nativeIds"], sorted(self.pijul_args()["native_change_hashes"]))
        self.assertEqual(record["vcs"]["kind"], "pijul")

    def test_pijul_change_set_digest_is_order_independent_set_digest(self):
        args = self.pijul_args()
        first = provenance.build_pijul_provenance(**args)["changeSet"]["digest"]
        args["native_change_hashes"] = list(reversed(args["native_change_hashes"]))
        second = provenance.build_pijul_provenance(**args)["changeSet"]["digest"]
        self.assertEqual(first, second)

    def test_rejects_git_uppercase_or_non_object_id(self):
        args = self.git_args()
        args["candidate_commit"] = "C" * 40
        with self.assertRaises(provenance.VcsProvenanceError):
            provenance.build_git_provenance(**args)
        args = self.git_args()
        args["target_ref"] = "main"
        with self.assertRaises(provenance.VcsProvenanceError):
            provenance.build_git_provenance(**args)

    def test_rejects_partial_base_binding(self):
        args = self.git_args()
        args["base_content_digest"] = None
        with self.assertRaises(provenance.VcsProvenanceError):
            provenance.build_git_provenance(**args)

    def test_rejects_duplicate_or_empty_pijul_change_set(self):
        args = self.pijul_args()
        args["native_change_hashes"] = ["same", "same"]
        with self.assertRaises(provenance.VcsProvenanceError):
            provenance.build_pijul_provenance(**args)
        args["native_change_hashes"] = []
        with self.assertRaises(provenance.VcsProvenanceError):
            provenance.build_pijul_provenance(**args)

    def test_rejects_unscoped_timestamp_and_invalid_digest(self):
        args = self.git_args()
        args["observed_at"] = "2026-11-28T12:00:00"
        with self.assertRaises(provenance.VcsProvenanceError):
            provenance.build_git_provenance(**args)
        args = self.git_args()
        args["governance_digest"] = "not-a-digest"
        with self.assertRaises(provenance.VcsProvenanceError):
            provenance.build_git_provenance(**args)

    def test_schema_is_valid_json_and_strict(self):
        schema_path = Path(__file__).resolve().parents[1] / "govcheck" / "formal" / "schemas" / "vcs-provenance-v1.schema.json"
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        self.assertEqual(schema["$id"], "urn:govcheck:schema:vcs-provenance:v1")
        self.assertFalse(schema["additionalProperties"])


if __name__ == "__main__":
    unittest.main()
