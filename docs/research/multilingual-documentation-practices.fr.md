# Pratiques documentaires multilingues et modèles de synchronisation

**Statut :** étude comparative issue de l'issue #33 et du catalogue de références. Ce document consigne des options et contraintes ; il ne décide pas quelle langue fait autorité normative.

## 1. Pourquoi c'est une question de gouvernance

Pour GovCheck, une traduction peut être linguistiquement correcte tout en étant périmée par rapport à sa source. Inversement, une traduction synchronisée peut rester sémantiquement incorrecte. Ce sont des propriétés distinctes qui ne doivent pas être fusionnées dans un unique état « traduit » ou « valide ».

Le problème est plus important pour les documents consommés par des agents ou des outils. Si deux fichiers d'instructions opérationnelles expriment des obligations différentes, un agent peut suivre la mauvaise règle. Le dépôt doit donc distinguer explicitement l'autorité normative des vues localisées informatives.

## 2. Comparaison des pratiques sources

| Source / pratique | Unité de synchronisation | Mécanisme utile | Limite pour GovCheck |
|---|---|---|---|
| MDN translated-content ([R-136](../references.fr.md#r-136)) | Fichier | Marqueur de commit source tel que l10n.sourceCommit ; fraîcheur par rapport à la révision source | L'identité par commit est propre à Git ; adoption incomplète ; l'alignement source n'établit pas la qualité de la traduction. |
| Localisation Kubernetes ([R-137](../references.fr.md#r-137)) | Fichier/langue | Correction de la source en premier, triage humain, statut par langue et automatisation explicable | Certaines pratiques sont des prototypes ; ne tranche ni la primauté linguistique ni l'authenticité normative. |
| Guides de traduction Vue ([R-138](../references.fr.md#r-138)) | Dépôt / PR de traduction | Synchronisation amont, glossaire et diffs examinables | Workflow propre à une communauté, pas un modèle général de gouvernance. |
| Workflow de traduction React ([R-139](../references.fr.md#r-139)) | Dépôt/fork séparé | Écart amont explicite et PR de synchronisation | Maintenance du fork et alignement sur la source à valider indépendamment. |
| Comprehensive Rust / mdbook-i18n-helpers ([R-140](../references.fr.md#r-140)) | Segment | Fichiers PO, msgmerge, marqueurs fuzzy et obsolètes | Contraintes d'extraction/génération ; l'identité des segments peut ne pas correspondre aux identifiants stables des documents/records GovCheck. |
| po4a ([R-141](../references.fr.md#r-141)) | Paragraphe/segment | État fuzzy pour les segments sources modifiés ; traductions générées ; seuil configurable de complétude | Markdown structuré, ancres, blocs de code et identifiants normatifs demandent un traitement précis. |
| Docusaurus i18n ([R-142](../references.fr.md#r-142)) | Fichier/locale | Répertoires par locale et repli sur la langue source | Pas de suivi sémantique natif de fraîcheur ; des outils externes ou propres au projet sont nécessaires. |
| Proposition Microsoft de traduction comme artefact ([R-143](../references.fr.md#r-143)) | Artefact versionné | Séparer état de synchronisation et qualité linguistique ; rapporter l'état et laisser les jugements de qualité aux humains | Article/conception, pas preuve d'une implémentation complète en production. |
| BCP 47 ([R-144](../references.fr.md#r-144)) | Identifiant de langue | Balises normalisées langue/écriture/région | Identifie la langue uniquement ; ne définit ni primauté source, ni qualité de traduction, ni fraîcheur. |

## 3. Contraintes propres à GovCheck

- **Neutralité VCS :** les hashes de commits Git ne sont pas portables vers Pijul. Le marqueur de source d'une traduction peut nécessiter un digest de contenu ou un identifiant stable de record source, en conservant la révision VCS comme provenance supplémentaire.
- **Modèle canonique de gouvernance :** l'autorité structurée de gouvernance est destinée à être normative ; les documents Markdown sont des projections lisibles vérifiées par rapport à elle. Une vue Markdown traduite ne doit pas devenir silencieusement une seconde autorité.
- **Artefacts opérationnels et documentaires :** instructions d'agents, fichiers conventionnels de plateforme et configuration CI peuvent affecter le comportement des outils ; documents explicatifs, ADR et catalogues informent surtout les humains. Ils peuvent exiger des règles de primauté et de repli différentes.
- **Langue par défaut :** l'anglais est actuellement la langue par défaut du dépôt et une documentation française parallèle existe. Cela ne décide pas, à lui seul, si l'anglais est la seule version normative authentique ou si EN/FR sont co-authentiques.
- **Sorties indépendantes de la langue :** résultats exécutables, identifiants, codes d'état et attestations doivent rester indépendants de la langue ; les messages lisibles par l'humain peuvent être localisés.
- **Absence de dépendance hébergée :** les plateformes de traduction peuvent être des adaptateurs facultatifs, jamais un service hébergé obligatoire ni le cœur de gouvernance.

## 4. Décisions qui restent ouvertes

| Décision | Options possibles | Conséquence à spécifier |
|---|---|---|
| Primauté normative | Anglais faisant foi et français informatif ; EN/FR co-authentiques avec parité obligatoire ; autorité par type de document | Quel texte contrôle en cas de divergence, notamment pour les instructions d'agents et les spécifications normatives |
| Noms de fichiers opérationnels | Un seul fichier opérationnel canonique ; traductions informatives sous des noms non conventionnels | Éviter deux fichiers que les agents ou plateformes pourraient charger comme instructions concurrentes |
| Périmètre des traductions | Documentation destinée aux utilisateurs ; également ADR/spécifications/catalogue ; instructions opérationnelles ; messages/refus CLI | Quels artefacts exigent des métadonnées de traduction et des contrôles bloquants |
| Unité de synchronisation | Fichier entier ; section/record stable ; paragraphe/segment | Comment les changements de source invalident les traductions et comment préserver l'identité entre Git/Pijul |
| Marqueur source | Commit Git ; digest blob/contenu ; ID de record source stable plus digest | Comparaison reproductible malgré squash, renommage et migration VCS |
| Sémantique de péremption | Toute modification source ; seulement les changements normatifs ; classification normative/informative/éditoriale | Éviter de périmer une traduction pour une retouche éditoriale tout en manquant un changement normatif |
| Comportement si périmé/manquant | Avertissement ; repli explicite sur la langue faisant foi ; blocage des changements normatifs jusqu'à mise à jour | Politique fail-open/fail-closed selon la classe d'artefact |
| Revue de traduction | Revue humaine ; assistance machine avec relecteur explicite ; brouillon non relu | Qui peut attester la revue et ce que signifie cette attestation |
| Terminologie | Glossaire lisible par machine et alternatives interdites ; correspondance des mots-clés normatifs | Traductions stables de MUST/SHOULD/MAY et du vocabulaire métier |
| Langues supplémentaires | Balises BCP 47 et statut par langue | Ajouter une troisième langue sans refondre le modèle |

## 5. Modèle candidat (non adopté)

Une conception utile à évaluer consiste à représenter chaque artefact localisé comme un record dérivé avec :

1. une identité stable de l'artefact ou de la section source ;
2. une balise de langue (BCP 47) ;
3. un digest du contenu source et une révision VCS facultative ;
4. une révision/digest du contenu traduit ;
5. un statut tel que unknown, synchronized, stale, missing ou review-required ;
6. une méthode (humaine, assistée par machine, brouillon machine), un relecteur et une date de revue ;
7. une classification du changement (normatif, informatif, éditorial) ;
8. un lien vers la version faisant autorité et une déclaration explicite de statut normatif/informatif.

Ce modèle permet des contrôles déterministes de structure, identifiants, ancres, liens, blocs de code, nombres et digests source. Il ne prétend pas que l'équivalence sémantique ou la qualité linguistique sont décidables ; elles restent attestées par un humain ou inconnues.

## 6. Question de nommage ouverte

La discussion du projet utilise à la fois AGENTS.md et la convention préférée agent.md. Le nom canonique du fichier d'instructions opérationnelles doit être confirmé avant d'adopter une règle de traduction. Ne pas créer de fichiers opérationnels parallèles sous des noms que des agents pourraient charger automatiquement.

## 7. Plateformes mentionnées mais non évaluées

Weblate ([R-145](../references.fr.md#r-145)) et Crowdin ([R-146](../references.fr.md#r-146)) ont été mentionnés dans l'issue #33, sans évaluation au-delà de leur apparition dans la discussion Docusaurus. Ils sont conservés comme candidats non évalués, pas comme recommandations ou dépendances.

## 8. Sources

- [MDN translated-content](../references.fr.md#r-136)
- [Localisation Kubernetes](../references.fr.md#r-137)
- [Vue](../references.fr.md#r-138) et [React](../references.fr.md#r-139)
- [Comprehensive Rust](../references.fr.md#r-140), [po4a](../references.fr.md#r-141) et [Docusaurus](../references.fr.md#r-142)
- [Recommandations Microsoft sur les traductions comme artefacts](../references.fr.md#r-143)
- [BCP 47](../references.fr.md#r-144)
- [Weblate](../references.fr.md#r-145) et [Crowdin](../references.fr.md#r-146)