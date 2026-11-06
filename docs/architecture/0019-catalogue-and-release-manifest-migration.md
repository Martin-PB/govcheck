# 0019 — Artifact catalogue and release-manifest evolution

**Status:** proposed migration design. It depends on review/adoption of Architecture 0017 and 0018 and the record schemas in formal/schemas. No current catalogue or release format is changed.

## 1. Purpose

Architecture 0017 separates logical identity, immutable revision, optional contract version, release identity and event identity. Architecture 0018 defines authority and compatibility decisions. The version-decision and dependency-edge schemas provide proposed record shapes.

This record explains how to integrate those concepts into the artifact catalogue and release manifest without confusing the serialization versions of those records with the versions of the artifacts they describe.

## 2. Current baseline

The current formal/artifacts.json contains catalogueVersion: 1, a prose versioningPolicy object and an artifacts array. Its lifecycle-model entry has a stable artifactId, source/configuration/documentation paths, a repository-history revision policy and a release-tag/commit binding.

The current release-manifest schema declares schemaVersion: 1, binds a release tag and Git commit, and lists artifact paths, SHA-256 digests, roles and optional evidence metadata. It rejects unknown properties. The lifecycle transition registry separately declares schemaVersion: 1. These are format markers for different documents; equal numeric values do not couple their formats.

No current catalogue entry declares a contract version. Do not infer one from a Git tag, path, schema marker or repository release. A contract version requires the declaration and authorization conditions in Architecture 0017 §2.2 and Architecture 0018.

## 3. Four record responsibilities

1. **Artifact catalogue:** stable logical identity, kind, title, maintained paths, revision strategy and optional contract metadata.
2. **Version decision event:** append-only record of prior/candidate revisions, compatibility classification, authority and outcome.
3. **Dependency edge:** typed, directed relation between exact artifact revisions.
4. **Release manifest:** immutable publication index binding the release commit and exact artifact, evidence and governance-record bytes.

The catalogue is not an event log. Decision and dependency history must not be overwritten into mutable catalogue fields. The release manifest records what was published together; it does not approve versions.

## 4. Proposed catalogue entry

A future catalogue schema should require artifactId, kind, title, source/location paths, revisionPolicy and releaseBinding. An optional contract block may identify contract ID, scope, consumer classes, compatibility direction and the latest authorized decision record. It must not hold an independently editable SemVer value: the decision event is authoritative. A cached value is acceptable only if a validator proves it agrees with that event.

Dependencies remain in the separate typed edge registry; do not duplicate an untyped dependency list in every catalogue item.

Keep catalogueVersion: 1 unchanged while the current format is in use. It denotes the catalogue serialization/format revision, not the version of each artifact. Do not rename it to schemaVersion merely for naming consistency. A future breaking format change needs a deliberate schema and migration plan.

## 5. Release-manifest v2 boundary

The current manifest schema rejects additional properties. Adding contract references or governance records to v1 would therefore break strict consumers. Do not silently extend v1.

A future v2 should preserve the v1 core and add explicit digest-bound references for contract-bearing artifacts, version-decision records and dependency-edge records. It should distinguish the manifest format version from each artifact's contract version. A referenced decision must be included or immutably retrievable; dangling references and duplicate record IDs must be rejected.

Do not add a global SemVer for the repository release. The Git tag/commit remains the repository release identity; each contract-bearing artifact retains its own approved version.

## 6. Migration sequence

1. Adopt 0017/0018 through the canonical governance process.
2. Adopt the version-decision and dependency-edge schemas and define validator requirements.
3. Publish catalogue and manifest schemas before changing instances.
4. Implement readers for current and new formats; unknown major formats fail closed with an explicit unsupported-format result.
5. Add only IDs and metadata supported by repository evidence; invent no historical contract versions or approvals.
6. Add dependency edges only where exact endpoints and relation semantics are known; mark uncertainty review-required.
7. Create authorized baseline decisions when contracts are actually approved; do not backdate them.
8. Publish the first v2 manifest only when every referenced artifact and governance record is immutable and resolvable.
9. Retain v1 manifests and catalogue history unchanged. Migration creates new records; it does not rewrite old release evidence.

## 7. Validation requirements

A future validator should check unique stable artifact IDs; path/digest agreement with the pinned release; contract metadata linked to an authorized decision for the same artifact/revision; authority scope; resolvable dependency endpoints; unique and digest-bound governance records; no blocked/rejected/withdrawn/superseded decision used as current authorization; evidence freshness; and explicit format support.

These are structural and cross-record checks. Semantic compatibility, authority legitimacy and evidence validity still require governance/domain evaluation. Successful schema validation is not approval.

## 8. Deferred choices

This record does not choose a graph database, signature format, global release SemVer or automatic invalidation algorithm. It changes no current JSON file and implements no validator. The current catalogue is small; a separate edge registry and immutable decision records are sufficient for the first implementation.

## 9. Related records

- [Architecture 0017](0017-artifact-identity-revision-and-versioning.md).
- [Architecture 0018](0018-version-governance-and-compatibility-authority.md).
- [Formal schema inventory](../../formal/schemas/README.md).
- [Version-decision and dependency-edge record design](../../formal/schemas/version-governance-records.md).
- [Canonical Governance Model](../specifications/0002-canonical-governance-model.md).
- [Change Lifecycle and Acceptance](../specifications/0003-change-lifecycle.md).
- [Assurance, Claims and Evidence](../specifications/0005-assurance-model.md).
