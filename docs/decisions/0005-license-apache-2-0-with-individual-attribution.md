# ADR 0005 — Apache License 2.0 with individual attribution

**Status:** adopted; records the project owner's explicit decision of 2026-11-09 to license GovCheck under the Apache License, Version 2.0, with a NOTICE file attributing the work to Martin Pruvost-Beaurain as an individual. **French:** [0005 (français)](0005-license-apache-2-0-with-individual-attribution.fr.md).

## Context

The repository has had no license. The README stated that no permission to reuse, modify or redistribute its contents should be assumed, and Architecture 0007 and 0009 (D-12) left the license deliberately unselected pending an explicit decision. Issues #26 and #30 recorded the missing license as a blocker for adoption and contribution.

The owner's requirements are:

1. the most open terms possible, allowing both commercial and non-commercial use;
2. guaranteed attribution, as far as an open-source license can guarantee it;
3. attribution to the owner's own name as an individual, not to an organization.

Comparable governance and supply-chain projects predominantly use Apache 2.0 (gittuf, OpenSSF Scorecard, Allstar, Minder, OPA, Cedar, CUE, Gemara, Privateer, in-toto, Sigstore). MIT, BSD and ISC require only that the copyright notice be retained in copies of the source. Apache 2.0 additionally requires that the attribution notices of a NOTICE file be reproduced in every distribution of the Work or of Derivative Works (section 4(d)), and grants an explicit patent license.

## Decision

1. **License:** GovCheck is licensed under the Apache License, Version 2.0. The unmodified official text is in [LICENSE](../../LICENSE) (SHA-256 `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30`, retrieved from the official plain-text file listed in [R-108](../references.md#r-108)).
2. **Attribution:** the [NOTICE](../../NOTICE) file names **Martin Pruvost-Beaurain** as the individual copyright holder and creator. It must not be replaced by an organization name or by a generic "GovCheck contributors" line.
3. **Scope:** the license applies to the whole repository: code, scripts, TLA+ models, schemas, fixtures and documentation, unless a file states otherwise.
4. **Contributions:** inbound contributions are accepted under the same license (Apache 2.0, section 5). Contributors retain copyright in their contributions; the NOTICE attribution to the owner is preserved.

## Consequences

- Anyone may use, modify and redistribute GovCheck, commercially or not. Redistribution of the Work or of Derivative Works must include the LICENSE and the NOTICE attribution, and modified files must carry a change notice (section 4).
- Attribution is triggered by redistribution. Purely internal use, or use behind a network service without redistribution, does not oblige anyone to mention the owner. This is a known limit of every permissive open-source license, accepted here in favour of openness.
- Apache 2.0 does not grant trademark rights (section 6). Protecting the name "GovCheck" itself would require a separate trademark decision.
- Apache 2.0 is compatible with GPLv3 in one direction only and incompatible with GPLv2. GPL-licensed tools considered by GovCheck (Git, Pijul, Neo4j, the JDK) must therefore remain external programs invoked by GovCheck, never embedded or linked. LGPL and EPL components (Rocq, SysML v2 pilot) must not be copied into the GovCheck tree. OMG and ISO standards are referenced, not reproduced; W3C material, if reproduced, keeps its W3C notice in NOTICE.

## Out of scope (follow-up work)

This ADR does not yet:

- decide how LICENSE and NOTICE travel with the reusable **govcheck/** package when `govcheck/bootstrap.py` copies it into a governed repository. Copying the root LICENSE into a target repository root would wrongly impose GovCheck's license on the target project, so the package needs its own attribution location;
- add SPDX headers (`SPDX-License-Identifier: Apache-2.0`, `SPDX-FileCopyrightText: 2026 Martin Pruvost-Beaurain`) to individual files;
- add a dependency-license check to CI;
- add an attribution line to reports and attestations produced by GovCheck;
- select a contribution sign-off mechanism (for example the Developer Certificate of Origin).

## References

- [R-108 — Apache License 2.0 and GPL compatibility](../references.md#r-108).
- [Architecture 0007 — Technology decision framework](../architecture/0007-technology-decision-framework.md).
- [Architecture 0009 — Design discussion record](../architecture/0009-govcheck-design-discussion-record.md).
