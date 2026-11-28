# Exécution des contrôles fournis par un dépôt : recherche sur l'isolation et les limites de ressources

**Statut :** recherche de conception fondée sur les sources et contrat candidat ; ni politique d'exécution adoptée, ni implémentation de sandbox, ni certification de sécurité.  
**Date :** 2026-11-28. **Parent :** [Issue #218](https://github.com/Martin-PB/govcheck/issues/218).  
**English:** [Repository-controlled check execution](check-execution-isolation-2026-11.md).

## 1. Conclusion exécutive

GovCheck doit traiter les commandes de build, test, scan et génération contrôlées par le dépôt comme des **charges non fiables**, même lorsque leur code source appartient au dépôt candidat. L'évaluateur de confiance, la politique de confiance, les clés de signature, le superviseur du runner et l'adaptateur d'acceptation ne doivent partager ni l'autorité ni l'environnement inscriptible de la charge candidate.

Aucun mécanisme unique ne fournit toutes les propriétés nécessaires :

- **Landlock** ajoute des restrictions additives non privilégiées sur l'accès au système de fichiers. Ce n'est pas un mécanisme général de filtrage des appels système ou de contrôle des ressources.
- **seccomp** restreint les appels système et certains de leurs arguments. Ce n'est ni une politique de système de fichiers, ni une politique de sortie réseau, ni un quota CPU/mémoire.
- **cgroups v2** contrôlent la consommation CPU, mémoire, processus et E/S. Ils ne constituent pas une frontière de système de fichiers ou de confiance.
- **Les conteneurs OCI** configurent namespaces, cgroups, capacités, seccomp, LSM et contrôles du système de fichiers. Un conteneur ne garantit rien sans configuration effective et intégration hôte contraintes.
- **Le sandbox de build Nix** est utile pour isoler dépendances et builds, mais comporte des qualifications de plateforme et de mode d'exécution ; ce n'est pas un sandbox universel contre le code hostile.
- **Les VM hébergées éphémères et microVM** offrent une isolation plus forte pour des charges hostiles issues de dépôts publics, au prix d'un coût supérieur et de dépendances de déploiement supplémentaires. Une microVM nécessite encore des contrôles de sortie réseau côté hôte et un superviseur durci.

**Recommandation :** spécifier un contrat d'exécution indépendant des plateformes et des profils, et non un produit de sandbox obligatoire. Par défaut, GovCheck ne doit **pas exécuter** de commandes contrôlées par le candidat. Si un déploiement choisit de les exécuter, il doit sélectionner un profil et un backend déclarés, minimiser les identifiants, appliquer les frontières de ressources/réseau/système de fichiers et produire des éléments probants liés au candidat et à la politique exacts. Si la frontière requise ne peut être établie, le résultat est UNKNOWN ou NOT-RUN, jamais PASS.

## 2. Frontière de confiance et adversaire

La charge candidate peut être malveillante ou compromise via une modification de PR d'un script de test/build/scan, un hook de cycle de vie d'un gestionnaire de paquets, une dépendance compromise, un compilateur/plugin/runner de tests, une archive/symlink/submodule malveillant, un outil/runtime vulnérable ou une modification de workflow élargissant les permissions.

Supposer que la charge tente de :
1. lire des fichiers hôte, identifiants, variables d'environnement, sockets, services de métadonnées ou autres jobs ;
2. exfiltrer via DNS, HTTPS, sockets brutes, variables de proxy ou endpoints de dépendances ;
3. modifier l'évaluateur de confiance, la politique, les clés, la configuration du runner ou les références Git ;
4. persister via processus d'arrière-plan, caches, montages inscriptibles, espaces partagés ou réutilisation du runner ;
5. épuiser CPU, mémoire, PID, descripteurs de fichiers, disque, inodes, réseau, journaux ou stockage d'artefacts ;
6. falsifier/remplacer les preuves de sortie ou faire interpréter une sortie non fiable comme métadonnée de confiance.

La base informatique de confiance (TCB) doit être déclarée pour chaque profil. Elle peut inclure noyau hôte, hyperviseur, superviseur du runner, runtime de conteneur, système de fichiers, filtre réseau, constructeur d'image, chaîne d'outils, magasin de politiques et collecteur d'artefacts. Une revendication de sandbox sans TCB déclaré ni tests adversariaux n'est pas une affirmation d'assurance significative.

## 3. Comparaison des mécanismes

| Mécanisme | Propriétés utiles | Ce qu'il n'établit pas seul | Contrainte |
|---|---|---|---|
| Landlock Linux | Restrictions additives par processus, non privilégiées, sur le système de fichiers ; composition avec les contrôles existants. | Ne remplace ni filtrage des appels système, ni quotas, ni isolation des processus, ni politique réseau, ni frontière VM. | Dépend du noyau/ABI Linux ; vérifier l'ABI et construire des règles correctes. |
| seccomp-BPF Linux | Restreint l'entrée des appels système et peut inspecter numéros/arguments ; réduit la surface d'attaque du noyau. | N'exprime pas une sémantique générale de chemin, ne définit pas de quotas et ne filtre pas toute sortie réseau. | Spécifique à Linux ; différences d'appels système/architectures et correction du filtre importantes. |
| Namespaces Linux | Séparent certaines vues PID, montage, réseau, IPC, UTS, utilisateur et cgroup. | Un namespace omis peut être hérité ; les namespaces n'imposent pas de budgets CPU/mémoire. | Spécifique à Linux ; privilèges, montages et périphériques doivent être configurés correctement. |
| cgroups v2 | Quotas/poids CPU, plafonds mémoire, limites PID et comptabilisation/limitation E/S. | N'empêche pas de lire des fichiers hôte, d'utiliser des identifiants, d'ouvrir des connexions réseau ou d'attaquer le noyau. | Spécifique à Linux ; disponibilité des contrôleurs et hiérarchie parente importantes. |
| Runtime de conteneur OCI | Configuration standardisée des namespaces, cgroups, capacités, seccomp, LSM, système de fichiers racine et ressources. | Le mot « conteneur » seul ne prouve rien. Mode privilégié, montages/sockets hôte, réseau hôte, capacités larges ou namespaces hérités peuvent défaire l'isolation. | Noyau hôte et configuration runtime restent de confiance. |
| Sandbox de build Nix | Limite la visibilité des builds aux entrées déclarées du store, répertoires temporaires et chemins sélectionnés ; namespaces Linux isolent plusieurs vues. | Ne couvre pas toute commande arbitraire hors des builds Nix ; les derivations à sortie fixe peuvent nécessiter le réseau ; ne définit pas la sémantique des preuves GovCheck. | Le manuel documente Linux/macOS, l'exigence root et des valeurs par défaut dépendant de la plateforme. |
| VM hébergée éphémère | Worker neuf et état jetable ; sépare le code candidat du plan de contrôle persistant. | N'empêche pas l'exfiltration des données volontairement fournies ni ne compense des permissions de workflow dangereuses. | Image, cycle de vie, identifiants, réseau et artefacts propres au fournisseur. |
| MicroVM (ex. Firecracker) | Frontière de virtualisation matérielle avec petit invité ; peut être combinée à jailer, seccomp, namespaces et cgroups. | Ne supprime pas la confiance envers hôte/hyperviseur/superviseur ; la sortie réseau invitée doit être filtrée sur l'hôte. | Linux/KVM et intégration hôte privilégiée ; complexité opérationnelle supérieure. |

### 3.1 Un conteneur est une configuration, pas une politique

La spécification OCI rend explicites les contrôles pertinents : sélection des namespaces, placement cgroup, ressources mémoire/PID/CPU, capacités, seccomp, profils LSM, montages et périphériques. Un namespace omis peut hériter de celui du runtime. Un futur profil GovCheck doit donc enregistrer la configuration effective, pas simplement indiquer qu'un conteneur est utilisé.

Une socket de runtime, un conteneur privilégié, un bind mount hôte inscriptible, les namespaces PID/réseau hôte, un accès large aux périphériques ou un répertoire runner partagé inscriptible peuvent effondrer la frontière prévue.

### 3.2 La composition est une défense en profondeur, pas une preuve par accumulation

Un profil Linux peut combiner identité non privilégiée dédiée, namespaces privés, entrée candidat en lecture seule, scratch inscriptible borné, restrictions Landlock, filtre seccomp default-deny, limites cgroup v2, absence de capacités ambiantes/sockets hôte/identifiants et refus de sortie réseau imposé par l'hôte.

La composition dépend toujours du noyau, de la configuration des namespaces/montages, des descripteurs transmis à la charge, de la correction du superviseur et des besoins exacts de la chaîne d'outils. Chaque couche nécessite des tests négatifs. Une configuration multicouche n'est pas automatiquement un sandbox vérifié.

## 4. Profils d'exécution candidats

Ces profils sont proposés à la discussion, pas des exigences adoptées.

### P0 — Aucune exécution du candidat (par défaut)

- GovCheck n'invoque aucune commande contrôlée par le candidat.
- Il peut valider les métadonnées statiques et vérifier les preuves détachées produites par un système configuré indépendamment.
- Une preuve d'exécution manquante reste UNKNOWN ou NOT-RUN ; l'évaluateur ne doit pas inférer que les tests ont réussi.
- L'enregistrement identifie producteur externe, candidat exact, politique, vérificateur et digest du rapport.

Ce profil possède la plus petite TCB d'exécution GovCheck et devrait constituer le repli universel.

### P1 — Exécution locale restreinte (best effort, consentement explicite)

- Exécution uniquement après sélection explicite du profil par un opérateur.
- Aucun secret de dépôt, forge, signature ou cloud n'est hérité.
- Compte non privilégié, espace temporaire isolé, entrée candidat en lecture seule, scratch inscriptible borné, timeouts et nettoyage de l'arbre de processus.
- Sous Linux, Landlock + namespaces + seccomp + cgroups peuvent fournir une défense en profondeur ; ailleurs, backend explicitement nommé et limites documentées.
- Aucune revendication de confinement fort du code hostile sans réussite de la suite adversariale du profil/backend exact.

Utile au développement local, mais ne doit pas être promu silencieusement en frontière d'acceptation de production.

### P2 — Worker isolé éphémère (base recommandée lorsque du code candidat public doit être exécuté)

- Créer une VM/worker jetable neuf par candidat ou lot de confiance équivalente.
- Garder contrôleur de confiance, politique, clés de signature et vérificateur d'artefacts hors du worker.
- Ne fournir aucun secret au processus candidat ; utiliser un token en lecture seule et de moindre privilège uniquement si nécessaire, inaccessible aux étapes non fiables lorsque possible.
- Refuser la sortie réseau par défaut ; accès aux dépendances via proxy/cache contraint, liste d'autorisation explicite et exception enregistrée.
- Détruire worker et état inscriptible après collecte ; ne pas réutiliser de caches contrôlés par un candidat entre frontières de confiance.
- Lier le résultat au digest image worker, identité runner, candidat/base exacts, révision de politique, commande, profil effectif et digests d'artefacts.

La documentation GitHub distingue ses VM éphémères propres hébergées des runners auto-hébergés, pour lesquels une compromission persistante par des workflows non fiables est possible. C'est une affirmation du fournisseur sur son service, pas une garantie générique pour tout CI hébergé.

### P3 — Exécution isolée à haut risque (profil facultatif)

- Utiliser une microVM ou VM jetable d'isolation équivalente.
- Garder le superviseur hôte minimal et à jour, sous un profil jailer/moindre privilège.
- Appliquer le filtrage de sortie réseau côté hôte ; ne pas supposer que le réseau invité filtre le trafic sortant.
- Appliquer des quotas CPU, mémoire, processus et E/S par VM.
- Traiter la sortie invitée comme non fiable jusqu'à validation et hachage indépendants par le collecteur hôte.

Ce profil n'est pertinent que si le modèle de menace justifie sa complexité ; il ne doit pas être obligatoire pour chaque dépôt.

## 5. Contrat d'exécution : champs minimaux

Une future requête/attestation devrait lier :

| Groupe | Informations requises |
|---|---|
| Identité | ID d'exécution, identité du dépôt, révision/arbre/digest candidat, révision de base, référence cible et révision/digest de politique. |
| Commande | Identité/digest exécutable, argv, répertoire de travail, fichiers d'entrée, chaîne d'outils et identités des dépendances. |
| Environnement | Liste d'autorisation ou digest ; politique de secrets ; variables héritées refusées par défaut. Jamais de valeurs secrètes dans l'attestation. |
| Système de fichiers | Snapshot candidat, montages lecture seule/inscriptibles, flags, chemins autorisés, politique symlink, quota scratch et résultat du nettoyage. |
| Réseau | Mode désactivé/liste d'autorisation/proxy, politique DNS, identité du filtre de sortie, destinations et justification des exceptions. |
| Isolation | Backend/profil ID et version ; versions OS/noyau/hyperviseur/runtime ; namespaces, ABI/règles Landlock, digest seccomp, capacités et limites cgroup. |
| Budgets | Timeout mural, quota CPU, plafonds mémoire/swap, PID/threads, descripteurs, disque/inodes, octets réseau, stdout/stderr et taille d'artefacts. |
| Résultat | started/completed/failed/denied/not-run/timed-out/resource-exhausted/cleanup-failed ; code de sortie, raison, journaux bornés et digests. |
| Provenance | Identité runner/superviseur, digest image, révision de politique, horodatages et liaison signature/politique de confiance. |

Un échec d'infrastructure ne doit pas devenir une réussite de test. timed-out, resource-exhausted, cleanup-failed, runner-untrusted et incomplete doivent produire un UNKNOWN bloquant ou un échec explicite, jamais PASS.

## 6. Secrets et réseau

- **Aucun secret par défaut.** Les processus candidats ne doivent recevoir ni clés de signature, ni tokens d'écriture forge, ni identifiants de déploiement/cloud, ni identifiants runner persistants.
- **Étapes privilégiées séparées.** Une action post-contrôle nécessitant un identifiant s'exécute après la charge non fiable dans un job de confiance séparé avec permissions minimales.
- **Éviter les caches porteurs d'identifiants.** Ne pas réutiliser caches inscriptibles, home, identifiants de gestionnaire de paquets ou espaces de travail entre frontières de confiance.
- **Réseau deny-by-default.** Un namespace réseau n'est pas une politique de sortie. Appliquer le filtrage hôte/fournisseur ; considérer DNS, bypass proxy, sockets brutes et IPv6.
- **Exceptions de dépendances explicites.** Les téléchargements privés passent par un broker/proxy étroit ou un mécanisme n'exposant pas le secret brut à la commande candidate. Enregistrer destination, portée et expiration.
- **Sorties non fiables.** Limiter journaux/artefacts ; assainir secrets ; hacher les octets exacts ; parser avec schémas stricts ; ne jamais interpréter stdout arbitraire comme décision authentifiée.

## 7. Tests adversariaux requis avant toute revendication de sandbox

Un backend/profil doit avoir des tests positifs et négatifs couvrant :
1. lecture de /etc, /proc, home, répertoires SSH/GPG hôte et identifiants runner ;
2. traversée de symlinks, montages bind, hard links et chemins d'archives hors espace de travail ;
3. accès aux sockets runtime conteneur, périphériques, namespaces PID/réseau hôte et endpoints de métadonnées ;
4. exfiltration DNS, HTTPS, sockets brutes, IPv6 et bypass proxy ;
5. fork/thread bombs, boucle CPU, épuisement mémoire, disque/inodes, descripteurs et flood de sortie ;
6. processus d'arrière-plan, modification de caches partagés ou persistance après le job ;
7. modification de l'évaluateur, politique, clés, références ou preuves après exécution ;
8. archives malformées, normalisation de chemins, chemins Unicode et différentiels de parseurs ;
9. échec du nettoyage ou réutilisation du worker après terminaison anormale ;
10. falsification, remplacement ou rejeu d'une preuve issue d'un autre candidat, base, politique, image runner ou vérificateur.

Chaque résultat enregistre backend/profil exacts, versions OS/noyau/runtime, candidat, base, politique et révision de fixture. Un test réussi sur un backend ou une version de noyau ne prouve pas un autre profil.

## 8. Frontière d'architecture proposée

Séparer quatre rôles :

1. **Contrôleur de gouvernance/évaluateur :** interprète le profil d'exécution déclaré et décide si l'exécution est permise.
2. **Superviseur d'exécution :** provisionne le worker isolé, applique le profil et impose les budgets. C'est une infrastructure de confiance, pas du code candidat.
3. **Charge candidate :** commandes et dépendances non fiables ; ne reçoit que les entrées et capacités déclarées.
4. **Collecteur/vérificateur de preuves :** récupère les sorties bornées, les hache, vérifie la provenance et produit un enregistrement détaché lié au candidat/politique exacts.

Le contrôleur ne doit pas faire confiance à un fichier produit par le candidat qui affirme ses propres propriétés d'isolation. Le superviseur rapporte la configuration effective depuis l'extérieur de la charge ; le collecteur lie ce rapport indépendamment au candidat et à la politique. Si le superviseur ne peut attester un contrôle requis, le résultat est UNKNOWN.

## 9. Décisions encore ouvertes

- GovCheck orchestre-t-il l'exécution candidate, ou vérifie-t-il/enregistre-t-il seulement des preuves externes ?
- Quel profil est le minimum pour un dépôt qui choisit l'exécution ?
- Le réseau est-il toujours refusé par défaut, et comment les exceptions sont-elles autorisées ?
- Des secrets sont-ils jamais autorisés dans une charge candidate, ou seulement via un broker externe étroit ?
- Quel profil multiplateforme est significatif sans exagérer les contrôles exclusivement Linux ?
- Quelle identité de superviseur et quel format d'attestation sont de confiance ; comment gérer les mises à jour d'images runner/chaînes d'outils ?
- Si la plateforme ne peut imposer un contrôle demandé, faut-il refuser l'exécution, marquer un statut dégradé ou exiger une acceptation de risque ?

Aucune réponse n'est adoptée par ce rapport. L'issue #218 reste un candidat de conception.

## 10. Références

- [R-236 — Linux Landlock](../references.fr.md#r-236)
- [R-237 — Filtre seccomp Linux](../references.fr.md#r-237)
- [R-238 — cgroup v2 Linux](../references.fr.md#r-238)
- [R-239 — Configuration de runtime Open Container Initiative](../references.fr.md#r-239)
- [R-240 — Conception et sandboxing Firecracker](../references.fr.md#r-240)
- [R-241 — Utilisation sécurisée de GitHub Actions](../references.fr.md#r-241)
- [R-242 — Sandbox de build Nix](../references.fr.md#r-242)
- [Architecture 0006 — Modèle de menace et de confiance](../architecture/0006-threat-and-trust-model.fr.md)
- [Audit de couverture du modèle de menace](threat-model-coverage-audit-2026-11-28.fr.md)
- [Issue #218 — candidat d'isolation d'exécution](https://github.com/Martin-PB/govcheck/issues/218)
