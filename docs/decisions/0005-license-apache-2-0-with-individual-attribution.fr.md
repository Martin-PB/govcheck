# ADR 0005 — Licence Apache 2.0 avec attribution individuelle

**Statut :** adopté ; consigne la décision explicite du responsable du projet du 9 novembre 2026 de placer GovCheck sous la licence Apache, version 2.0, avec un fichier NOTICE qui attribue l'œuvre à Martin Pruvost-Beaurain en tant que personne physique. **Anglais :** [0005 (English)](0005-license-apache-2-0-with-individual-attribution.md).

## Contexte

Le dépôt n'avait pas de licence. Le README précisait qu'aucune permission de réutilisation, de modification ou de redistribution ne devait être présumée, et les architectures 0007 et 0009 (D-12) laissaient volontairement la licence ouverte en attendant une décision explicite. Les issues #26 et #30 signalaient cette absence comme un frein à l'adoption et aux contributions.

Les exigences du responsable du projet sont :

1. les conditions les plus ouvertes possibles, pour un usage commercial comme non commercial ;
2. une attribution garantie, dans la mesure où une licence open source peut la garantir ;
3. une attribution à son nom propre, en tant que personne physique, et non à une organisation.

Les projets comparables de gouvernance et de chaîne d'approvisionnement utilisent majoritairement l'Apache 2.0 (gittuf, OpenSSF Scorecard, Allstar, Minder, OPA, Cedar, CUE, Gemara, Privateer, in-toto, Sigstore). Les licences MIT, BSD et ISC exigent seulement de conserver la notice de copyright dans les copies du code source. L'Apache 2.0 exige en plus que les mentions d'attribution d'un fichier NOTICE soient reproduites dans toute distribution de l'œuvre ou d'une œuvre dérivée (section 4(d)), et accorde une licence de brevets explicite.

## Décision

1. **Licence :** GovCheck est placé sous la licence Apache, version 2.0. Le texte officiel, non modifié, se trouve dans [LICENSE](../../LICENSE) (SHA-256 `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30`, récupéré depuis le fichier texte officiel listé dans [R-108](../references.fr.md#r-108)).
2. **Attribution :** le fichier [NOTICE](../../NOTICE) désigne **Martin Pruvost-Beaurain** comme titulaire individuel du droit d'auteur et créateur. Ce nom ne doit pas être remplacé par celui d'une organisation ni par une mention générique du type « GovCheck contributors ».
3. **Périmètre :** la licence s'applique à tout le dépôt (code, scripts, modèles TLA+, schémas, fixtures et documentation), sauf mention contraire dans un fichier.
4. **Contributions :** les contributions sont acceptées sous la même licence (Apache 2.0, section 5). Les contributeurs conservent leurs droits sur leurs apports ; l'attribution du NOTICE au responsable du projet est maintenue.

## Conséquences

- Chacun peut utiliser, modifier et redistribuer GovCheck, à des fins commerciales ou non. Toute redistribution de l'œuvre ou d'une œuvre dérivée doit inclure la LICENSE et l'attribution du NOTICE, et les fichiers modifiés doivent porter une mention de modification (section 4).
- L'obligation d'attribution naît de la redistribution. Un usage purement interne, ou derrière un service réseau sans redistribution, n'oblige personne à mentionner le responsable du projet. C'est une limite connue de toutes les licences open source permissives, acceptée ici au profit de l'ouverture.
- L'Apache 2.0 n'accorde aucun droit sur les marques (section 6). Protéger le nom « GovCheck » lui-même relèverait d'une décision distincte de dépôt de marque.
- L'Apache 2.0 n'est compatible avec la GPLv3 que dans un sens, et ne l'est pas avec la GPLv2. Les outils sous GPL envisagés par GovCheck (Git, Pijul, Neo4j, le JDK) doivent donc rester des programmes externes appelés par GovCheck, jamais embarqués ni liés. Les composants LGPL et EPL (Rocq, pilote SysML v2) ne doivent pas être recopiés dans l'arborescence de GovCheck. Les normes OMG et ISO sont référencées et non reproduites ; les contenus W3C éventuellement reproduits conservent leur notice W3C dans le NOTICE.

## Hors périmètre (travaux à suivre)

Cet ADR ne traite pas encore :

- la manière dont LICENSE et NOTICE accompagnent le paquet réutilisable **govcheck/** quand `govcheck/bootstrap.py` le copie dans un dépôt gouverné. Copier la LICENSE racine à la racine d'un dépôt cible imposerait à tort la licence de GovCheck au projet cible : le paquet a besoin de son propre emplacement d'attribution ;
- l'ajout d'en-têtes SPDX (`SPDX-License-Identifier: Apache-2.0`, `SPDX-FileCopyrightText: 2026 Martin Pruvost-Beaurain`) dans chaque fichier ;
- l'ajout d'un contrôle des licences des dépendances en CI ;
- l'ajout d'une ligne d'attribution dans les rapports et attestations produits par GovCheck ;
- le choix d'un mécanisme de validation des contributions (par exemple le Developer Certificate of Origin).

## Références

- [R-108 — Licence Apache 2.0 et compatibilité avec la GPL](../references.fr.md#r-108).
- [Architecture 0007 — Cadre de décision technologique](../architecture/0007-technology-decision-framework.fr.md).
- [Architecture 0009 — Registre des discussions de conception](../architecture/0009-govcheck-design-discussion-record.fr.md).
