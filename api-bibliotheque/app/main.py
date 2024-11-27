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

@app.get("/utilisateurs", response_model=list[s.Utilisateurs])
async def get_utilisateurs(payload=Depends(tc.verifierTokenAcess)) -> list[s.Utilisateurs]:
    try:
        utilisateurs: list[s.Utilisateurs] = c.get_utilisateurs()
        
        if not utilisateurs:
            raise HTTPException(status_code=404, detail="Aucun utilisateurs trouvé.")
        
        return utilisateurs
    
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erreur interne du serveur : {str(e)}"
        )

@app.get("/livres")
async def get_livres(payload=Depends(tc.verifierTokenAcess)) -> list[s.Livres]:
    try:
        livres: list = c.get_livres()
        
        if not livres:
            raise HTTPException(status_code=404, detail="Aucun auteurs trouvé.")
        
        return livres

    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erreur interne du serveur : {str(e)}"
        )

@app.get("/auteurs")
async def get_auteurs(payload=Depends(tc.verifierTokenAcess)) -> list[s.Auteurs]:
    try:
        auteurs: list = c.get_auteurs()
        
        if not auteurs:
            raise HTTPException(status_code=404, detail="Aucun auteurs trouvé.")
        
        return auteurs

    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erreur interne du serveur : {str(e)}"
        )

@app.get("/utilisateur/{utilisateur}")
async def get_utilisateur(utilisateur: str, payload=Depends(tc.verifierTokenAcess)) -> s.Utilisateurs:
    try:
        utilisateurs: dict = c.get_utilisateur(utilisateur)
        
        if not utilisateurs:
            raise HTTPException(status_code=404, detail="Aucun utilisateurs trouvé.")
        
        return utilisateurs

    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erreur interne du serveur : {str(e)}"
        )

@app.route('/utilisateur/emprunts/{utilisateur}')
async def get_emprunts(utilisateur: str, payload=Depends(tc.verifierTokenAcess)) -> list[s.Livres]:
    try:
        emprunts: list = c.get_emprunts(utilisateur)
        
        if not emprunts:
            raise HTTPException(status_code=404, detail="Aucun emprunts trouvé.")
        
        return emprunts

    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erreur interne du serveur : {str(e)}"
        )

@app.get("/livres/siecle/{numero}")
async def get_livres_siecle(numero:int, payload=Depends(tc.verifierTokenAcess)) -> list[s.Livres]:
    try:
        livres: list = c.get_livres_siecle(numero)
        
        if not livres:
            raise HTTPException(status_code=404, detail="Aucun livres trouvé.")
        
        return livres

    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erreur interne du serveur : {str(e)}"
        )

@app.post("/livres/ajouter")
async def ajouter_livre(livre: s.CreateLivre, payload=Depends(tc.verifierTokenAcess)) -> dict:
    try:
        nouveau_livre = c.ajouter_livre(livre)

        if not nouveau_livre:
            raise HTTPException(
                status_code=500,
                detail="Erreur lors de l'ajout du livre."
            )

        return nouveau_livre

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur interne du serveur : {str(e)}"
        )

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