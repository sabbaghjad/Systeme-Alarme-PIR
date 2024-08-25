from Module_LCD.Adafruit_LCD1602 import Adafruit_CharLCD
from Module_LCD.PCF8574 import PCF8574_GPIO
import Module_Keypad.KeypadGPIO as c
from datetime import datetime
from modele import Evenement
from database import Database
from gpiozero import MotionSensor, LED, Buzzer
import tkinter as tk
import time
import threading

class Controleur:
    def __init__(self, modele, vue):
        self.modele = modele
        self.vue = vue

        # Initialisation du lcd
        self.lcd = self.initialiser_lcd()
        
        # Initialisation de la base de donnees
        self.db = Database("evenements.db")
        
        # Initialisation des capteurs
        self.pir = MotionSensor(16)
        self.led_verte = LED(21)
        self.buzzer = Buzzer(12)
        self.led_rouge = LED(20)
        
        
        self.detecter = True
        self.active = True


        # Code pour le keypad
        self.touches = ['1', '2', '3', 'A',
                        '4', '5', '6', 'B',
                       '7', '8', '9', 'C',
                       '*', '0', '#', 'D' ]
        
        self.colonneGPIO = [26, 19, 13, 6]
        self.ligneGPIO = [18, 23, 24, 25]
        self.LIGNE = 4
        self.COLONNE = 4
        self.code = "1234"
        self.compteur = 0
        
        self.clavier = c.Keypad(self.touches, self.ligneGPIO, self.colonneGPIO, self.LIGNE, self.COLONNE)  


    # Methode qui active le systeme d'alarme
    def activer_alarme(self):
        self.led_verte.on()
        self.vue.bouton_activer.config(state="disabled")
        self.lcd.message("Systeme d'alarme\nactive")
        self.vue.label_etat.config(text="Systeme d'alarme active", foreground="green")
        nouveau_evenement = Evenement(dateHeureEvenement=datetime.now(), typeEvenement="activation du systeme d'alarme", valeurEvenement=self.pir.value)        
        self.db.ajouter_evenement(nouveau_evenement)
        evenements = self.db.recuperer_evenements()
        for evenement in evenements:
            if isinstance(evenement.dateHeureEvenement, str):
                evenement.dateHeureEvenement = datetime.strptime(evenement.dateHeureEvenement, "%Y-%m-%d %H:%M:%S.%f")
                self.vue.liste_evenements.insert(tk.END, f"{evenement.dateHeureEvenement.time()} - {evenement.typeEvenement}")
        self.vue.bouton_desactiver.config(state="normal")
        self.detecter_thread = threading.Thread(target=self.check_sensor)
        self.detecter_thread.start()
        
    # Methode qui verifie si le capteur detecte un mouvement
    def check_sensor(self):
        while self.detecter:
            try:
                if self.pir.value == 1:
                    self.detecter_mouvement()
                    self.detecter = False
            except RuntimeError:
                time.sleep(0.1) 
    

    # Methode qui detecte le mouvement
    def detecter_mouvement(self):
        self.lcd.clear()
        self.lcd.message("Mouvement \ndetecte")
        time.sleep(2)
        self.lcd.clear()
        self.lcd.message("Entrez le code \n a 4 chiffres")
        time.sleep(2)
        self.lcd.clear()
        self.vue.bouton_valider_code.config(state="normal")
        
        self.clavier.setDebounceTime(50)
        self.touches_entrees = []
        self.touches_entrees = self.get_key_presses()

    # Methode qui recupere les touches entrees
    def get_key_presses(self, num_presses=4):
        touches_entrees = []
        while len(touches_entrees) < num_presses:
            touche = self.clavier.NULL
            # Attendre que la touche soit pressée
            while touche == self.clavier.NULL:
                touche = self.clavier.getKey()
                time.sleep(0.1)
            self.lcd.message(touche)
            touches_entrees.append(touche)

            # Attendre un court moment pour vérifier si la touche est relâchée
            time.sleep(0.2)
            # Vérifier si la touche est relâchée
            while touche != self.clavier.NULL:
                touche = self.clavier.getKey()
                time.sleep(0.1)
        return touches_entrees
    
    # Methode qui valide le code entree
    def valider_code(self):
        self.vue.bouton_valider_code.config(state="disabled")
        code_entrer = "".join(self.touches_entrees)
        db = Database("evenements.db")
        wrong_attempts = 0
        while wrong_attempts <= 3:
            if code_entrer == self.code:
                self.lcd.clear()
                self.lcd.message("Code valide")
                nouveau_evenement = Evenement(dateHeureEvenement=datetime.now(), typeEvenement="Acces valide", valeurEvenement=self.pir.value)
                db.ajouter_evenement(nouveau_evenement)
                self.vue.liste_evenements.insert(tk.END, f"{nouveau_evenement.dateHeureEvenement.time()} - {nouveau_evenement.typeEvenement}")
                self.clignoter_led(self.led_verte, 3, 0.5)
                self.led_verte.on()
                return
            else:
                wrong_attempts += 1
                if wrong_attempts == 3:
                    wrong_attempts += 1
                self.buzzer.on()
                time.sleep(2)
                self.buzzer.off()
                self.lcd.clear()
                self.lcd.message("Code invalide")
                nouveau_evenement = Evenement(dateHeureEvenement=datetime.now(), typeEvenement="Acces invalide", valeurEvenement=self.pir.value)
                db.ajouter_evenement(nouveau_evenement)
                self.vue.liste_evenements.insert(tk.END, f"{nouveau_evenement.dateHeureEvenement.time()} - {nouveau_evenement.typeEvenement}")
                time.sleep(2)
                self.lcd.clear()
                self.lcd.message("Veuillez \nrecommencer")
                time.sleep(2)
                self.lcd.clear()
                self.touches_entrees = []
                self.touches_entrees = self.get_key_presses()
                code_entrer = "".join(self.touches_entrees)
        self.lcd.clear()
        self.lcd.message("Acces bloque")
        self.led_verte.off()
        self.led_rouge_clignoter = threading.Thread(target=self.clignoter_led_rouge)
        self.led_rouge_clignoter.start()
        nouveau_evenement = Evenement(dateHeureEvenement=datetime.now(), typeEvenement="Acces bloque", valeurEvenement=self.pir.value)
        db.ajouter_evenement(nouveau_evenement)
        self.vue.liste_evenements.insert(tk.END, f"{nouveau_evenement.dateHeureEvenement.time()} - {nouveau_evenement.typeEvenement}")
        self.buzzer.on()
        time.sleep(10)
        self.buzzer.off()
        
    # Methode qui fait clignoter la led rouge indefiniment
    def clignoter_led_rouge(self):
        while self.active:
            self.led_rouge.on()
            time.sleep(0.5)
            self.led_rouge.off()
            time.sleep(0.5)
            
    # Methode qui desactive le systeme
    def desactiver_alarme(self):
        self.vue.bouton_desactiver.config(state="disabled")
        self.led_verte.off()
        self.active = False
        self.led_rouge.on()
        self.lcd.clear()
        self.lcd.message("Systeme d'alarme\ndesactive")
        db = Database("evenements.db")
        nouveau_evenement = Evenement(dateHeureEvenement=datetime.now(), typeEvenement="Systeme desactive", valeurEvenement=self.pir.value)
        db.ajouter_evenement(nouveau_evenement)
        self.vue.liste_evenements.insert(tk.END, f"{nouveau_evenement.dateHeureEvenement.time()} - {nouveau_evenement.typeEvenement}")
        self.vue.label_etat.config(text="Systeme desactive", foreground="red")
            
                      
            
    # Methode qui fait clignoter une led
    def clignoter_led(self, led, nombre_de_clignotement, vitesse):
        for i in range(nombre_de_clignotement):
            led.on()
            time.sleep(vitesse)
            led.off()
            time.sleep(vitesse)
        

    
    def initialiser_lcd(self):
        # Code tire du kit de demarrage de Freenove
        PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
        PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
        # Create PCF8574 GPIO adapter.
        try:
            mcp = PCF8574_GPIO(PCF8574_address)
        except:
            try:
                mcp = PCF8574_GPIO(PCF8574A_address)
            except:
                print ('I2C Address Error !')
                exit(1)
        # Create LCD, passing in MCP GPIO adapter.
        mcp.output(3,1)
        lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)
        lcd.begin(16,2)
        return lcd