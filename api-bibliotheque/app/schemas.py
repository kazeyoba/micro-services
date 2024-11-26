from pydantic import BaseModel, Field
from typing import Optional

class Auteurs(BaseModel):
    id: Optional[int] = Field(None, description="Identifiant unique de l'auteur")
    nom_auteur: str = Field(..., description="Nom complet de l'auteur")

class Livres(BaseModel):
    id: Optional[int] = Field(None, description="Identifiant unique du livre")
    titre: str = Field(..., description="Titre du livre")
    pitch: Optional[str] = Field(None, description="Résumé ou pitch du livre")
    auteur_id: int = Field(..., description="Nom de l'auteur du livre")
    date_public: str = Field(..., description="Date de publication du livre (format YYYY-MM-DD)")
    emprunteur_id: Optional[int] = Field(None, description="Identifiant de l'utilisateur ayant emprunté le livre")

class Utilisateurs(BaseModel):
    id: Optional[int] = Field(None, description="Identifiant unique de l'utilisateur")
    nom_utilisateur: str = Field(..., description="Nom complet ou pseudo de l'utilisateur")

class CreateAuteur(BaseModel):
    nom_auteur: str = Field(..., description="Nom complet de l'auteur à ajouter")

class CreateLivre(BaseModel):
    titre: str = Field(..., description="Titre du livre à ajouter")
    pitch: Optional[str] = Field(None, description="Résumé ou pitch du livre")
    nom_auteur: str = Field(..., description="Nom de l'auteur du livre")
    date_public: str = Field(..., description="Date de publication du livre (format YYYY-MM-DD)")

class CreateUtilisateur(BaseModel):
    nom_utilisateur: str = Field(..., description="Nom complet ou pseudo de l'utilisateur à ajouter")
    
class DeleteAuteur(BaseModel):
    id: Optional[int] = Field(..., description="Identifiant de l'auteur à supprimer")
    
class DeleteLivre(BaseModel):
    id: int = Field(..., description="Identifiant du livre à supprimer")

class DeleteUtilisateur(BaseModel):
    id: int = Field(..., description="Identifiant de l'utilisateur à supprimer")