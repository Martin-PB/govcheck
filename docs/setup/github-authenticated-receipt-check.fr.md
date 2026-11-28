# Activer le check GitHub de reçu authentifié

Ce guide configure la source de check fusionnée dans la PR #185. Il ne configure **pas** automatiquement la protection de branche. Le check est opt-in : sans `GOVCHECK_RECEIPT_CHECK_ENABLED=true`, les événements de PR neutralisent tout check en attente obsolète et les commentaires de reçu ne lancent pas la vérification.

## 1. Committer une policy de clés publiques de confiance

Créer un fichier JSON de trust-policy sur la branche protégée `main`, par exemple :

`govcheck/formal/github-pr-receipt-trust-policy.json`

Il doit respecter le schéma de trust-policy GovCheck existant et contenir :

- `schemaVersion: "1"` et `policyId: "urn:govcheck:trust-policy:v1"` ;
- une `revision` contrôlée par la gouvernance ;
- `openssl.path` comme chemin absolu d'exécutable et `openssl.sha256` comme SHA-256 brut sur 64 caractères hexadécimaux ;
- au moins une clé publique `ed25519` active avec `keyId`, `publicKeyPath`, `publicKeySha256`, `principalId` et le rôle requis `governance-authority` (ou un autre rôle configuré).

Seules les clés publiques sont dans le dépôt. Conserver la clé privée correspondante hors du dépôt en mode 0600. Épingler l'exécutable OpenSSL et le digest de chaque clé publique.

## 2. Définir les variables du dépôt

Utiliser le contexte GitHub CLI du dépôt (le vérifier avec `gh repo view`). Ce sont des **variables de configuration publiques**, pas des secrets :

```sh
gh variable set GOVCHECK_TRUST_POLICY_PATH --body "govcheck/formal/github-pr-receipt-trust-policy.json"
gh variable set GOVCHECK_TRUST_POLICY_SHA256 --body "$(sha256sum govcheck/formal/github-pr-receipt-trust-policy.json | cut -d' ' -f1)"

gh variable set GOVCHECK_JOURNAL_SCOPE_ID --body "<ID exact du scope de journal>"
gh variable set GOVCHECK_REPOSITORY_URI --body "<URI canonique exacte du dépôt>"
gh variable set GOVCHECK_GOVERNANCE_REVISION --body "<révision de gouvernance>"
gh variable set GOVCHECK_GOVERNANCE_DIGEST --body "sha256:<digest du package de gouvernance sur 64 hex>"
gh variable set GOVCHECK_EXPECTED_REPOSITORY_ID --body "<ID exact du dépôt utilisé par le gate>"
gh variable set GOVCHECK_EXPECTED_POLICY_DIGEST --body "sha256:<digest de la politique d'acceptation sur 64 hex>"

gh variable set GOVCHECK_REQUIRED_ROLE --body "governance-authority"
gh variable set GOVCHECK_PROTECTED_BASE_REF --body "main"

# Activer seulement après la policy de confiance, tous les pins et le ruleset requis.
gh variable set GOVCHECK_RECEIPT_CHECK_ENABLED --body "true"
```

Le scope du journal, l'ID/URI du dépôt, la révision/digest de gouvernance et le digest de politique d'acceptation doivent être exactement les mêmes que ceux utilisés par le gate local de confiance. Ne pas deviner ni substituer le digest de trust-policy au digest de gouvernance ou de politique d'acceptation.

## 3. Exécuter le préflight

Exporter localement les mêmes valeurs (ou les récupérer avec `gh variable get`) puis exécuter :

```sh
python scripts/validate-github-receipt-check-config.py --repository-root .
```

Le préflight vérifie les variables requises, le pin du fichier trust-policy, le pin de l'exécutable OpenSSL, les digests des fichiers de clés publiques et la présence d'une clé active pour le rôle requis. Le workflow de reçu de PR exécute ce même préflight avant la vérification de signature. Il n'expose aucun matériel privé.

## 4. Exiger le check dans le ruleset

Dans GitHub Settings du dépôt → Rules → Rulesets, configurer la branche de base protégée pour :

1. Exiger une pull request.
2. Exiger le check **GovCheck authenticated acceptance receipt**, provenant de GitHub Actions.
3. Exiger que la branche de PR soit à jour avant merge.
4. Restreindre les acteurs de bypass et les push directs vers la branche protégée.

Ne pas considérer le workflow comme enforcement tant que ce ruleset n'est pas actif. La source de check ne modifie pas elle-même les rulesets.

## 5. Soumettre un reçu

Dans la PR, publier un commentaire contenant la commande seule et l'enveloppe signée :

```text
/govcheck-receipt
```json
<enveloppe DSSE signée>
```
```

Seule une décision `pass` authentifiée, liée aux SHA actuels de tête/base et au digest de contenu exact, peut terminer le check avec succès. Les PR provenant de forks ne sont pas prises en charge par cet adaptateur initial.
