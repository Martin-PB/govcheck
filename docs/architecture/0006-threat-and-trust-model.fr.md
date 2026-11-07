# Architecture 0006 — Modèle de menace et de confiance

**Statut :** proposition à examiner ; aucun contrôle de sécurité n'est implémenté. **English:** [0006](0006-threat-and-trust-model.md).

## 1. Actifs

Protéger : paquet canonique de gouvernance et historique ; contenu et identité exacte du dépôt ; changements et approbations ; preuves et provenance ; clés/signatures/identités ; binaires et configurations de l'évaluateur/adaptateurs ; décisions locales et distantes ; données privées et secrets rencontrés par les contrôles.

## 2. Objectifs de sécurité

- Intégrité : règles, états, preuves et décisions ne sont pas modifiés silencieusement.
- Authenticité/autorité : approbations et attestations sont attribuables à des acteurs autorisés.
- Liaison : chaque décision/preuve nomme dépôt, candidat et sémantique exacts.
- Fraîcheur : une preuve périmée n'autorise pas un candidat modifié.
- Disponibilité : épuisement de ressources ou adaptateur indisponible produit un blocage/indétermination explicite, jamais un faux succès.
- Confidentialité : ne pas recopier inutilement secrets et données privées dans rapports, journaux ou services distants.
- Auditabilité : les corrections ajoutent à l'historique sans effacer les événements antérieurs.

## 3. Adversaires et sources de défaillance

Considérer contributeur malveillant ou compromis, agent compromis, contenu de dépôt hostile, dépendance/outillage compromis, identité/clé falsifiée ou révoquée, forge/serveur d'équipe compromis, donnée externe périmée ou hostile, parseur/évaluateur/adaptateur défectueux, erreur opérateur, courses et échecs partiels. Ce sont des scénarios à étudier, pas une hypothèse uniforme sur tous les environnements.

## 4. Frontières de confiance

1. **Entrée normative :** modèle, schémas et profils canoniques. Le contenu du dépôt est non fiable avant analyse/validation.
2. **Évaluateur :** parseur, canonicalisation, moteur sémantique et résolution des règles constituent le TCB central.
3. **Contrôles :** scripts/builds/scanners du projet peuvent être hostiles et disposer de privilèges. Leur orchestration exige une politique d'exécution explicite ; une CLI locale ne rend pas arbitrairement du code sûr.
4. **Adaptateurs VCS :** interprétation de l'état et des conflits natifs, critique pour la sécurité.
5. **Producteurs/vérificateurs de preuves :** sortie d'outil, signatures, dates et faits externes ont des propriétés de confiance distinctes.
6. **Opérateur local :** un utilisateur ayant accès au système de fichiers ou des droits admin peut modifier les fichiers, désactiver hooks ou remplacer le binaire. L'application locale ne résiste pas à cet adversaire.
7. **Frontière d'acceptation partagée :** serveur d'équipe ou forge de confiance peut appliquer les décisions, sous réserve de ses administrateurs, identifiants et possibilités de contournement.
8. **Projections documentaires :** Markdown généré peut dériver ou être édité ; ce n'est pas une entrée normative.

## 5. Attaques principales et traitements requis

| Menace | Traitement requis / issue sûre |
|---|---|
| Affaiblir/supprimer une règle | IDs stables, diff sémantique révisable, historique, protection des changements de gouvernance |
| Règles ambiguës ou contradictoires | Détection déterministe ; échec fermé |
| Confusion de portée / masquage par profil | Portée et priorité partielle explicites ; fondations non affaiblissables |
| Expression de politique hostile | Préférer les données au code ; langage typé/borné si nécessaire ; aucune exécution arbitraire |
| Traversée de chemins / échappement par symlink | Racine explicite, chemins canoniques, rejet des échappements/ambiguïtés |
| Différences parseur/canonicalisation | Canonicalisation spécifiée, rejet des clés dupliquées/encodages ambigus, vecteurs inter-implémentations |
| Rejeu de preuve | Liaison à état, gouvernance, versions outils/évaluateur et dépendances exacts |
| Mutation après approbation | Réempreinter à l'application ; décision périmée |
| Approbation falsifiée | Identité authentifiée, contrôle d'autorité, cycle de vie/révocation des clés |
| Clé compromise | Révocation, rotation, invalidation des preuves et journal d'incident |
| Adaptateur VCS incorrect | Tests natifs ; inconnu/non supporté = indéterminé |
| Contournement de forge/admin | Déclarer capacités et contournements ; jamais prétendre à une application absolue |
| Script/dépendance de contrôle hostile | Frontière d'exécution explicite, limites de ressources, moindre privilège |
| Épuisement de ressources | Analyse/évaluation bornée, limites temps/mémoire, résultat incomplet explicite |
| Fuite de secrets dans journaux | Rédaction, minimisation, stockage local par défaut |
| TOCTOU / concurrence | Préconditions compare-and-swap et revalidation du candidat juste avant application |

## 6. Limites explicites

GovCheck seul ne peut empêcher un administrateur local de modifier les fichiers, remplacer le binaire ou contourner les hooks. Une signature ne prouve ni correction ni autorité sans identité et gouvernance des clés fiables. Un résultat de test ne prouve pas la sûreté du runner. Une barrière de forge ne protège pas d'un administrateur pouvant la désactiver sans contrôle indépendant. Aucune garantie d'inviolabilité, d'herméticité ou de zéro confiance n'est revendiquée.

## 7. Décisions avant implémentation

Définir sérialisation canonique et clés dupliquées ; isolation/limites de l'évaluateur ; modèle de clés, identité et approbation ; stockage/confidentialité des preuves ; exécution locale des contrôles ; protocole d'application distante et visibilité des contournements ; tests de sécurité ciblés. Ne pas laisser ces choix devenir des défauts implicites.


## Références bibliographiques

- [R-01 — contrôles NIST SP 800-53 de sécurité et de confidentialité](../references.fr.md#r-01)
- [R-02 — pratiques de développement sécurisé NIST SP 800-218](../references.fr.md#r-02)
- [R-06 — provenance de chaîne logicielle in-toto](../references.fr.md#r-06)
- [R-07 — assurance de chaîne logicielle SLSA](../references.fr.md#r-07)
- [R-27 — évaluation des risques NIST SP 800-30](../references.fr.md#r-27)
- [R-28 — ingénierie des systèmes dignes de confiance NIST SP 800-160](../references.fr.md#r-28)
- [R-29 — lignes directrices de gestion des risques ISO 31000](../references.fr.md#r-29)
- [R-30 — tactiques et techniques adverses MITRE ATT&CK](../references.fr.md#r-30)
- [R-31 — modélisation des menaces Microsoft SDL](../references.fr.md#r-31)
- [R-32 — méthode des arbres d'attaque de Schneier](../references.fr.md#r-32)
- [R-72 — modélisation des menaces à partir d'observations en production](../references.fr.md#r-72)
- [R-75 — surveillance continue de la sécurité NIST](../references.fr.md#r-75)
- [R-76 — certification à l'exécution et surveillance des hypothèses](../references.fr.md#r-76)
