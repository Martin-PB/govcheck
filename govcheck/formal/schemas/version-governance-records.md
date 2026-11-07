# Version decision and dependency records

**Status:** proposed machine-readable contract, pending adoption of Architecture Records 0017 and 0018. These schemas are not yet normative and are not wired into a validator.

## Files

- `version-decision.schema.json` describes an immutable event proposing, authorizing, rejecting, blocking, withdrawing or superseding a contract-version decision.
- `dependency-edge.schema.json` describes a directed relation between two exact artifact revisions.

Both use JSON Schema Draft 2020-12. Their own `schemaVersion: 1` fields identify the serialized record format; they are not the contract version of the artifact being described.

## Design constraints

1. Every edge binds both endpoints to stable `artifactId` values and immutable native revision identities. Git and Pijul identities are both representable.
2. Contract versions are optional. Absence is not treated as version zero.
3. A version decision records classification, rationale, consumers, changed guarantees, dependency impact, actors, authority basis and provenance.
4. An authorized decision requires a previous state, proposed contract version, scope, proposer, authorizer and authority record. A structurally complete record still does not prove that the authority is legitimate or that the compatibility classification is correct.
5. `undetermined` is a first-class outcome for compatibility assessment, but cannot be authorized by the current schema condition.
6. Corrections and later decisions are linked through supersession; records are not overwritten.
7. Dependency relations are typed and directional. The graph may legitimately contain cycles for some relation classes; cycle policy must be relation-specific and is not asserted by JSON Schema.

## Relation orientation

`source` is the artifact making/holding the relation; `target` is the artifact it points to. Examples:

- A proof `verifies` a model property: source = proof/evidence, target = property/model claim.
- An implementation `conforms-to` a specification: source = implementation, target = specification.
- A release manifest `published-with` an artifact: source = release, target = artifact revision.
- A successor `supersedes` a prior artifact: source = successor, target = predecessor.

For `depends-on`, source is the dependent artifact and target is the dependency.

## Validation boundary

JSON Schema can check shape, required fields, enumerations, identifier syntax, digest syntax and some conditional requirements. It cannot establish:

- that an actor is authorized under the canonical governance model;
- that a claimed revision or digest exists or is immutable;
- that a MAJOR/MINOR/PATCH classification is semantically correct;
- that dependency impact is complete;
- that a proof or test remains valid after a dependency changes;
- that relation cycles are valid or invalid;
- that timestamps, signatures or external provenance are truthful.

A future evaluator must resolve these against pinned repository/governance state and explicit authority records. Unknown authority or unresolved compatibility must block authorization, not be defaulted to success.

## Deliberately deferred

This first schema increment does not mutate `formal/artifacts.json`, `formal/lifecycle-transitions.json` or the release-manifest schema. It does not invent contract versions for existing artifacts or retroactively create decision records. Catalogue migration should follow a reviewed compatibility plan after the record contracts and their validation tests are adopted.
