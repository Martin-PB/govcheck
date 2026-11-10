# Compte rendu de recherche : assurance sémantique et modèles quantitatifs de transition

**Statut :** compte rendu de recherche, pas une décision d'architecture adoptée. **Date :** 2026-11-10.

## Objectif

Ce document consolide les échanges sur les fondations sémantiques de GovCheck et sur la place des approches épistémiques, probabilistes, floues et à transitions d'états dans l'assurance. GovCheck est un système généraliste de gouvernance des dépôts, pas un cadre limité à la sécurité. Aucune norme, logique, assistant de preuve ou outil de model checking ne doit définir à lui seul toute son ontologie.

## 1. Relations sémantiques

Le modèle doit relier sans les confondre intentions, objectifs, besoins des parties prenantes, exigences, décisions, spécifications, propriétés, architecture, modèles, implémentations et assurance. Ces éléments forment un graphe typé, plusieurs-à-plusieurs et évolutif, pas une hiérarchie documentaire linéaire. Une décision peut traiter plusieurs exigences ; une propriété peut raffiner plusieurs objectifs ; un élément probant peut soutenir plusieurs affirmations ; un changement peut invalider des raisonnements ou éléments probants en aval. Les relations doivent préciser type, sens, justification, autorité, portée et applicabilité temporelle.

L'intention n'est pas l'unique source des exigences : droit, normes, contrats, besoins, observations opérationnelles, menaces, défauts, interfaces et contraintes d'interopérabilité peuvent aussi les générer. Un objectif n'est pas en soi un résultat observable ; une mesure ne prouve pas automatiquement l'atteinte d'un objectif.

## 2. Paysage externe étudié

Fondations candidates :

- **Cycle de vie et exigences :** ISO/IEC/IEEE 15288, 12207, 29148 et 15289.
- **Architecture et modélisation système :** ISO/IEC/IEEE 42010, SysML v2/KerML.
- **Exigences orientées objectifs :** KAOS, i*, GRL et Tropos.
- **Décisions et processus :** OMG DMN et BPMN.
- **Cas d'assurance :** SACM (cible d'ingénierie discutée : 2.4 Beta 1), GSN, ISO/IEC/IEEE 15026-2 et recherche Assurance 2.0.
- **Provenance et échange :** W3C PROV-DM/PROV-O, ReqIF, in-toto, SLSA, SPDX et CycloneDX.
- **Risque, sécurité et gouvernance IA :** NIST SP 800-160 Rev. 1, ISO/IEC 23894, ISO/IEC 42001 et NIST AI RMF.
- **Qualité et mesure :** ISO/IEC 25010 et Goal-Question-Metric (GQM).
- **Raisonnement sur les décisions et risques :** PEAK, à ne pas confondre avec SACM.

Ces sources sont complémentaires, pas interchangeables. SACM est un profil important d'assurance et d'interopérabilité, pas l'ontologie complète de GovCheck. La préservation sémantique complète et les échanges sans perte sont des objectifs importants pour l'import/export SACM.

Lacunes à approfondir : autorité organisationnelle et délégation ; logique déontique (obligation, permission, interdiction) ; théorie de la décision et arbitrage multicritère ; facteurs sociotechniques ; assurance des IA/agents ; validité temporelle, fraîcheur et invalidation.

## 3. Statut épistémique et justification

Le regroupement antérieur sous une dimension générique d'« incertitude » a été jugé insuffisant. Le concept de travail préféré est **statut épistémique et justification** (ou « connaissance et justification »). GovCheck doit exprimer ce qui est affirmé, pourquoi cela est accepté, ce qui le soutient ou le contredit, comment les éléments de soutien ont été produits, quelle conclusion est autorisée et quelles sont sa portée, sa fraîcheur et ses limites.

