import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# --- IMPORTS DE TES CAPTEURS MODULARISÉS ---
from dht11 import CapteurDHT11
from ds18b20 import CapteurDS18B20
from led_rgb import IndicateurLED
from capteur_vibration import CapteurVibration

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
led_statut = IndicateurLED()
vibration = CapteurVibration()

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
        
    # 3. Lecture Vibration (Nouveau !)
    valeurs_vib = vibration.lire()
    if valeurs_vib:
        donnees.update(valeurs_vib)
        
    # Validation et envoi
    if len(donnees) > 0:
        donnees["timestamp"] = firestore.SERVER_TIMESTAMP 
        return donnees
    
    return None

# --- 3. BOUCLE PRINCIPALE ---
print("Démarrage de l'envoi des données (CTRL+C pour arrêter)...")

while True:
    try:
        donnees = lire_donnees_capteur()
        if donnees:
            # --- 1. LOGIQUE DE COULEUR SELON LA TEMPÉRATURE ---
            temperature = donnees.get("temperature_ds18b20", donnees.get("temperature_dht11"))

            # On allume la LED et on ENREGISTRE la couleur dans le dictionnaire
            if temperature is not None:
                if temperature > 30:
                    led_statut.rouge()
                    donnees["alerte_led"] = "rouge"
                elif 20 <= temperature <= 30:
                    led_statut.vert()
                    donnees["alerte_led"] = "vert"
                else: 
                    led_statut.bleu()
                    donnees["alerte_led"] = "bleu"
            else:
                led_statut.eteindre()
                donnees["alerte_led"] = "eteinte"

            # --- 2. ENVOI À FIRESTORE ---
            db.collection("mes_capteurs").add(donnees)
            
            heure_actuelle = time.strftime('%H:%M:%S')
            print(f"[{heure_actuelle}] Données envoyées avec succès : {donnees}")

        else:
            print("Aucune donnée valide lue ce cycle, on réessaiera au prochain.")
            led_statut.eteindre()
        
    except Exception as e:
        print(f"Erreur lors de l'envoi : {e}")
        led_statut.rouge_erreur()
    
    # On met le programme en pause pendant 30 secondes
    time.sleep(30)