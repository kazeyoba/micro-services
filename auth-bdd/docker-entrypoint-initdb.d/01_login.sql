CREATE DATABASE web_lou_login;
GRANT ALL PRIVILEGES ON DATABASE web_lou_login TO admin;
\c web_lou_login;

CREATE TABLE "Utilisateur" (
  "NoUtilisateur" INTEGER NOT NULL,
  "NomUtilisateur" VARCHAR(255) NOT NULL,
  "PrenomUtilisateur" VARCHAR(255) NOT NULL,
  "EmailUtilisateur" VARCHAR(255) NOT NULL,
  "MotdepasseUtilisateur" TEXT NOT NULL,
  "Statut" VARCHAR(255) NOT NULL DEFAULT 'user'
);

ALTER TABLE "Utilisateur"
  ALTER COLUMN "NoUtilisateur" SET NOT NULL,
  ALTER COLUMN "NoUtilisateur" ADD GENERATED ALWAYS AS IDENTITY;

INSERT INTO "Utilisateur" ("NomUtilisateur", "PrenomUtilisateur", "EmailUtilisateur", "MotdepasseUtilisateur", "Statut") VALUES
('admin', 'admin', 'admin@admin.fr', 'admin', 'admin'),
('test', 'test', 'test@test.fr', 'test', 'user');