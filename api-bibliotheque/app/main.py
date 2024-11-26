from fastapi import FastAPI, HTTPException, Depends
import schemas as s
import crud as c
import token_decode as tc

app = FastAPI()

@app.get('/')
async def get_api():
    return {
        'msg': 'Welcome - API Bibliotheque'
    }

@app.get("/utilisateurs")
async def get_utilisateurs(payload=Depends(tc.verifierTokenAcess)) -> list[s.Utilisateurs]:
    utilisateurs: list = c.get_utilisateurs()
    
    return utilisateurs

@app.get("/livres")
async def get_livres(payload=Depends(tc.verifierTokenAcess)) -> list[s.Livres]:
    livres: list = c.get_livres()
    
    return livres

@app.get("/auteurs")
async def get_auteurs(payload=Depends(tc.verifierTokenAcess)) -> list[s.Auteurs]:
    auteurs: list = c.get_auteurs()
    
    return auteurs

@app.get("/utilisateur/{utilisateur}")
async def get_utilisateur(utilisateur: str, payload=Depends(tc.verifierTokenAcess)) -> s.Utilisateurs:
    utilisateur: dict = c.get_utilisateur(utilisateur)
    
    return utilisateur

@app.route('/utilisateur/emprunts/{utilisateur}')
async def get_emprunts(utilisateur: str, payload=Depends(tc.verifierTokenAcess)) -> list[s.Livres]:
    emprunts: list = c.get_emprunts(utilisateur)
    
    return emprunts

@app.get("/livres/siecle/{numero}")
async def get_livres_siecle(numero:int, payload=Depends(tc.verifierTokenAcess)) -> list[s.Livres]:
    livres: list = c.get_livres_siecle(numero)
    
    return livres

@app.post("/livres/ajouter")
async def ajouter_livre(livre: s.CreateLivre, payload=Depends(tc.verifierTokenAcess)) -> dict:
    return c.ajouter_livre(livre)

@app.post("/utilisateur/ajouter")
async def ajouter_utilisateur(utilisateur: s.CreateUtilisateur, payload=Depends(tc.verifierTokenAcess)) -> dict:
    return c.ajouter_utilisateur(utilisateur)

@app.post("/auteur/ajouter")
async def ajouter_auteur(auteur: s.CreateAuteur, payload=Depends(tc.verifierTokenAcess)) -> dict:
    return c.ajouter_auteur(auteur)

@app.delete("/utilisateur/{utilisateur}/delete")
async def delete_utilisateur(utilisateur: int, payload=Depends(tc.verifierTokenAcess)) -> dict:
    return c.supprimer_utilisateur(utilisateur)

@app.put("/utilisateur/{utilisateur_id}/emprunter/{livre_id}")
def emprunter_livre(utilisateur_id: int, livre_id: int, payload=Depends(tc.verifierTokenAcess)) -> dict:
    return c.emprunter_livre(utilisateur_id, livre_id)

@app.put("/utilisateur/{utilisateur_id}/rendre/{livre_id}")
def rendre_livre(utilisateur_id: int, livre_id: int, payload=Depends(tc.verifierTokenAcess)) -> dict:
    return c.rendre_livre(utilisateur_id, livre_id)