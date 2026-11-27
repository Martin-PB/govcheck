# Spécification 0009 — Attestations de revue indépendante détachées

**Statut :** contrat d'implémentation pour l'issue #160 ; proposé à la revue, sans nouvelle règle d'autorité ni affirmation qu'une revue indépendante réelle a eu lieu. **English:** [0009](0009-independent-review-attestations.md).

## 1. Objet et frontière

Définir un enregistrement de revue détaché et authentifié que GovCheck peut consommer sans traiter un nom de reviewer libre, une chaîne d'auteur Git, une signature seule ou un test synthétique comme preuve d'indépendance humaine.

L'enregistrement de revue est une preuve au sens d'élément probant. Il n'autorise pas lui-même une fusion, n'accepte pas un risque et ne modifie pas le modèle d'autorité de gouvernance. Tant qu'un seul contributeur est disponible, GovCheck doit continuer à signaler la revue indépendante comme indisponible/UNKNOWN.

## 2. Statement et prédicat

La revue est un Statement in-toto v1 utilisant le type de prédicat :

`urn:govcheck:attestation:independent-review:v1`

Le schéma JSON strict est `../../formal/schemas/independent-review-v1.schema.json`. Le prédicat lie :

- la révision candidate et le SHA-256 du contenu candidat ;
- la révision exacte de base ;
- la révision de gouvernance et l'identifiant de scope ;
- l'horodatage `reviewedOn` déclaré par le reviewer ;
- le résultat `accepted` ou `changes_requested` ;
- une liste non vide d'identifiants de claims examinés ;
- les observations et des limites non vides.

Le digest du sujet du Statement doit être égal à `candidateContentSha256`. Le prédicat ne contient volontairement aucun champ d'identité du reviewer.

## 3. Digest du contenu candidat

L'évaluateur calcule un SHA-256 déterministe du snapshot du checkout candidat. Les fichiers sont ordonnés par chemin POSIX relatif normalisé ; les répertoires et tout chemin contenant un composant `.git` sont exclus. Le payload d'un fichier ordinaire est son contenu exact en octets. Le payload d'un lien symbolique est le texte UTF-8 `symlink:` suivi de la cible du lien.

Pour chaque fichier, le flux de hachage reçoit une longueur non signée de 64 bits en big-endian puis les octets du chemin, suivis d'une longueur non signée de 64 bits en big-endian puis du payload. Le SHA-256 du flux obtenu est le digest du contenu candidat.

Le checkout doit être propre (fichiers suivis et non suivis) et `HEAD` doit être égal à la révision candidate complète. Sinon, la règle de revue indépendante ne peut pas réussir. Cela empêche d'attribuer à un commit différent une revue portant sur des fichiers supplémentaires du working tree.

## 4. Identité et confiance

Le principal du reviewer provient uniquement du signataire DSSE vérifié et de l'association key ID/principal/rôle de la politique de confiance épinglée par l'opérateur. Le rôle requis est `independent-reviewer`. Le principal reviewer authentifié doit être distinct du principal auteur.

Le principal auteur et l'URI de sa source sont des entrées explicites de l'évaluateur. La CLI n'authentifie **pas** elle-même l'API de forge ni l'URI source ; l'opérateur/le déploiement doit obtenir le principal auteur depuis un mécanisme d'identité de forge distinct et fiable. Les métadonnées d'auteur Git seules ne constituent pas un principal authentifié.

Le Statement d'assurance est lui aussi détaché et vérifié sous un rôle explicite de la politique de confiance. Son `independentReview.status` doit être `attested`, et son `independentReview.reference.digest.sha256` doit être égal au SHA-256 des octets exacts du fichier d'enveloppe de revue. Les deux enveloppes et la politique de confiance doivent se trouver hors de l'arbre candidat.

`reviewedOn` est une assertion signée du reviewer, pas une preuve d'horodatage fiable. Cette spécification ne crée aucune clé ni aucun compte reviewer de production.

## 5. Sémantique de l'évaluateur

- **PASS :** les enveloppes DSSE de revue et d'assurance sont vérifiées ; les rôles requis sont autorisés ; le reviewer est distinct de l'auteur ; toutes les liaisons candidat/base/gouvernance/scope/contenu correspondent ; l'assurance référence l'enveloppe exacte de revue ; le résultat est `accepted`.
- **FAIL :** signature/preuve mal formée ou invalide, liaison incorrecte, collision reviewer/auteur, digest de référence d'assurance incorrect ou `changes_requested`.
- **UNKNOWN :** preuve détachée, politique de confiance, rôle, révisions complètes, checkout candidat propre ou identité/source d'auteur indépendamment fiable manquants.

La règle est fail-closed. Une signature vérifiée authentifie le signataire du Statement ; elle ne prouve ni l'exhaustivité de la revue ni la justesse de ses affirmations.

## 6. Interopérabilité et limites

DSSE authentifie le type de payload et les octets exacts du payload via PAE. `keyid` n'est qu'un indice de recherche. L'association des rôles et principaux GovCheck reste une décision externe de politique de confiance.

Cette spécification ne définit ni temps fiable, ni cycle de vie des clés de production, ni authentification de l'API de forge, ni score de qualité de revue, ni décision d'autorité. Elle ne prétend pas que des tests synthétiques constituent une véritable revue par une seconde personne.

## Références

- [R-06 — in-toto](../references.fr.md#r-06)
