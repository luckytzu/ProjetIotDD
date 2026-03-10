import board
import adafruit_dht

class CapteurDHT11:
    def __init__(self, pin=board.D17):
        self.capteur = adafruit_dht.DHT11(pin)

    def lire(self):
        try:
            temp = self.capteur.temperature
            hum = self.capteur.humidity
            if temp is not None and hum is not None:
                return {"temperature_dht11": temp, "humidite_dht11": hum}
        except RuntimeError as e:
            print(f"Avertissement DHT11 (lecture ratée) : {e.args[0]}")
        except Exception as e:
            self.capteur.exit()
            print(f"Erreur critique DHT11 : {e}")
        return None