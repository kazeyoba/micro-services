"""
Définit la classe UserLogin pour représenter les informations d'identification d'un utilisateur.

La classe UserLogin hérite de la classe de base de Pydantic et représente les informations d'identification d'un utilisateur. Elle est utilisée pour valider les données d'entrée lorsqu'un utilisateur tente de s'authentifier.

Attributs :
    - EmailUtilisateur : attribut chaîne de caractères qui représente l'adresse e-mail de l'utilisateur.
    - MotdepasseUtilisateur : attribut chaîne de caractères qui représente le mot de passe de l'utilisateur.
"""

from pydantic import BaseModel

class UserLogin(BaseModel):
    EmailUtilisateur: str
    MotdepasseUtilisateur: str