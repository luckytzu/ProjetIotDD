import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# --- 1. CONFIGURATION FIRESTORE ---
chemin_cle = "projetiotdd-firebase-adminsdk-fbsvc-b8a381685c.json"  

try:
    cred = credentials.Certificate(chemin_cle)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("Connexion à Firestore réussie et sécurisée !")
except Exception as e:
    print(f"Erreur de connexion à Firebase : {e}")
    exit()

# --- 2. FONCTION DE LECTURE DU CAPTEUR ---
def lire_donnees_capteur():
    # TODO: C'est ici qu'on mettra le vrai code de ton capteur
    # Pour l'instant, on simule une lecture
    donnees = {
        "temperature": 24.5, 
        "humidite": 60,
        # SERVER_TIMESTAMP permet à Firestore de dater l'entrée précisément
        "timestamp": firestore.SERVER_TIMESTAMP 
    }
    return donnees

# --- 3. BOUCLE PRINCIPALE ---
print("Démarrage de l'envoi des données (CTRL+C pour arrêter)...")

while True:
    try:
        nouvelles_donnees = lire_donnees_capteur()
        
        db.collection("mes_capteurs").add(nouvelles_donnees)
        
        heure_actuelle = time.strftime('%H:%M:%S')
        print(f"[{heure_actuelle}] Données envoyées avec succès !")
        
    except Exception as e:
        print(f"Erreur lors de l'envoi : {e}")
    
    # On met le programme en pause pendant 30 secondes
    time.sleep(30)