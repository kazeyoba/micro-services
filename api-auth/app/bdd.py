import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

CONFIG_PATH: str = "./config.json"

def get_db_session(config_file_path: str = CONFIG_PATH):
    """
    Établit une connexion à la base de données en utilisant les informations du fichier de configuration spécifié.

    Arguments :
        config_file_path : chaîne de caractères qui indique le chemin d'accès au fichier de configuration (par défaut : CONFIG_PATH).

    Retour :
        session : objet de type Session qui représente une session de base de données.

    Ouvre le fichier de configuration JSON spécifié, extrait les informations nécessaires pour se connecter à la base de données MySQL, crée une instance de moteur SQLAlchemy, crée toutes les tables nécessaires à l'aide de la méthode create_all() de Base.metadata, crée une instance de sessionmaker liée au moteur et retourne une session active.

    Lève une exception en cas d'erreur lors de la lecture du fichier de configuration ou de la connexion à la base de données.
    """
    with open(config_file_path, 'r') as f:
        config = json.load(f)

    url = f"postgresql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"

    engine = create_engine(url)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    return session

def testSession(config_file_path):
    """
    Vérifie si une session de base de données peut être établie en exécutant une requête de test.

    Arguments :
        config_file_path : chaîne de caractères qui indique le chemin d'accès au fichier de configuration contenant les informations de connexion à la base de données.

    Retour :
        test : valeur booléenne qui indique si la session de base de données est valide (True) ou non (False).

    Établit une session de base de données en utilisant la fonction get_db_session(), puis exécute une requête de test pour vérifier que la connexion à la base de données est valide. Si la requête est réussie, la valeur de retour est True, sinon la valeur de retour est False.
    """
    test: bool = None
    session = get_db_session(config_file_path)

    try:
        session.execute("SELECT 1")
        test = True
    except:
        test = False
    finally:
        session.close()
    
    return test