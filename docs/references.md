# External references

**Purpose.** This page is the thematic entry point to GovCheck's external bibliography. It helps readers find sources by the question or design domain they concern; it does not duplicate the source descriptions.

The detailed, numbered bibliography is maintained in the [governance, assurance and formal-methods register](references/governance-and-assurance.md) ([Français](references/governance-and-assurance.fr.md)). Each entry records its primary source, relevant concepts, use in GovCheck and limitations.

## Browse by domain

| Domain | What to look for | Detailed entries |
|---|---|---|
| Governance authority and separation of duties | Normative authority, responsibilities, access controls, separation of duties and secure-development obligations | R-01–R-03, R-11 |
| Assurance cases and safety arguments | Claims, arguments, context, assumptions and evidence; structuring assurance without confusing it with proof | R-04 |
| Formal methods and proof | TLA+, TLC, state-transition models, invariants, model checking and proof assistants | R-05, R-20 |
| Evidence, provenance and software supply chain | in-toto attestations, SLSA provenance, build integrity and scoped security-posture evidence | R-06–R-08 |
| Policy engines and authorization | Policy decision/enforcement separation, typed authorization and the limits of OPA/Cedar | R-09–R-10 |
| Governance metadata and catalogues | Typed metadata, relationships, lineage and catalogue patterns | R-17 |
| Schemas and interface contracts | JSON Schema structural validation and OpenAPI machine-readable interfaces | R-13, R-16 |
| Artifact identity, versioning and releases | SemVer's proper scope, immutable revisions, Git tags, releases and reproducible verification context | R-14–R-15, R-21 |
| Version-control semantics and collaboration | Git snapshots versus Pijul's patch graph, channels, conflicts and adapter boundaries | R-22 |
| Agent workflow systems assessed as fixtures | Source-pinned assessments of Writ and Privateer; neither is adopted as a GovCheck dependency or authority | R-18–R-19 |

## How to use the bibliography

- Start with the domain above, then consult the corresponding numbered entries in the detailed register.
- Follow the architecture-record mappings at the end of the detailed register to find where a source informs a specific GovCheck design decision.
- Prefer primary standards, publications, official documentation and pinned source revisions.
- Treat every source according to its evidence class. A standard, paper, product document, source tree, test result and model-checking report do not establish the same kinds of claims.
- Inclusion means relevance to the documented reasoning, not adoption, implementation, compatibility, approval or proof of conformity.
- Keep source-specific explanations and limitations in the detailed register; do not maintain duplicate bibliographic descriptions here.

## Related documentation

- [Detailed reference register](references/governance-and-assurance.md)
- [French thematic index](references.fr.md)
- [Architecture records](architecture/README.md)
- [VCS and collaboration adapter specification](specifications/0004-vcs-collaboration-contracts.md)
