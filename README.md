# micro-services

CM architecture micro-services

## Dossier

- api-auth: Generation de JWT (pas de vérifications) - SQLAlchemy
- auth-bdd: Utilisation de PostgreSQL comme SGBD.
- api-bibliotheque: Communique avec une BDD SQLite les données de la bibliothèque. Vérifie les token JWTF avant rêquetes.
- front-bibliotheque: Client des API "api-auth" & "api-bibliotheque".

## Workflow dev -

`docker compose watch`

> A chaque modification du code source (Python) synchronise la couche avec le container.