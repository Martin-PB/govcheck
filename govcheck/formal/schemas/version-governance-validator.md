# Version-governance bundle validator

**Status:** experimental implementation proposal. It does not make Architectures 0017/0018 normative and is not connected to release publication or the current catalogue.

## Purpose

`scripts/validate-version-governance.py` checks relationships that the individual JSON Schemas cannot check across records. It uses only the Python standard library.

Input is a JSON bundle with this envelope:

```json
{
  "schemaVersion": 1,
  "revisions": [
    {
      "artifactId": "govcheck.example-contract",
      "revision": { "vcs": "git", "nativeId": "<exact-native-revision>" }
    }
  ],
  "decisions": [],
  "dependencies": []
}
```

- `revisions` is an explicit inventory of exact artifact revisions known to the caller. It is not inferred from artifact paths or version labels.
- `decisions` contains records conforming to `version-decision.schema.json`.
- `dependencies` contains records conforming to `dependency-edge.schema.json`.
- Revision identity currently compares `artifactId`, `vcs` and `nativeId`. Repository paths and content digests are additional provenance, not substitutes for the native revision identifier.

## Checks

The validator detects duplicate decision/edge/revision identities, missing candidate or previous revisions, orphan dependency endpoints, orphan dependency-impact references, inconsistent impact declarations, invalid authorized-decision shape/classification, invalid SemVer syntax, supersession references/cycles/scope mismatches, and multiple authorized decisions for the same artifact/contract/candidate revision.

A dependency marked `review-required`, `stale-invalid`, `superseded` or `revoked` is reported as stale rather than current. A decision cannot simultaneously call such an edge `unaffected`.

## Result states and exit codes

| State | Exit | Meaning |
|---|---:|---|
| `valid` | 0 | No detected cross-record inconsistency. This is not an authorization or assurance claim. |
| `invalid` | 1 | A structural or cross-record contradiction was detected. |
| `unknown` | 2 | No contradiction was detected, but a required external authority fact remains unresolved. |
| `stale` | 3 | A referenced dependency is explicitly not current. |

Errors take precedence over stale, and stale takes precedence over unknown. Every report contains a machine-readable scope declaration.

## Deliberate limits

The current bundle does **not** define an authority/delegation registry, a VCS object resolver, a semantic compatibility oracle, or an evidence-record contract. Therefore the validator never claims to establish:

- whether an authority was actually delegated the relevant subject scope;
- whether a named authorizer was entitled to act at the recorded time;
- whether a Git/Pijul revision exists or resolves to the asserted content;
- whether a MAJOR/MINOR/PATCH classification is semantically correct;
- whether a proof, test, assessment or other evidence remains fresh.

In particular, `unknown` for an authorized decision is intentional: a syntactically complete authority object is not proof of delegated authority. A future authority registry must be derived from the canonical governance authority model and its adoption process, not invented by this validator.

The tool does not perform JSON Schema Draft 2020-12 validation. Run an independently selected schema validator for the individual records. It also does not modify or migrate `formal/artifacts.json`, lifecycle records, or release manifests, and it is not wired into release acceptance.

## Local verification

From the repository root:

```sh
python3 -m unittest discover -s tests -p 'test_version_governance_validator.py' -v
python3 scripts/validate-version-governance.py path/to/version-governance-bundle.json --pretty
```

The test suite uses synthetic records only. A passing test suite demonstrates behavior of this implementation against those test cases, not conformance of GovCheck's governance model or authorization regime.
