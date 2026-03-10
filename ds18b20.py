from w1thermsensor import W1ThermSensor

class CapteurDS18B20:
    def __init__(self):
        try:
            self.capteur = W1ThermSensor()
        except Exception as e:
            print(f"Erreur d'initialisation du DS18B20 : {e}")
            self.capteur = None

    def lire(self):
        if not self.capteur:
            return None
        try:
            temp = self.capteur.get_temperature()
            return {"temperature_ds18b20": round(temp, 2)}
        except Exception as e:
            print(f"Erreur de lecture DS18B20 : {e}")
            return None