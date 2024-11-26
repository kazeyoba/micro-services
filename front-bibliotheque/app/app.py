from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from werkzeug.utils import secure_filename
import api

import requests

app = Flask(__name__)
app.secret_key = "secret-key"  # Utilisé pour les messages flash

API_URL = "http://api-server:5000"  # URL de base de l'API FastAPI

@app.route('/', endpoint='index')
def index():
    return render_template("index.html.j2")

@app.route('/utilisateurs', endpoint="utilisateurs")
def utilisateurs():
    response = requests.get(f"{API_URL}/utilisateurs")
    if response.status_code == 200:
        utilisateurs = response.json()
        return render_template("renders/tableau.html.j2", data_list=utilisateurs, name="Tableau utilisateurs",  addUri="/utilisateur/ajouter", addMsg="Ajouter utilisateur", deleteUri="/utilisateur/")
    else:
        flash("Erreur lors de la récupération des utilisateurs.")
        return redirect(url_for('index'))
    
@app.route('/livres', endpoint="livres")
def livres():
    response = requests.get(f"{API_URL}/livres")
    if response.status_code == 200:
        livres = response.json()
        return render_template("renders/tableau.html.j2", data_list=livres, name="Tableau livres", addUri="/livres/ajouter", addMsg="Ajouter livre")
    else:
        flash("Erreur lors de la récupération des livres.")
        return redirect(url_for('index'))

@app.route('/auteurs', endpoint="auteurs")
def auteurs():
    response = requests.get(f"{API_URL}/auteurs")
    if response.status_code == 200:
        auteurs = response.json()

        return render_template("renders/tableau.html.j2", data_list=auteurs, name="Tableau auteurs", addUri="/auteur/ajouter", addMsg="Ajouter auteur")
    else:
        flash("Erreur lors de la récupération des auteurs.")
        return redirect(url_for('index'))
    
@app.route('/utilisateur/ajouter', methods=["GET", "POST"], endpoint="adduser")
def ajouter_utilisateur():
    if request.method == "POST":
        nom_utilisateur = request.form.get("nom_utilisateur")
        data = {"nom_utilisateur": nom_utilisateur}
        response = requests.post(f"{API_URL}/utilisateur/ajouter", json=data)
        if response.status_code == 200:
            flash("Utilisateur ajouté avec succès.")
        else:
            flash("Erreur lors de l'ajout de l'utilisateur.")
        return redirect(url_for('utilisateurs'))
    return render_template("forms/ajouter_utilisateur.html.j2")

@app.route('/livres/ajouter', methods=["GET", "POST"], endpoint="addlivre")
def ajouter_livre():
    if request.method == "POST":
        titre = request.form.get("nom_livre")
        pitch = request.form.get("pitch_livre")
        nom_auteur = request.form.get("nom_auteur_livre")
        date_public = request.form.get("date_public_livre")
        data = {
            "titre": titre,
            "pitch": pitch,
            "nom_auteur": nom_auteur,
            "date_public": date_public
        }
        response = requests.post(f"{API_URL}/livres/ajouter", json=data)
        if response.status_code == 200:
            flash("Livre ajouté avec succès.")
        else:
            flash("Erreur lors de l'ajout du livre.")
        return redirect(url_for('livres'))
    return render_template("forms/ajouter_livres.html.j2")

@app.route('/auteur/ajouter', methods=["GET", "POST"], endpoint="addauteur")
def ajouter_auteur():
    if request.method == "POST":
        nom_auteur = request.form.get("nom_auteur")
        data = {"nom_auteur": nom_auteur}
        response = requests.post(f"{API_URL}/auteur/ajouter", json=data)
        if response.status_code == 200:
            flash("Auteur ajouté avec succès.")
        else:
            flash("Erreur lors de l'ajout de l'auteur.")
        return redirect(url_for('auteurs'))
    return render_template("forms/ajouter_auteur.html.j2")

@app.route('/utilisateur/<int:utilisateur_id>/delete', methods=["POST"], endpoint="deleteUser")
def supprimer_utilisateur(utilisateur_id):
    response = requests.delete(f"{API_URL}/utilisateur/{utilisateur_id}/delete")
    if response.status_code == 200:
        flash("Utilisateur supprimé avec succès.")
    else:
        flash("Erreur lors de la suppression de l'utilisateur.")
    return redirect(url_for('utilisateurs'))

@app.route('/utilisateur/<int:utilisateur_id>/emprunter/<int:livre_id>', methods=["POST"])
def emprunter_livre(utilisateur_id, livre_id):
    response = requests.put(f"{API_URL}/utilisateur/{utilisateur_id}/emprunter/{livre_id}")
    if response.status_code == 200:
        flash("Livre emprunté avec succès.")
    else:
        flash("Erreur lors de l'emprunt du livre.")
    return redirect(url_for('utilisateurs'))

@app.route('/utilisateur/<int:utilisateur_id>/rendre/<int:livre_id>', methods=["POST"])
def rendre_livre(utilisateur_id, livre_id):
    response = requests.put(f"{API_URL}/utilisateur/{utilisateur_id}/rendre/{livre_id}")
    if response.status_code == 200:
        flash("Livre rendu avec succès.")
    else:
        flash("Erreur lors du retour du livre.")
    return redirect(url_for('utilisateurs'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Gère la connexion de l'utilisateur.

    Returns:
        Union[make_response, redirect]: Renvoie le template HTML de la page de connexion ou redirige vers la page d'accueil si la connexion est réussie.
    """
    if request.method == 'GET':
        # Traitement pour les demandes GET
        if 'access_token' in request.cookies:
            response = make_response(render_template('login.html'))
            response.set_cookie('access_token', '', expires=0)
        else:
            response = make_response(render_template('forms/login.html.j2'))
        return response
    
    elif request.method == 'POST':
        mail = request.form.get('mail')
        password = request.form.get('pass')
        
        # Tentative de récupération du token:
        token = api.get_access_token(email=mail, password=password)
        
        if 'access_token' in token:
            response = make_response(redirect("/index"))
            response.set_cookie('access_token', token['access_token'])
            return response
        else:
            return redirect("/login")

if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")
