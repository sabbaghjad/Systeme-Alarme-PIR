import tkinter as tk
from tkinter import ttk
import threading

class Vue(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        style = ttk.Style()
        style.theme_use("alt")
        
        self.controleur = None

        # Widgets
        self.bouton_activer = ttk.Button(self, text="Activer l'alarme")
        self.bouton_desactiver = ttk.Button(self, text="Désactiver l'alarme")
        self.bouton_valider_code = ttk.Button(self, text="Valider le code", state="disabled", command=self.valider_code)
        self.liste_evenements = tk.Listbox(self, width=50, height=10)
        self.label_etat = ttk.Label(self, text="Système d'alarme désactivé")

        # Placement des widgets
        self.bouton_activer.grid(row=0, column=0, padx=5, pady=5)
        self.bouton_desactiver.grid(row=0, column=1, padx=5, pady=5)
        self.bouton_valider_code.grid(row=1, column=1, padx=5, pady=5)
        self.liste_evenements.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        self.label_etat.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.bouton_activer.config(command=self.activer_alarme)
        self.bouton_desactiver.config(command=self.desactiver_alarme)
        self.bouton_valider_code.config(command=self.valider_code)


    def activer_alarme(self):
        if self.controleur:
            self.controleur.activer_alarme()


    def desactiver_alarme(self):
        if self.controleur:
            self.controleur.desactiver_alarme()

    def valider_code(self):
        if self.controleur:
            self.valider_thread = threading.Thread(target=self.controleur.valider_code)
            self.valider_thread.start()

    
    def set_controleur(self, controleur):
        self.controleur = controleur

