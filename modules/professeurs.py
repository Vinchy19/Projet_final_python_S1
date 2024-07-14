"""Module pour les professeurs."""

import sqlite3
import re
from authentification import Gestion_authentification, effacer_ecran, pause
from cours import Gestion_cours

db_name = "data/projet.db"


class Professeurs:
    """Classe pour l'instace professeur."""

    def __init__(self, code_professeur, nom_professeur, prenom_professeur,
                 sexe_professeur, tel_professeur, email_professeur):
        """Creation de l'instance."""
        self.code_professeur = code_professeur
        self.nom_professeur = nom_professeur
        self.prenom_professeur = prenom_professeur
        self.sexe_professeur = sexe_professeur
        self.tel_professeur = tel_professeur
        self.email_professeur = email_professeur


class Gestion_professeurs:
    """Classe pour la gestion des professeurs."""

    def __init__(self, db_name):
        """Creation de l'instance pour gerer les professeurs."""
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.table_professeurs()

    def table_professeurs(self):
        """Creation de la table professeur."""
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Professeurs (
                                    code_professeur TEXT PRIMARY KEY,
                                    nom_professeur TEXT,
                                    prenom_professeur TEXT,
                                    sexe_professeur TEXT,
                                    tel_professeur TEXT,
                                    email_professeur TEXT
                            )""")
        self.conn.commit()

    def verify_code_professeur(self, code_prof):
        """Verifier si le professeu est enregistrer."""
        SQL = "SELECT * FROM Professeurs WHERE code_professeur = ? "
        self.cursor.execute(SQL, (code_prof,))
        return self.cursor.fetchone() is not None

    def verify_professeur(self, prenom_prof, nom_prof):
        """Verifier si le professeur existe dans la base de donnees."""
        SQL = "SELECT * FROM Professeurs WHERE \
        prenom_professeur = ? AND nom_professeur = ?"
        self.cursor.execute(SQL, (prenom_prof, nom_prof))
        return self.cursor.fetchone() is not None

    def enregistrer(self, professeur):
        """Enregistrer les professeurs."""
        self.cursor.execute("SELECT * FROM \
        Professeurs WHERE code_professeur =?", (professeur.code_professeur,))
        professeur_trouve = self.cursor.fetchone()
        if professeur_trouve:
            print("Ce professeur est déjà enregistré...!")
        else:
            SQL = """INSERT INTO Professeurs (code_professeur, nom_professeur,
            prenom_professeur, sexe_professeur,
            tel_professeur, email_professeur)
                     VALUES (?, ?, ?, ?, ?, ?)"""
            self.cursor.execute(SQL, (professeur.code_professeur,
                                      professeur.nom_professeur,
                                      professeur.prenom_professeur,
                                      professeur.sexe_professeur,
                                      professeur.tel_professeur,
                                      professeur.email_professeur))
            self.conn.commit()
            print("Enregistrement réussi!")
        pause()

    def afficher(self):
        """Afficher les professeurs."""
        self.cursor.execute("SELECT * FROM Professeurs")
        tous_professeurs = self.cursor.fetchall()
        if tous_professeurs:
            for professeur in tous_professeurs:
                print(f"\nCode Professeur : {professeur[0]}")
                print(f"Nom Professeur : {professeur[1]}")
                print(f"Prénom Professeur : {professeur[2]}")
                print(f"Sexe Professeur : {professeur[3]}")
                print(f"Tel Professeur : {professeur[4]}")
                print(f"Email Professeur : {professeur[5]}")
        else:
            print("Aucune donnée")
        pause()

    def rechercher(self, code_professeur):
        """Rechercher un professeur."""
        self.cursor.execute("SELECT * FROM \
        Professeurs WHERE code_professeur=?", (code_professeur,))
        professeur = self.cursor.fetchone()
        if professeur:
            print("----------Votre professeur---------")
            print(f"\nCode Professeur : {professeur[0]}")
            print(f"Nom Professeur : {professeur[1]}")
            print(f"Prénom Professeur : {professeur[2]}")
            print(f"Sexe Professeur : {professeur[3]}")
            print(f"Tel Professeur : {professeur[4]}")
            print(f"Email Professeur : {professeur[5]}")
        else:
            print("Aucun professeur avec ce code")
        pause()

    def supprimer(self, code_professeur):
        """Supprimer un professeur."""
        self.cursor.execute("SELECT * FROM \
        Professeurs WHERE code_professeur=?", (code_professeur,))
        professeur = self.cursor.fetchone()
        if professeur:
            self.cursor.execute("DELETE FROM \
            Professeurs WHERE code_professeur=?", (code_professeur,))
            self.conn.commit()
            print("Suppression avec succès...!")
        else:
            print("Aucun professeur avec ce code.")
        pause()

    def fermer_connexion(self):
        """Close database."""
        self.conn.close()


def menu_professeur():
    """Fonction menu principal."""
    while True:
        effacer_ecran()
        print("*************************************")
        print("* Menu Gestion Professeur *")
        print("*************************************")
        print("1. Pour Enregistrer un Professeur")
        print("2. Pour Afficher les Professeurs")
        print("3. Pour Rechercher un Professeur")
        print("4. Pour Supprimer un Professeur")
        print("5. Pour quitter le Menu")
        choix = input("Que voulez-vous faire ? Veuillez choisir un numéro : ")
        try:
            choix_principal = int(choix)
            if 1 <= choix_principal <= 5:
                return choix_principal
            # else:
            print("Choisir un nombre entre 1 et 5")
            pause()
        except ValueError:
            print("Choisir un nombre entre 1 et 5")
            pause()


def pour_enregistrer():
    """Fonction qui permet d'enregistrer un professeur."""
    auth = Gestion_authentification(db_name)
    verify = auth.verifier_authentifier()
    if verify:
        nom = input_texte("Entrez le nom du professeur: ").capitalize()
        prenom = input_texte("Entrez le prénom du professeur: ").capitalize()
        sexe = input_sexe("Entrez le sexe du professeur (M ou F): ")
        tel = get_valid_phone_number()
        code = (f"{prenom[:3]}-{nom[:3]}-{sexe}-{tel[3:6]}").lower()
        email = get_valid_email()
        professeur = Professeurs(code, nom, prenom, sexe, tel, email)
        gestion_professeurs = Gestion_professeurs(db_name)
        gestion_professeurs.enregistrer(professeur)
        gestion_professeurs.fermer_connexion()
    else:
        print("Vous n'etes pas un authentifier...")
        pause()


