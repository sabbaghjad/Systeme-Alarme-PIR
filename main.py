import vue as v
import modele as m
import controleur as c
import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Système d'alarme")
        
        modele = m.Evenement( 0, "Désactivé", 0)
        
        vue = v.Vue(self)
        vue.grid(row=0, column=0, padx=10, pady=10)
        
        controleur = c.Controleur(modele, vue)
        
        vue.set_controleur(controleur)
        
if __name__ == "__main__":
    app = App()
    app.mainloop()