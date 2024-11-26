"""
Définit la classe ORM pour la table Utilisateur de la base de données.

La classe Utilisateur hérite de la classe declarative_base() de SQLAlchemy et représente la structure de la table "Utilisateur" dans la base de données. Elle est utilisée pour mapper les enregistrements de la table "Utilisateur" aux instances de la classe Utilisateur.

Attributs :
    - NoUtilisateur : attribut entier qui représente la clé primaire de la table "Utilisateur".
    - NomUtilisateur : attribut chaîne de caractères qui représente le nom de l'utilisateur.
    - PrenomUtilisateur : attribut chaîne de caractères qui représente le prénom de l'utilisateur.
    - EmailUtilisateur : attribut chaîne de caractères qui représente l'adresse e-mail de l'utilisateur.
    - MotdepasseUtilisateur : attribut chaîne de caractères qui représente le mot de passe de l'utilisateur.
    - Statut : attribut chaîne de caractères qui représente le statut de l'utilisateur (par défaut : 'user').
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Définir une classe ORM pour la table Utilisateur
class Utilisateur(Base):
    __tablename__ = 'Utilisateur'
    NoUtilisateur = Column(Integer, primary_key=True)
    NomUtilisateur = Column(String(50))
    PrenomUtilisateur = Column(String(50))
    EmailUtilisateur = Column(String(50))
    MotdepasseUtilisateur = Column(String(255))
    Statut = Column(String(20), default='user')