def input_texte(prompt):
    """Fonction permet de verifier \
le nom et prenom du professeur et d'autres champ de texte."""
    while True:
        texte = input(prompt)
        if texte.isalnum() and texte[0].isalpha():
            return texte
        # else:
        print("ce champ doit contenir \
uniquement des lettres(au commencement) et des chiffres.")
        pause()


def input_sexe(prompt):
    """Fonction permettant de verifier si input sexe est correcte."""
    while True:
        sexe = input(prompt).upper()
        if sexe in ["M", "F"]:
            return sexe
        # else:
        print("Le sexe doit être M ou F.")
        pause()


def get_valid_email():
    """Fonction permet de verifier un email avec une expression reguliere."""
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    while True:
        effacer_ecran()
        email = input("Entrez un email valide : ")
        if re.fullmatch(regex, email):
            return email
        # else:
        print("Email invalide. Veuillez réessayer.")
        pause()


def get_valid_phone_number():
    """Fonction permet de verifier un numero de \
telephone avec une expression reguliere."""
    haiti_phone_regex = r'^[2-5][0-9]{7}$'
    while True:
        effacer_ecran()
        tel = input("Veuillez entrer votre numéro de téléphone : +509 ")
        if re.match(haiti_phone_regex, tel):
            return f"+509 {tel}"
        # else:
        print(f"{tel} n'est pas un numéro de \
téléphone valide. Veuillez réessayer.")
        pause()


def pour_afficher():
    """Fonction permettant d'afficher les professeurs."""
    gestion_professeurs = Gestion_professeurs(db_name)
    gestion_professeurs.afficher()
    gestion_professeurs.fermer_connexion()


def pour_rechercher():
    """Fonction permettant de rechercher un professeur."""
    code_professeur = input("Entrez le code du professeur: ").lower()
    gestion_professeurs = Gestion_professeurs(db_name)
    gestion_professeurs.rechercher(code_professeur)
    gestion_professeurs.fermer_connexion()


def pour_supprimer():
    """Fonction permettant de supprrimer un professeur."""
    g = Gestion_authentification(db_name)
    verify = g.verifier_authentifier()
    if verify:
        code_professeur = input("Entrez le code du professeur \
à supprimer: ").lower()
        gestion_professeurs = Gestion_professeurs(db_name)
        gestion_professeurs.supprimer(code_professeur)
        gestion_professeurs.fermer_connexion()
    else:
        print("ID et/ou mot de passe incorrect")
        pause()


def main_professeur():
    """Cette fonction permet la gestion des \
differentes fonctionalites de ce module."""
    while True:
        effacer_ecran()
        menu = menu_professeur()
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
#     main_professeur()