Le vocabulaire récupéré de travaux GovCheck antérieurs comprend Claim/Assertion, Hypothesis, Argument, ArgumentReasoning, AssertedInference, AssertedEvidence, Context, Observation, Indicator, Evaluation, Incident et Decision. Métadonnées associées possibles : force des éléments probants, confiance, provenance, portée temporelle, contre-arguments/réfutations, indécidabilité, inconnues, limites, hypothèses et risque résiduel accepté.

Tests, model checking et preuves sont distincts :

- Un **résultat de test** est un témoignage/élément probant sur une exécution dans des conditions spécifiées, pas une preuve de théorème.
- Le **model checking** analyse un modèle formel au regard de propriétés et peut produire un résultat de satisfaction ou un contre-exemple. Ses conclusions sont bornées par le modèle, sa sémantique, sa configuration et l'espace d'états exploré.
- Une **preuve formelle** est une dérivation vérifiée dans un système formel et sous ses hypothèses ; elle ne prouve pas automatiquement que la formalisation correspond à la réalité.
- Revues, inspections et observations de production produisent d'autres types d'éléments probants, chacun avec sa méthode et ses limites.

Ce sont des méthodes et types de résultats reliés aux affirmations et arguments, pas des sous-types d'incertitude. Une chaîne illustrative Observation → Hypothesis → Threat → Control → Evidence → Assertion → Argument → Decision → Accepted Risk est un motif possible, pas un workflow obligatoire.

Dimensions transversales candidates, sous réserve d'examen des recouvrements : statut épistémique/justification ; autorité/responsabilité ; provenance/traçabilité ; contexte/applicabilité ; temps/fraîcheur ; risque/incertitude ; méthode/conformité ; évolution/invalidation ; observation/mesure.

## 4. Probabilités et logique floue

La **probabilité** représente l'incertitude portant sur des événements, résultats ou paramètres. Les méthodes bayésiennes combinent informations a priori et observations, mais les hypothèses a priori, modèles de vraisemblance et dépendances comptent. Usages possibles : fiabilité, probabilité de défaillance, estimation du risque, données opérationnelles et analyse de sensibilité. Toute probabilité associée à une affirmation doit préciser événement, hypothèses conditionnelles, population, horizon, sources des données/paramètres, méthode d'estimation, dépendances et incertitude de l'estimation.

La **logique floue** représente l'appartenance graduelle à des concepts aux frontières imprécises (par exemple maintenabilité « faible/moyenne/élevée ») et peut aider à traiter des exigences vagues ou contradictoires. Un degré d'appartenance de 0,8 à « maintenabilité élevée » **n'est pas** une probabilité de 80 % que le produit soit maintenable. Fonctions d'appartenance, bases de règles et jugements experts doivent être justifiés et validés.

À distinguer : vérité et dérivation en logique classique/formelle ; probabilité d'événements/paramètres ; appartenance floue et imprécision linguistique ; arguments qualitatifs d'assurance. Ces approches peuvent coexister, mais les règles de combinaison/agrégation doivent être explicites. Pas de champ universel de confiance numérique ni de score global inexpliqué.

Recommandation provisoire : noyau générique pour affirmations, hypothèses, arguments, éléments probants, méthodes, résultats, limites et conclusions, avec profils/moteurs spécialisés optionnels pour les méthodes formelles, probabilistes, floues et qualitatives. Le noyau représente résultats et hypothèses ; l'évaluation spécialisée peut être déléguée. La question de savoir si GovCheck doit lui-même valider les hypothèses probabilistes/floues reste ouverte.

### Sources sur probabilité, logique floue et confiance dans l'assurance

