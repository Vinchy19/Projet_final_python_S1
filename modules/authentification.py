"""Module permettant de gerer le droit d'acces (authetification) au projet."""

import os
import sqlite3

db_name = "data/projet.db"

class Authentification:
    """Classe pour creer l'instance authentification."""

    def __init__(self, code_authentification, password):
        """Pour creer l'instance authemtification."""
        self.code_authentification = code_authentification
        self.password = password

class Gestion_authentification:
    """Classe pour la gestion des authentifier."""

    def __init__(self, db_name):
        """Methode pour creer l'instance de gestion."""
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.table_authentifications()

    def table_authentifications(self):
        """Creation de la table Authentifications."""
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Authentifications (
                            code_authentification TEXT PRIMARY KEY, password TEXT)""")
        self.conn.commit()

    def verifier_authentifier(self):
        """Methode permettant de veriddier l'authentificationd'un administrateur."""
        print("\n Veuillez vous authentifier...\n")
        code = input("Entrez votre ID d'authentification : ")
        password = input("Entrez votre mot de passe d'authentification : ")
        self.cursor.execute("SELECT * FROM \
            Authentifications WHERE code_authentification=?", (code,))
        authentifier = self.cursor.fetchone()
        if authentifier and authentifier[1] == password:
            return True
        return False

    def enregistrer(self, authentifier):
        """Methode permettant d'eregistrer un admin par le super admin."""
        self.cursor.execute("SELECT * FROM Authentifications \
                            WHERE code_authentification=?",
                            (authentifier.code_authentification,))
        authentifier_trouve = self.cursor.fetchone()
        if authentifier_trouve:
            print("Cet identifiant est déjà enregistré.")
        else:
            SQL = """INSERT INTO Authentifications
              (code_authentification, password) 
            VALUES (?, ?)"""
            self.cursor.execute(SQL, (authentifier.code_authentification,
                                      authentifier.password))
            self.conn.commit()
            print("Enregistrement réussi.")
        pause()

    def afficher(self, masque_password):
        """Methode permettant d'afficher les admin."""
        self.cursor.execute("SELECT * FROM Authentifications")
        tous_authentifiers = self.cursor.fetchall()
        if tous_authentifiers:
            for authentifier in tous_authentifiers:
                password = "Caché" if masque_password else authentifier[1]
                print(f"Code Authentifiant : {authentifier[0]}")
                print(f"Mot de passe : {password}\n")
        else:
            print("Aucun authentifiant trouvé.")
        pause()

    def rechercher(self, code_authentifier):
        """Methode permettant de rechercher un admin."""
        effacer_ecran()
        self.cursor.execute("SELECT * FROM Authentifications\
             WHERE code_authentification=?", (code_authentifier,))
        authentifier = self.cursor.fetchone()
        if authentifier:
            print("----------Votre Authentifiant---------")
            print(f"Code Authentifiant : {authentifier[0]}")
            print("Mot de passe : Caché")
        else:
            print("Aucun authentifiant trouvé avec ce code.")
        pause()

    def supprimer(self, code):
        """Methode pour suprimmer un admin."""
        self.cursor.execute("DELETE FROM Authentifications\
                     WHERE code_authentification=?", (code,))
        self.conn.commit()
        print("Suppression réussie.")
        pause()

def effacer_ecran():
    """Effacer l'écran."""
    os.system("cls" if os.name == "nt" else "clear")

def pause():
    """Faire une pause."""
    os.system("pause")

def menu_authentifications():
    """Menu principal pour la gestion des authentifications."""
    while True:
        effacer_ecran()
        print("*************************************")
        print("* Menu Gestion Authentifications *")
        print("*************************************")
        print("1. Enregistrer un Authentifiant")
        print("2. Afficher les Authentifiants (sans mot de passe)")
        print("3. Afficher les Authentifiants (avec mot de passe)")
        print("4. Rechercher un Authentifiant")
        print("5. Supprimer un Authentifiant")
        print("6. Quitter le Menu")
        choix = input("Que voulez-vous faire ? Veuillez choisir un numéro : ")
        print("\n")
        try:
            choix_principal = int(choix)
            if 1 <= choix_principal <= 6:
                return choix_principal
            # else:
            print("Choisir un nombre entre 1 et 6.")
            pause()
        except ValueError:
            print("Choisir un nombre entre 1 et 6.")
            pause()

def verifier_super_admin():
    """Vérification des informations d'authentification du super admin."""
    print("Vérifiez que vous êtes un super admin.")
    id = input("Entrez votre ID super admin : ")
    passwd = input("Entrez le mot de passe super admin : ")
    return id == "jonas" and passwd == "jonas"

def pour_enregistrer():
    """Fonction qui permet d'enregistrer un admin par le super admin."""
    if verifier_super_admin():
        while True:
            effacer_ecran()
            code = input("Entrez un ID pour le nouvel \
authentifiant(min 3) : ")
            password = input("Entrez un mot de passe pour \
le nouvel authentifiant(min 3) : ")
            password_confirmed = input("Confirmez le mot \
de passe pour le nouvel authentifiant : ")
            if len(code) > 2 and len(password) > 2:
                if password == password_confirmed:
                    authentifiant = Authentification(code, password)
                    gauth = Gestion_authentification(db_name)
                    gauth.enregistrer(authentifiant)
                    break
                # else:
                print("Les mots de passe ne correspondent pas.")
                pause()
            else:
                print("ID et/ou mot de passe trop courts.")
                pause()
    else:
        print("ID et/ou mot de passe incorrect.")
        pause()

def pour_afficher():
    """Fonction pour d'afficher un admin."""
    gauth = Gestion_authentification(db_name)
    gauth.afficher(True)

def pour_afficher_tous():
    """Fonction pour afficher les admins."""
    if verifier_super_admin():
        gauth = Gestion_authentification(db_name)
        gauth.afficher(False)
    else:
        print("ID et/ou mot de passe incorrect.")
        pause()

def pour_rechercher():
    """Fonction pour rechercher un admin."""
    code = input("Entrez l'ID pour rechercher : ")
    gauth = Gestion_authentification(db_name)
    gauth.rechercher(code)

def pour_supprimer():
    """Fonction qui permet d e suprimmer un admin."""
    if verifier_super_admin():
        code = input("Entrez l'ID pour supprimer : ")
        gauth = Gestion_authentification(db_name)
        gauth.supprimer(code)
    else:
        print("ID et/ou mot de passe incorrect.")
        pause()

def main_authentification():
    """Cette fonction permet la gestion des \
differentes fonctionalites des salles."""
    while True:
        effacer_ecran()
        menu = menu_authentifications()
        if menu == 1:
            pour_enregistrer()
        elif menu == 2:
            pour_afficher()
        elif menu == 3:
            pour_afficher_tous()
        elif menu == 4:
            pour_rechercher()
        elif menu == 5:
            pour_supprimer()
        else:
            break

# if __name__ == "__main__":
#     main_authentification()
