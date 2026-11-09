# Comparative landscape: GovCheck, gittuf, SLSA Source, Gemara, Privateer and Gerrit

**Status:** research comparison, not an architecture decision, adoption record or implementation claim. The comparison is based on the source records cited below and on the current design specifications in this repository.

## 1. Executive comparison

| System / model | Primary scope | What it contributes | What it does not replace in GovCheck |
|---|---|---|---|
| **GovCheck** (current design) | General repository governance across lifecycle, authority, change acceptance, assurance and VCS adapters | A repository-level normative model intended to describe intent, requirements, rules, properties, decisions, claims, arguments, evidence, verification and accepted risk; bootstrap and enforcement at a repository change boundary | It is currently a design/specification project. The repository does not yet establish that the proposed evaluator, adapters or enforcement boundary are implemented or formally verified. |
| **gittuf** ([R-112](../references.md#r-112)) | Git repository security and authenticated policy metadata | Cryptographic root of trust, delegated administrators and verifiable policy metadata over Git changes | General lifecycle governance, assurance-case semantics, arbitrary repository artefacts, and Pijul semantics |
| **SLSA Source Track** ([R-113](../references.md#r-113)) | Source provenance and source-control assurance | A vocabulary and assurance framework for how source revisions are created and protected, with attestable properties | Normative repository governance, authority/delegation across all governance domains, semantic correctness, or change-acceptance policy |
| **Gemara** ([R-114](../references.md#r-114)) | Governance, risk and compliance data models and schemas | Structured control catalogs, assessments and evidence vocabularies for GRC interoperability | GovCheck's repository lifecycle, VCS-neutral change identity, authority model and distinctions between tests, model checking and proof |
| **OpenSSF Privateer** ([R-120](../references.md#r-120)) | Plugin-based evaluation of security/compliance controls | Evaluator plugins, structured control catalogs, deterministic checks and a human-review path for unresolved evidence | Canonical governance authority, repository lifecycle, change acceptance or theorem proof |
| **Gerrit submit requirements** ([R-115](../references.md#r-115)) | Forge/code-review integration and submit gating | Configurable predicates for whether a reviewed change is submittable | Forge-neutral governance, cross-VCS lifecycle semantics, assurance arguments and general evidence provenance |

## 2. Complementarity rather than replacement

The strongest architecture is not to make GovCheck reimplement every adjacent system. It is to define the normative governance model and explicit contracts through which specialized systems can contribute evidence or enforce a subset of controls.

- **Governance authority:** GovCheck specifies which claims, rules, requirements, authorities and acceptance conditions apply to a repository. It must remain explicit about scope, applicability, exceptions, delegation and accepted risk.
- **Git-specific integrity:** gittuf may supply authenticated Git policy metadata and change-integrity evidence. A GovCheck Git adapter can consume or cross-check that evidence without making gittuf the universal authority. Pijul requires its own semantics and cannot be represented as Git commits.
- **Source provenance:** SLSA Source can inform source-repository expectations and attestations. It should be treated as a specialized assurance profile, not a full repository-governance framework. SLSA Build and source provenance remain distinct.
- **Control vocabulary:** Gemara can provide interoperable GRC concepts and schemas. A mapping must preserve GovCheck-specific authority, applicability, exceptions, VCS identity and assurance semantics rather than silently replacing the canonical model.
- **Control evaluation:** Privateer may be an optional evaluator for selected controls. Each result must retain plugin identity/version, control-catalog revision, inputs, outputs, evidence references, uncertainty and human-review state. An AI-assisted review is not proof.
- **Change gating:** Gerrit submit requirements, GitLab approval rules, Zuul/Bors and forge-native queues are integration mechanisms. GovCheck can map its acceptance predicate onto them, but the mapping must disclose platform-specific gaps and bypass assumptions.

## 3. Evidence and assurance mapping

| GovCheck concept | Candidate external contribution | Required boundary
|---|---|
| Source/revision identity and provenance | gittuf; SLSA Source; in-toto/VSA; Sigstore | Verify subject digest, signer/verifier identity, trust root, predicate type, resource scope and freshness. A signature or attestation proves neither the truth of the claim nor the correctness of the verifier. |
| Control definitions and categories | Gemara; OSPS Baseline; Security Insights | Preserve source version, control identifiers, applicability and mapping loss. A control catalog is not itself an assessment result. |
| Control execution and evaluation | Privateer; OPA/Rego; Cedar; CEL; Conftest; Kyverno | Preserve evaluator version, policy revision, inputs, deterministic result, unresolved state and evidence provenance. |
| Change integration and acceptance | Gerrit; GitLab approval rules; Zuul/Bors; forge-native merge queues | Evaluate the exact candidate integration state; distinguish approval, CI result, policy satisfaction and final authorized acceptance. |
| Assurance argument | SACM; GSN; Assurance 2.0; Eliminative Argumentation | Preserve claims, contexts, assumptions, strategies, evidence, counterevidence, defeaters and confidence rationale. A well-formed assurance graph is not automatically a sound argument. |

## 4. Distinctions GovCheck must preserve

1. **A test is testimony/evidence, not a theorem proof.** A passing test supports a bounded claim under its test assumptions and observed inputs.
2. **Model checking is model-validation evidence, not theorem proving.** Its result depends on the model, specification, explored state space and abstraction.
3. **A proof checked is not the same as a model checked.** The verifier, kernel, assumptions and trust boundary must be identified.
4. **An attestation is a signed statement by an identified producer/verifier.** It does not make the statement true or the producer trustworthy.
5. **A control catalog is not a policy decision.** Applicability, scope, exceptions, evidence freshness and authorized risk acceptance must be explicit.
6. **A forge's merge button is not the governance model.** The same normative acceptance predicate may need different adapters for GitHub, GitLab, Gerrit, local Git, other forges and Pijul.

## 5. Current conclusion

GovCheck's potential contribution is the layer above individual tools: a general-purpose, repository-resident governance authority and lifecycle model that can bind together intent, rules, changes, evidence, assurance arguments and acceptance decisions across different VCS and forge environments.

That contribution remains a design hypothesis until a narrow vertical slice demonstrates that a real repository rule can be evaluated deterministically, that a failing or unknown result blocks acceptance at the declared boundary, and that the resulting evidence is traceable and independently reviewable. No source listed here is selected as a mandatory GovCheck dependency by this comparison.

## 6. Sources

- [gittuf](../references.md#r-112)
- [SLSA Source Track](../references.md#r-113)
- [Gemara](../references.md#r-114)
- [Gerrit submit requirements](../references.md#r-115)
- [OpenSSF Privateer](../references.md#r-120)
- [OpenSSF Security Insights](../references.md#r-109) and [OSPS Baseline](../references.md#r-110)
- [SLSA Verification Summary Attestation](../references.md#r-121) and [Sigstore](../references.md#r-122)
- [Zuul and Bors](../references.md#r-132)
- [GitLab approval rules](../references.md#r-131)
- [Assurance argumentation and GSN](../references.md#r-129) and [R-134](../references.md#r-134)