- Graydon & Holloway, “An investigation of proposed techniques for quantifying confidence in assurance arguments,” *Safety Science* 92 (2017) : https://doi.org/10.1016/j.ssci.2016.09.014. La revue met en garde contre des résultats quantitatifs peu plausibles et une validation empirique insuffisante pour une recommandation générale en contexte critique.
- “A probabilistic model of belief in safety cases,” *Safety Science* 138 (2021), 105187 : DOI à vérifier avant intégration définitive au catalogue ; le DOI cité dans les échanges était https://doi.org/10.1016/j.ssci.2021.09.014. Exemple de réseau bayésien, pas une méthode universelle.
- NIST Engineering Statistics Handbook, évaluation bayésienne de la fiabilité : https://www.itl.nist.gov/div898/handbook/apr/section1/apr1a.htm.
- Johanyák & Zlatko (2025), “A comprehensive survey on Fuzzy logic applications in software requirements engineering” : https://doi.org/10.47833/2025.2.CSC.008.
- Yen, Tiao & Liu (1996), “A Systematic Tradeoff Methodology for Acquiring and Validating Imprecise Requirements” : https://doi.org/10.1109/FUZZY.1996.551766.
- Salako & Zhao (2023), “The Unnecessity of Assuming Statistically Independent Tests in Bayesian Software Reliability Assessments” : https://doi.org/10.1109/TSE.2022.3233802.
- Salako & Zhao (2024), “Demonstrating Software Reliability using Possibly Correlated Tests” : https://doi.org/10.1002/qre.3460.
- NIST, “Software Assurance Using Structured Assurance Case Models” : https://pmc.ncbi.nlm.nih.gov/articles/PMC4548534/.

## 5. Machines à états finis, transitions pondérées et modèles de Markov

Ces familles sont pertinentes, mais la sémantique du poids d'une transition doit être explicite.

- **Machine à états finis / système de transitions :** définit états possibles et transitions autorisées ; peut être déterministe ou non déterministe, sans être probabiliste.
- **Chaîne de Markov à temps discret (DTMC) :** la distribution de l'état suivant dépend de l'état courant ; les probabilités sortantes forment une distribution.
- **Chaîne de Markov à temps continu (CTMC) :** transitions décrites par des taux, pas par des probabilités directes pour un pas fixe ; unités et sémantique temporelle comptent.
- **Processus de décision markovien (MDP) :** combine choix d'actions/non-déterminisme et transitions probabilistes, pour analyser des stratégies.
- **Automates probabilistes temporisés / modèles hybrides :** ajoutent horloges, contraintes temporelles ou variables continues.

La propriété de Markov est une hypothèse : l'état courant doit contenir assez d'information pour déterminer la distribution conditionnelle de l'état suivant. Si l'historique compte, il faut l'encoder dans l'état ou choisir une autre famille de modèles.

Un poids numérique sur une arête n'est pas nécessairement une probabilité. Il peut représenter probabilité, taux de transition, coût, récompense/utilité, priorité/préférence ou fréquence empirique/paramètre estimé. Ces sémantiques ne sont pas interchangeables. Un taux n'est pas une probabilité ; un coût ne doit pas être normalisé comme une probabilité sans modèle explicite.

Usages possibles : fiabilité sur un horizon temporel ; atteignabilité/probabilité d'états compromis ; transitions CI/CD entre proposition, vérification, rejet, déploiement et retour arrière ; états de maintenance ; trajectoires de gouvernance des agents ; probabilité d'un événement indésirable avant détection/mitigation. Les modèles d'autorisation et de gouvernance doivent d'abord exprimer les transitions permises et les autorités. Ajouter des probabilités seulement si comportement stochastique, fréquences empiriques, temps ou risque quantitatif le justifient.

Distinguer (1) l'aléa représenté par le modèle, (2) l'incertitude épistémique sur les probabilités/taux, et (3) l'imprécision linguistique sur les niveaux qualitatifs de risque. Les probabilités par intervalles et MDP à intervalles peuvent exprimer l'incertitude des paramètres et borner les résultats ; ce ne sont pas des degrés d'appartenance flous.

