import schemas as s
import token_generator as tk
import auth
from fastapi import FastAPI, HTTPException
from datetime import datetime, timezone

app = FastAPI()

@app.get("/")
async def root():
    """
    Renvoie un message de bienvenue à l'utilisateur.

    Retour :
        Dictionnaire JSON contenant une clé "message" avec le message de bienvenue.
    """

    return {"message": "Bienvenu sur l'API d'authentification"}

@app.post("/login")
async def logingUser(user: s.UserLogin) -> dict:
    """
    Authentifie un utilisateur en vérifiant ses informations d'identification et en créant un jeton d'accès.

    Arguments :
        user : objet de type UserLogin qui contient l'adresse e-mail et le mot de passe de l'utilisateur à authentifier.

    Retour :
        dict: Dictionnaire JSON contenant une clé "access_token" avec le jeton d'accès généré et une clé "token_type" avec la valeur "bearer".

    Lève une exception HTTPException si l'utilisateur n'a pas pu être authentifié.
    """
    reponse: dict
    try:
        utilisateur = auth.challenge_auth(user=user)
        access_token = tk.token_generator(utilisateur)
        reponse = {"access_token": access_token, "token_type": "bearer"}
    except HTTPException as e:
        reponse = {"message": "Login fail", "detail": e.detail}
    
    return reponse

@app.get("/date")
def get_current_datetime():
    """
    Retourne l'heure actuelle au format ISO 8601.
    """
    current_time = datetime.now(timezone.utc)
    return {"current_datetime": current_time.isoformat()}