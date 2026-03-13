from gpiozero import RGBLED

class IndicateurLED:
    def __init__(self, pin_r=18, pin_g=23, pin_b=24):
        # Initialise la LED sur les bons GPIO
        self.led = RGBLED(red=pin_r, green=pin_g, blue=pin_b)

    def eteindre(self):
        self.led.off()
        
    def rouge(self):
        # Rouge pur : (1, 0, 0)
        self.led.color = (1, 0, 0)
        
    def vert(self):
        # Vert pur : (0, 1, 0)
        self.led.color = (0, 1, 0)
        
    def bleu(self):
        # Bleu pur : (0, 0, 1)
        self.led.color = (0, 0, 1)

    def rouge_erreur(self):
        # Reste identique pour signaler un plantage
        self.led.color = (1, 0, 0)