from gpiozero import RGBLED
import random

class IndicateurLED:
    def __init__(self, pin_r=18, pin_g=23, pin_b=24):
        self.led = RGBLED(red=pin_r, green=pin_g, blue=pin_b)

    def couleur_aleatoire(self):
        r = random.random()
        g = random.random()
        b = random.random()
        self.led.color = (r, g, b)

    def eteindre(self):
        self.led.off()
        
    def rouge_erreur(self):
        self.led.color = (0, 1, 0)