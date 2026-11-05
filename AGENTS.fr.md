# Instructions pour les agents de programmation

Ces instructions guident les contributeurs pendant le bootstrap ; elles ne prétendent pas que l'application des règles est déjà implémentée.

1. Gouverner le dépôt et son cycle de vie. Ne transformez pas GovCheck en sandbox d'agent ou passerelle d'appels d'outils.
2. N'introduisez aucun service hébergé, daemon ou serveur MCP obligatoire. L'interface principale visée est un petit exécutable local.
3. Les fondations formelles de gouvernance et d'assurance s'appliquent à tout dépôt, quelle que soit sa taille ; ne créez pas de niveaux d'assurance.
4. Git et Pijul sont des VCS de première classe et sémantiquement distincts. Préservez nativement patches, dépendances, canaux et conflits Pijul.
5. Séparez VCS, hébergement, collaboration et acceptation. Les usages locaux et les serveurs d'équipe sont dans le périmètre.
6. Ne présumez aucun langage, fournisseur CI, système de build ou gestionnaire de paquets. Ne déclenchez pas de CI hébergée sans autorisation explicite.
7. Préférez un noyau réduit, des profils déclaratifs et des adaptateurs étroits à un système dynamique de plugins ou une pile obligatoire importante.
8. N'affirmez jamais qu'un contrôle, model checking, preuve ou résultat de conformité a été exécuté sans preuve de son exécution et de sa portée.
9. Le futur modèle canonique de gouvernance lisible par machine sera l'autorité normative. Markdown ne doit pas devenir silencieusement une autorité concurrente.
10. Suivez la politique temporaire de docs/BOOTSTRAP_GOVERNANCE.fr.md jusqu'à son remplacement par le moteur canonique.

## Discipline de bootstrap

Inspecter avant de planifier ; planifier avant d'appliquer. Préserver le contenu existant. Consigner les décisions d'architecture en ADR, avec l'anglais par défaut et un pendant français. Ne choisir aucun langage, noyau formel, format de données, licence ou dépendance obligatoire sans décision explicite examinée. Rapporter les fichiers modifiés, la justification, les contrôles réellement exécutés, ceux qui ne l'ont pas été et les décisions restantes.

English: [AGENTS.md](AGENTS.md).