import unittest

from govcheck import attestation
from govcheck import forge_author_identity as identity


class ForgeAuthorIdentityTests(unittest.TestCase):
    def inputs(self):
        return dict(
            repository_uri="https://forge.example/org/repo",
            candidate_revision="c" * 40,
            candidate_content_sha256="a" * 64,
            base_revision="b" * 40,
            governance_revision="gov-17",
            scope_id="repo:org/repo",
            author_principal="forge:person-123",
            source_uri="https://forge.example/api/commits/c" + "c" * 39 + "/author",
            asserted_on="2026-11-27T12:00:00Z",
        )

    def test_builds_signed_source_claim_without_git_author_inference(self):
        statement = identity.build_statement(**self.inputs())
        self.assertEqual(statement["predicateType"], identity.PREDICATE_TYPE)
        self.assertEqual(statement["predicate"]["authorPrincipal"], "forge:person-123")
        self.assertEqual(statement["subject"][0]["digest"]["sha256"], "a" * 64)
        self.assertNotIn("gitAuthor", statement["predicate"])
        attestation.validate_statement(statement)

    def test_rejects_malformed_digest(self):
        values = self.inputs()
        values["candidate_content_sha256"] = "z" * 64
        with self.assertRaises(identity.ForgeAuthorIdentityError):
            identity.build_statement(**values)

    def test_rejects_naive_asserted_on(self):
        values = self.inputs()
        values["asserted_on"] = "2026-11-27T12:00:00"
        with self.assertRaises(identity.ForgeAuthorIdentityError):
            identity.build_statement(**values)

    def test_rejects_unknown_predicate_fields(self):
        predicate = identity.build_statement(**self.inputs())["predicate"]
        predicate["reviewer"] = "free-form"
        with self.assertRaises(identity.ForgeAuthorIdentityError):
            identity.validate_predicate(predicate)


if __name__ == "__main__":
    unittest.main()
