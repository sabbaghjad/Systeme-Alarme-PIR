class Evenement:
    def __init__(self, dateHeureEvenement, typeEvenement, valeurEvenement):
        self.dateHeureEvenement = dateHeureEvenement
        self.typeEvenement = typeEvenement
        self.valeurEvenement = valeurEvenement

    def __repr__(self):
        return f"{self.dateHeureEvenement} - {self.typeEvenement}"

    def afficherEvenement(self):
        return f"Date : {self.dateHeureEvenement}\nType d'événement : {self.typeEvenement}\nValeur : {self.valeurEvenement}"
