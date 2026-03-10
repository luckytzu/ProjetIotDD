import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# --- IMPORTS DE TES CAPTEURS MODULARISÉS ---
from dht11 import CapteurDHT11
from ds18b20 import CapteurDS18B20

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

# --- 2. INITIALISATION ET LECTURE DES CAPTEURS ---
dht11 = CapteurDHT11()
ds18b20 = CapteurDS18B20()

def lire_donnees_capteur():
    donnees = {}
    
    # 1. Lecture DHT11
    valeurs_dht = dht11.lire()
    if valeurs_dht:
        donnees.update(valeurs_dht)
        
    # 2. Lecture DS18B20
    valeurs_ds = ds18b20.lire()
    if valeurs_ds:
        donnees.update(valeurs_ds)
        
    # 3. Validation et envoi
    if len(donnees) > 0:
        donnees["timestamp"] = firestore.SERVER_TIMESTAMP 
        return donnees
    
    return None # Si aucun capteur n'a marché

# --- 3. BOUCLE PRINCIPALE ---
print("Démarrage de l'envoi des données (CTRL+C pour arrêter)...")

while True:
    try:
        donnees = lire_donnees_capteur()
        if donnees:
            db.collection("mes_capteurs").add(donnees)
            heure_actuelle = time.strftime('%H:%M:%S')
            print(f"[{heure_actuelle}] Données envoyées avec succès : {donnees}")
        else:
            print("Aucune donnée valide lue ce cycle, on réessaiera au prochain.")
        
    except Exception as e:
        print(f"Erreur lors de l'envoi : {e}")
    
    # On met le programme en pause pendant 30 secondes
    time.sleep(30)