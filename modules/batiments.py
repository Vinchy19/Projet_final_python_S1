import os
import sqlite3
from authentification import Gestion_authentification, effacer_ecran, pause

db_name = "data/projet.db"

class Batiments:
    """
    Classe por definir(creer) les batiments.
    """
    def __init__(self, code_batiment, nbre_salles, nbre_etages):
        self.code_batiment = code_batiment
        self.nbre_salles = nbre_salles
        self.nbre_etages = nbre_etages

class Gestion_batiments:
    """
    Classe pour la gestion des batiments.
    """
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.table_batiments()

    def table_batiments(self):
        """
        Methode pour creer la table.
        """
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Batiments (
                            code_batiment TEXT PRIMARY KEY,
                            nbre_salles INTEGER,
                            nbre_etages INTEGER)""")
        self.conn.commit()

    def verify_batiment(self, code_batiment):
        """
        Methode pour verifier si un batiment est enregistrer. 
        """
        effacer_ecran()
        SQL = "SELECT * FROM Batiments WHERE code_batiment=?"
        self.cursor.execute(SQL, (code_batiment,))
        return self.cursor.fetchone() is not None
       

    def enregistrer(self, batiment):
        """
        Methode pour enregistrer un batiment. 
        """
        effacer_ecran()
        self.cursor.execute("SELECT * FROM Batiments WHERE code_batiment=?", (batiment.code_batiment,))
        batiment_trouve = self.cursor.fetchone()
        if batiment_trouve:
            print("Ce bâtiment est déjà enregistré.")
        else:
            SQL = """INSERT INTO Batiments (code_batiment, nbre_salles, nbre_etages) VALUES (?, ?, ?)"""
            self.cursor.execute(SQL, (batiment.code_batiment, batiment.nbre_salles, batiment.nbre_etages))
            self.conn.commit()
            print("Enregistrement réussi.")
        pause()

    def afficher(self):
        """
        Methode pour afficher les batiments.
        """
        effacer_ecran()
        self.cursor.execute("SELECT * FROM Batiments")
        tous_batiments = self.cursor.fetchall()
        if tous_batiments:
            for batiment in tous_batiments:
                print(f"Code Bâtiment : {batiment[0]}")
                print(f"Nombre de salles du Bâtiment : {batiment[1]}")
                print(f"Nombre d'étages du Bâtiment : {batiment[2]}\n")
        else:
            print("Aucun bâtiment trouvé.")
        pause()

    def rechercher(self, code_batiment):
        """
        Methode pour rechercher un batiment par son code.
        """
        effacer_ecran()
        self.cursor.execute("SELECT * FROM Batiments WHERE code_batiment=?", (code_batiment,))
        batiment = self.cursor.fetchone()
        if batiment:
            print("----------Votre Bâtiment---------")
            print(f"Code Bâtiment : {batiment[0]}")
            print(f"Nombre de salles du Bâtiment : {batiment[1]}")
            print(f"Nombre d'étages du Bâtiment : {batiment[2]}")
        else:
            print("Aucun bâtiment trouvé avec ce code.")
        pause()

    def supprimer(self, code_batiment):
        """
        Methode pour suprimmer un batiment. 
        """
        self.cursor.execute("SELECT * FROM Batiments WHERE code_batiment=?", (code_batiment,))
        batiment = self.cursor.fetchone()
        if batiment:
            self.cursor.execute("DELETE FROM Batiments WHERE code_batiment=?", (code_batiment,))
            self.conn.commit()
            print("Suppression réussie.")
        else:
            print("Bâtiment introuvable.")
        pause()

def choix_batiments(action):
    """
    Fonction permettant de choisir un batiment pour une action qui sera definie.
    """
    while True:
        effacer_ecran()
        print("*********************************************")
        print(f"* Choisir le chiffre du bâtiment à {action} *")
        print("*********************************************")
        print("1. A")
        print("2. B")
        print("3. C")
        print("4. D")
        choix = input("Veuillez choisir un numéro : ")
        try:
            choix_batiment = int(choix)
            if 1 <= choix_batiment <= 4:
                code = chr(64 + choix_batiment)  # Convertir 1-4 en A-D
                return code
            else:
                print("Veuillez choisir un nombre entre 1 et 4.")
                pause()
        except ValueError:
            print("Choisir un nombre entre 1 et 4.")
            pause()

def menu_batiments():
    """
    Fonction permet la gestion des differentes taches.
    """
    while True:
        effacer_ecran()
        print("*************************************")
        print("* Menu Gestion Bâtiments *")
        print("*************************************")
        print("1. Enregistrer un Bâtiment")
        print("2. Afficher les Bâtiments")
        print("3. Rechercher un Bâtiment")
        print("4. Supprimer un Bâtiment")
        print("5. Quitter le Menu")
        choix = input("Que voulez-vous faire ? Veuillez choisir un numéro : ")
        try:
            choix_principal = int(choix)
            if 1 <= choix_principal <= 5:
                return choix_principal
            else:
                print("Choisir un nombre entre 1 et 5.")
                pause()
        except ValueError:
            print("Choisir un nombre entre 1 et 5.")
            pause()

def pour_enregistrer():
    """
    Fonction permettent d'enregistrer une salle en passant par la methode.
    """
    gauth = Gestion_authentification(db_name)
    if gauth.verifier_authentifier():
        code_batiment = choix_batiments("enregistrer")
        nbre_salles = 18
        nbre_etages = 3
        gbatiment = Gestion_batiments(db_name)
        batiment = Batiments(code_batiment, nbre_salles, nbre_etages)
        gbatiment.enregistrer(batiment)
    else:
        print("ID et/ou mot de passe incorrect.")
        pause()

def pour_afficher():
    """
    Cette fonction permet d'afficher les batiments.
    """
    gbatiment = Gestion_batiments(db_name)
    gbatiment.afficher()

def pour_rechercher():
    """
    Cette fonction permet de rechercher un batiment.
    """
    code_batiment = choix_batiments("rechercher")
    gbatiment = Gestion_batiments(db_name)
    gbatiment.rechercher(code_batiment)

def pour_supprimer():
    """
    Cette fonction permet de suprimr un btiment par son code.
    """
    gauth = Gestion_authentification(db_name)
    if gauth.verifier_authentifier():
        code_batiment = choix_batiments("supprimer")
        gbatiment = Gestion_batiments(db_name)
        gbatiment.supprimer(code_batiment)
    else:
        print("ID et/ou mot de passe incorrect.")
        pause()

def main_batiment():
    """
    C'est la focntion main de la gestion batiment permet d'apliquer les differentes personaliter.
    """
    while True:
        effacer_ecran()
        menu = menu_batiments()
        if menu == 1:
            pour_enregistrer()
        elif menu == 2:
            pour_afficher()
        elif menu == 3:
            pour_rechercher()
        elif menu == 4:
            pour_supprimer()
        else:
            break

# if __name__ == "__main__":
#     main_batiment()
