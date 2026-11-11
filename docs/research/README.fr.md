# Registre des recherches GovCheck

**Objet :** index durable des dossiers de recherche non normatifs susceptibles d'éclairer des décisions ultérieures. Ce registre n'est ni un backlog d'implémentation, ni un ensemble d'exigences adoptées, ni un registre de décisions prises.

## Mode d'emploi

Chaque dossier reçoit un **identifiant STUDY-ID** stable, indépendant du numéro de PR, de la branche, du nom de fichier ou de l'état actuel du produit. Une étude conserve :
- la ou les sources fournies par l'utilisateur et leur identité ;
- les questions de recherche et le périmètre ;
- les analyses des sources et les recherches complémentaires académiques, industrielles et normatives ;
- l'applicabilité à GovCheck, y compris la non-applicabilité et les prérequis externes ;
- les limites, contre-arguments, incertitudes et lacunes de recherche non résolues ;
- les liens vers les études liées, les entrées du catalogue, les architectures/spécifications/issues et les décisions ultérieures.

**La recherche ne vaut pas autorisation.** Une étude peut suggérer une question, révéler une lacune ou apporter des éléments ; elle ne crée pas d'obligation d'implémentation. Seule une décision explicitement autorisée peut adopter une recommandation. Ne pas transformer chaque étude en issue. Créer un dossier de décision uniquement lorsqu'un arbitrage est réellement demandé ou rendu.

### Procédure pour retrouver une étude

Lorsque l'utilisateur demande de reprendre une étude :
1. Résoudre l'identifiant STUDY-ID stable ou rechercher par titre de source, intervenant, URL, thème ou identifiant de référence.
2. Ouvrir le dossier complet et son évaluation d'applicabilité liée.
3. Réexaminer la source primaire et les références pertinentes si la question dépend de détails non conservés dans la synthèse.
4. Retrouver les dossiers de décision qui citent l'étude et indiquer si chaque source a été examinée, acceptée, rejetée ou laissée en suspens.
5. Garder les interprétations ultérieures distinctes de l'analyse originale ; ajouter une révision datée ou un lien de décision plutôt que réécrire silencieusement le raisonnement historique.

Lorsqu'une nouvelle étude est ajoutée, mettre à jour ce registre et les deux catalogues centraux de références. Lier l'étude depuis chaque entrée R pertinente, et lier les entrées R depuis l'étude. Préserver explicitement l'incertitude sur les sources.

## Catalogue des études

| Identifiant stable | Sujet de recherche | Dossier principal (FR) | Dossier principal (EN) | Statut décisionnel |
|---|---|---|---|---|
| STUDY-001 | Qualité du code assistée par IA, maintenabilité, TDD agentique et adoption organisationnelle | [Revue de recherche](ai-assisted-quality-governance.fr.md) | [Research review](ai-assisted-quality-governance.md) | Recherche uniquement ; aucune recommandation adoptée |
| STUDY-002 | Software factories, gouvernance de l'ingénierie IA et applicabilité de GovCheck | [Applicabilité de GovCheck](govcheck-applicability-and-boundaries.fr.md) · [Analyse de la conférence](software-factory-self-improvement.fr.md) | [GovCheck applicability](govcheck-applicability-and-boundaries.md) · [Conference analysis](software-factory-self-improvement.md) | Recherche uniquement ; aucune architecture de factory ni taxonomie d'audit adoptée |
| STUDY-003 | Épistémologie constructiviste, complexité irréductible et modélisation systémique (colloque Le Moigne en trois sessions) | [Dossier du colloque](le-moigne-colloquium.fr.md) · [Applicabilité à GovCheck](govcheck-applicability-constructivism-and-systems.fr.md) | [Colloquium dossier](le-moigne-colloquium.md) · [GovCheck applicability](govcheck-applicability-constructivism-and-systems.md) | Recherche uniquement ; aucune ontologie constructiviste/systémique adoptée |

## Thèmes transversaux

Ces thèmes servent à la navigation ; ils ne sont ni des concepts adoptés ni une taxonomie produit.

- **Connaissance, épistémologie et validité des modèles :** STUDY-003 ; à comparer avec le dossier de recherche sur le métamodèle/les ontologies et les spécifications d'assurance.
- **Intention, spécification, vérification et assurance :** STUDY-001 et STUDY-003.
- **Ingénierie assistée par IA et adéquation organisationnelle :** STUDY-001 et STUDY-002.
- **Frontières du dépôt et prérequis externes :** STUDY-002.
- **Complexité, incertitude, périmètre des modèles et risque résiduel :** STUDY-003 et STUDY-002.
- **Preuves, provenance et autorité décisionnelle :** toutes les études.

## Traçabilité des décisions

Les futurs dossiers de décision devront référencer :
- l'identifiant STUDY-ID stable ;
- les identifiants R exacts utilisés comme éléments ;
- les affirmations ou passages précis mobilisés (avec page/section/horodatage si disponibles) ;
- les contre-arguments et sources non retenus ;
- les limites de contexte et d'applicabilité ;
- l'autorité décisionnelle et la date ;
- le résultat adopté/rejeté/différé et sa justification ;
- les questions restantes qui relèvent encore de la recherche et non de l'implémentation.

Les PR liées constituent une provenance, pas des décisions :
- [PR #111 — Recherche sur la qualité et la gouvernance de l'ingénierie assistée par IA](https://github.com/Martin-PB/govcheck/pull/111) (STUDY-001).
- [PR #112 — Analyse software factory et applicabilité de GovCheck](https://github.com/Martin-PB/govcheck/pull/112) (STUDY-002).

Aucune décision ne doit être déduite du seul fait qu'une PR de recherche a été fusionnée.