Un model checker peut établir un résultat quantitatif pour le modèle et les paramètres fournis, pas que le modèle représente fidèlement la réalité. L'assurance quantitative nécessite donc provenance des données/paramètres, justification du modèle, hypothèses, horizon, dépendances, sensibilité et limites. Le résultat est un élément d'un argument d'assurance, pas une garantie automatique sur le monde réel.

### Contrat générique candidat

Un contrat commun pour les modèles de transition pourrait décrire :

- `TransitionSystem` : états, état initial, transitions et invariants ;
- `TransitionSemantics` : déterministe, non déterministe, probabiliste, temporisé ou hybride ;
- `TransitionWeight` : valeur typée, unité, domaine, contraintes et interprétation ;
- `ParameterJustification` : provenance, observations, hypothèses, méthode d'estimation et période de validité ;
- `AnalysisSpecification` : propriété/objectif, horizon, hypothèses de stratégie/adversaire et sémantique d'analyse ;
- `AnalysisResult` : résultat, outil/version, configuration, bornes explorées, témoin/contre-exemple, limites et reproductibilité ;
- liens d'assurance des résultats vers affirmations, arguments, décisions et risques résiduels.

Ceci est conceptuel, pas un schéma adopté. Ne pas forcer automates, réseaux de Petri, chaînes de Markov et autres formalismes dans une représentation unique. Préférer un contrat commun pour sémantique, paramètres, analyse et provenance des résultats, avec profils propres aux domaines et formats natifs.

### Sources sur systèmes de transitions et model checking probabiliste

- Baier & Katoen, *Principles of Model Checking*, MIT Press (2008) : https://is.ifmo.ru/books/_principles_of_model_checking.pdf.
- Manuel officiel PRISM : https://www.prismmodelchecker.org/manual/Main/Introduction ; tutoriels : https://www.prismmodelchecker.org/tutorial/ ; études de cas : https://www.prismmodelchecker.org/casestudies/.
- Documentation UPPAAL, sémantique : https://docs.uppaal.org/language-reference/system-description/semantics/.

PRISM et UPPAAL sont des outils d'analyse candidats et implémentations de référence, pas des dépendances GovCheck ni des autorités normatives.

## 6. Orientations provisoires et questions ouvertes

Orientations de travail, pas encore une ADR :

1. Utiliser un graphe sémantique typé avec relations explicites, plusieurs-à-plusieurs et temporelles.
2. Garder le noyau indépendant d'une norme, logique, d'un model checker ou assistant de preuve particulier.
3. Représenter séparément témoignages, éléments probants, preuves formelles, résultats de model checking, observations et jugements experts, avec méthode et portée.
4. Préserver les distinctions entre probabilité, appartenance floue, non-déterminisme, taux de transition, coûts et récompenses.
5. Autoriser des profils/outils spécialisés sans rendre obligatoires preuve formelle, analyse probabiliste ou logique floue.
6. Préserver hypothèses, inconnues, éléments contradictoires, limites et risques acceptés plutôt que les masquer derrière un score.
7. Traiter normes et formats d'outils comme profils de domaine, pas comme le métamodèle GovCheck entier.
8. Relier toute conclusion calculée au modèle, paramètres, données, méthode, version d'outil et périmètre de validité.

Questions ouvertes : noyau ontologique minimal cohérent ; typage formel des relations intention/objectifs/besoins/exigences/décisions/spécifications/propriétés/modèles/implémentations/assurance ; représentation seule ou validation des hypothèses probabilistes/floues par le noyau ; sémantiques de transition de premier ordre ou profils d'extension ; distinction entre aléa, incertitude paramétrique/du modèle et imprécision floue ; comparaison de résultats issus d'abstractions, horizons, hypothèses et unités différents ; orthogonalité des dimensions transversales.

## 7. Statut des décisions

Ce compte rendu n'adopte aucune logique, norme, outil de model checking, assistant de preuve, sérialisation ou méthode de confiance quantitative particulière. Il préserve les échanges pour la prochaine étape de recherche académique/industrielle et de conception du métamodèle.
