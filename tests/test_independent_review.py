import unittest

from govcheck.independent_review import (
    PREDICATE_TYPE, STATEMENT_TYPE, IndependentReviewError, build_statement,
    validate_predicate,
)


class IndependentReviewPredicateTests(unittest.TestCase):
    def inputs(self):
        return dict(
            repository_uri="https://github.com/example/project",
            candidate_revision="c" * 40,
            candidate_content_sha256="a" * 64,
            base_revision="b" * 40,
            governance_revision="gov-17",
            scope_id="repo:example/project",
            reviewed_on="2026-11-27T12:00:00Z",
            outcome="accepted",
            claims_reviewed=["claim:security", "claim:tests"],
            observations=["No blocking finding in declared scope."],
            limitations=["Review was limited to the declared scope."],
        )

    def test_builds_distinct_predicate_and_candidate_binding(self):
        statement = build_statement(**self.inputs())
        self.assertEqual(statement["_type"], STATEMENT_TYPE)
        self.assertEqual(statement["predicateType"], PREDICATE_TYPE)
        self.assertEqual(statement["subject"][0]["digest"]["sha256"], "a" * 64)
        self.assertEqual(statement["predicate"]["outcome"], "accepted")
        self.assertNotIn("reviewer", statement["predicate"])
        self.assertNotIn("reviewerId", statement["predicate"])

    def test_rejects_reviewer_identity_in_predicate(self):
        predicate = build_statement(**self.inputs())["predicate"]
        predicate["reviewer"] = "someone"
        with self.assertRaises(IndependentReviewError):
            validate_predicate(predicate)

    def test_rejects_invalid_digest(self):
        values = self.inputs()
        values["candidate_content_sha256"] = "z" * 64
        with self.assertRaises(IndependentReviewError):
            build_statement(**values)

    def test_rejects_naive_timestamp(self):
        values = self.inputs()
        values["reviewed_on"] = "2026-11-27T12:00:00"
        with self.assertRaises(IndependentReviewError):
            build_statement(**values)

    def test_rejects_empty_claim_set_and_unknown_outcome(self):
        values = self.inputs()
        values["claims_reviewed"] = []
        with self.assertRaises(IndependentReviewError):
            build_statement(**values)
        values = self.inputs()
        values["outcome"] = "pass"
        with self.assertRaises(IndependentReviewError):
            build_statement(**values)


if __name__ == "__main__":
    unittest.main()
