import json
import requests
import jwt
from flask import jsonify

"""
Ce module contient des fonctions pour interagir avec une API RESTful.

Les fonctions disponibles sont :
    - read_json_file : lit un fichier JSON et retourne un objet Python.
    - get_api : envoie une requête GET à une API et retourne le contenu de la réponse.
    - get_access_token : envoie une requête POST pour obtenir un token d'accès à l'API.
    - decode_token : décode un token JWT.
    - create_product : envoie une requête POST pour créer un produit.
    - delete_product : envoie une requête DELETE pour supprimer un produit.
"""

def read_json_file(file_path: str = "config.json") -> dict:
    """
    La fonction read_json_file ouvre et charge un fichier JSON en tant que dictionnaire Python.

    Args:
        file_path (str, optionnel): Le chemin d'accès au fichier JSON. Par défaut, il s'agit du fichier config.json dans le répertoire courant.
    
    Returns:
        dict: le dictionnaire Python contenant les données JSON chargées depuis le fichier.
    """
    with open(file_path) as f:
        config = json.load(f)
    return config

CONFIG_API: dict = read_json_file("config.json")

def get_api(endpoint: str = "/", api_url: str = CONFIG_API['api_url'], api_port: str = CONFIG_API['api_port'], token: str = None) -> dict:
    """
    La fonction get_api() effectue une requête HTTP GET vers une API à l'aide de la bibliothèque Python Requests. Elle prend en entrée des arguments optionnels qui 
    définissent l'URL de l'API, le port sur lequel se connecter, l'endpoint à atteindre et un jeton d'authentification.

    Args:
        endpoint (str, optional):  l'endpoint à atteindre de l'API. Defaults to "/".
        api_url (str, optional):  l'URL de l'API, par défaut. Defaults to CONFIG_API['api_url'].
        api_port (str, optional): le port de l'API. Defaults to CONFIG_API['api_port'].
        token (str, optional): le jeton d'authentification à utiliser pour la requête. Defaults to None.

    Returns:
        dict: La fonction retourne un dictionnaire contenant les données JSON de la réponse de l'API.
    """
    url = f"http://{api_url}:{api_port}{endpoint}"
    headers = {}
    if token:
        headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    data = json.loads(response.content)
    return data

def get_access_token(email: str, password: str, api_url: str = CONFIG_API['api_token_url'], api_port: str = CONFIG_API['api_token_port']) -> str:
    """
    get_access_token Cette fonction permet de récupérer un token d'accès à l'API en utilisant une requête POST avec un email et un mot de passe.

    Args:
        email (str): l'adresse e-mail de l'utilisateur.
        password (str): le mot de passe de l'utilisateur.
        api_url (str, facultatif): l'URL de l'API pour récupérer le token. Par défaut, la valeur est `CONFIG_API['api_token_url']`.
        api_port (str, facultatif): le port de l'API pour récupérer le token. Par défaut, la valeur est `CONFIG_API['api_token_port']`.

    Returns:
        str: un token d'accès à l'API.
    """
    token: dict = {}
    url = f"http://{api_url}:{api_port}/login"
    payload = {
        "EmailUtilisateur": email,
        "MotdepasseUtilisateur": password
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        token = response.json()
    
    return token

def decode_token(token: str, secret: str = CONFIG_API['SECRET_KEY'], algorithms: str = CONFIG_API['ALGORITHMS']) -> dict:
    """
    Décode un token JWT en utilisant une clé secrète.

    Args:
        token (str): Le token JWT à décoder.
        secret (str, optional): La clé secrète utilisée pour signer le token. Defaults to CONFIG_API['SECRET_KEY'].
        algorithms (str, optional): La liste des algorithmes de signature acceptés. Defaults to CONFIG_API['ALGORITHMS'].

    Returns:
        dict: Un dictionnaire contenant les informations stockées dans le token décodé. En cas d'erreur, un message d'erreur est renvoyé.
    """
    try:
        decode_token = jwt.decode(token, secret, algorithms=algorithms, options={"verify_aud": False})
    except jwt.exceptions.DecodeError:
        decode_token = {"message" : "Impossible de décoder le token"}
    
    return decode_token
