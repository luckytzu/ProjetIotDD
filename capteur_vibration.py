from gpiozero import InputDevice

class CapteurVibration:
    def __init__(self, pin=21):
        self.capteur = InputDevice(pin, pull_up=True)

    def lire(self):
        try:
            vibration = 1 if not self.capteur.value else 0
            
            return {"vibration_detectee": vibration}
        except Exception as e:
            print(f"Erreur de lecture du capteur de vibration : {e}")
            return None