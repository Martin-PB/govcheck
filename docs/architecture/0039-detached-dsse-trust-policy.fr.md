# Architecture 0039 — Vérification DSSE détachée et politique de confiance épinglée

**Statut :** premier profil de fournisseur de vérification proposé pour l'issue #158. Il n'adopte ni PKI universelle, ni politique générale de gestion de clés, ni exigence normative de revue indépendante. **English:** [0039](0039-detached-dsse-trust-policy.md).

## 1. Objectif

La Spécification 0008 définit l'enveloppe in-toto Statement/DSSE et sa validation structurelle. La validité structurelle n'est pas l'authenticité d'une signature. Ce profil ajoute un vérificateur local facultatif de signatures Ed25519, en déléguant les opérations cryptographiques à un exécutable OpenSSL explicitement épinglé. C'est un fournisseur, pas une dépendance obligatoire de GovCheck.

## 2. Frontière de confiance

Le vérificateur consomme trois entrées distinctes :
1. une enveloppe DSSE détachée (potentiellement fournie par le candidat et donc non fiable) ;
2. un fichier de politique de confiance fourni hors bande, hors de l'arbre candidat, dont le digest exact en octets est épinglé par l'opérateur ;
3. une racine du candidat permettant de rejeter les chemins de politique, de clé et de vérificateur situés dans un contenu contrôlé par le candidat.

La structure de la politique est définie par le schéma [attestation-trust-policy-v1.schema.json](../../govcheck/formal/schemas/attestation-trust-policy-v1.schema.json). La politique épingle :
- l'identifiant et la révision de la politique ;
- le chemin et le SHA-256 de l'exécutable OpenSSL ;
- pour chaque clé, son key ID, l'algorithme Ed25519, le chemin et le SHA-256 de la clé publique ;
- un identifiant stable de principal et les rôles autorisés ;
- l'intervalle de validité et l'état de révocation de la clé.

Le digest de politique est transmis séparément au vérificateur. Une politique ne peut pas s'authentifier elle-même. Les clés publiques et l'exécutable OpenSSL sont également épinglés par leurs octets. L'opérateur doit protéger la politique et les fichiers de clés ; les contrôles de chemin/digest ne protègent pas contre un opérateur privilégié capable de changer le digest attendu ou le processus vérificateur.

## 3. Vérification de signature

Le vérificateur :
1. décode structurellement l'enveloppe DSSE et valide le Statement in-toto ;
2. vérifie le payload type exact et les liaisons attendues predicate type/candidat/politique ;
3. calcule le pré-encodage d'authentification DSSE v1 (PAE) sur les octets exacts du payload ;
4. résout chaque key ID de signature via la politique épinglée ;
5. vérifie les digests de la clé et de l'exécutable OpenSSL, la validité/révocation, le rôle requis et le principal requis facultatif ;
6. invoque la vérification Ed25519 OpenSSL sur les octets PAE, sans shell ;
7. ne retourne l'identité/rôle du signataire qu'après réussite cryptographique.

Key ID inconnu, OpenSSL indisponible, politique manquante, digest différent, algorithme non pris en charge ou données de confiance indisponibles donnent UNKNOWN/invalide, jamais PASS. Une enveloppe structurellement valide mais non signée/non fiable n'est pas une preuve de confiance.

## 4. Limites temporelles et identitaires

L'intervalle de validité de la clé est évalué selon l'horloge système courante du vérificateur. DSSE ne fournit ici aucun horodatage de signature fiable. L'horodatage d'évaluation contenu dans le Statement est une déclaration du signataire ; il ne prouve pas quand la signature a été créée. Une validation historique après expiration/révocation exige un horodatage fiable ou une politique d'archivage gouvernée séparément, hors périmètre.

Un key ID associé à un principal/rôle authentifie la possession de la clé privée correspondante selon la politique configurée. Il ne prouve pas l'identité réelle d'une personne, son emploi, sa disponibilité ou son indépendance. L'opérateur de la politique reste responsable de l'association clé-principal et de l'autorisation des rôles.

Le projet ne dispose actuellement que d'un seul contributeur. Le vérificateur ne doit donc pas fabriquer un second reviewer. L'affirmation de revue indépendante reste UNKNOWN tant qu'un principal authentifié réellement distinct, doté du rôle requis, ne fournit pas une attestation de revue détachée correspondante. Les clés synthétiques de test prouvent uniquement le mécanisme cryptographique.

## 5. Premier profil de fournisseur

- Algorithme : Ed25519 uniquement.
- Implémentation crypto : OpenSSL CLI pkeyutl ; aucune primitive cryptographique maison ni dépendance Python crypto.
- Politique de confiance et clés publiques : fichiers locaux contrôlés par l'opérateur, hors de la racine du candidat.
- Exécutable OpenSSL : chemin absolu et SHA-256 épinglés dans la politique.
- Key ID DSSE : recherche exacte dans la table ; aucune découverte implicite de clé.
- Rôles : chaînes explicites telles que independent-reviewer, verifier ou risk-authority ; l'appartenance à un rôle ne constitue pas à elle seule une décision GovCheck.
- États de sortie : verified, invalid, unknown.
- CLI : commande locale ; aucun appel réseau ni service hébergé.

Implémentation : [attestation_verify.py](../../govcheck/attestation_verify.py) et [schéma de politique de confiance](../../govcheck/formal/schemas/attestation-trust-policy-v1.schema.json). Ce fournisseur est facultatif. Si OpenSSL est absent ou ne correspond pas au digest épinglé, le résultat est UNKNOWN. D'autres fournisseurs/algorithmes pourront implémenter ultérieurement le même contrat de vérification.

## 6. Hors objectifs

Aucune chaîne de certificats X.509, PKI, Sigstore/Fulcio/Rekor, révocation en ligne, autorité d'horodatage fiable, service de génération/rotation de clés, séquestre de clés, quorum multi-signatures ou délégation automatique d'autorité n'est implémenté. Aucune clé privée n'est stockée dans le dépôt. Le constructeur structurel de attestation.py ne réalise aucune vérification cryptographique.

## 7. Références et documents liés

- [R-232 — OpenSSL pkeyutl](../references.fr.md#r-232)
- [R-233 — RFC 8032 EdDSA/Ed25519](../references.fr.md#r-233)
- [Spécification 0008 — Attestations d'assurance interopérables](../specifications/0008-interoperable-assurance-attestations.fr.md)
- [Issue #158 — Vérificateur DSSE détaché](https://github.com/Martin-PB/govcheck/issues/158)
- Liés : #44 attestations, #60 risque résiduel d'autorité unique, #155 journal canonique, #45 frontière d'acceptation.

**Ce profil authentifie une signature selon une politique de clés épinglée par l'opérateur. Il ne prouve ni l'identité humaine, ni une revue indépendante, ni la correction de l'autorité, ni un instant de signature fiable.**
