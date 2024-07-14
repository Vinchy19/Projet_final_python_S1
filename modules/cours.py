"""Module permettant la gestion des cours."""

import sqlite3
from random import randint
from authentification import Gestion_authentification, effacer_ecran, pause


db_name = "data/projet.db"


class Cours:
    """Classe pour creer l'instance des cours."""

    def __init__(self, code_cours, nom_cours, nom_faculte):
        """Creation de l'instance."""
        self.code_cours = code_cours
        self.nom_cours = nom_cours
        self.nom_faculte = nom_faculte


class Gestion_cours:
    """Classe pour la gestion des cours."""

    def __init__(self, db_name):
        """Creation de l'instance gestion cours."""
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.table_cours()

    def table_cours(self):
        """Craetion de la table cours."""
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Cours (
                            code_cours TEXT PRIMARY KEY,
                            nom_cours TEXT,
                            nom_faculte TEXT
                            )""")
        self.conn.commit()

    def verify_cours(self, code_cours):
        """Verifier si ce cours est deja enregister."""
        SQL = "SELECT * FROM Cours WHERE code_cours = ?"
        self.cursor.execute(SQL, (code_cours,))
        return self.cursor.fetchone() is not None

    def verify_cours_faculte(self, nom_cours, faculte):
        """Verifier le cours et la faculte."""
        SQL = "SELECT * FROM Cours WHERE nom_cours = ? AND nom_faculte = ?"
        self.cursor.execute(SQL, (nom_cours, faculte))
        return self.cursor.fetchone() is not None

    def enregistrer(self, cours):
        """Methode pour enregistrer les cours."""
        effacer_ecran()
        self.cursor.execute("SELECT * FROM \
            Cours WHERE code_cours=?", (cours.code_cours,))
        cours_trouve = self.cursor.fetchone()
        if cours_trouve:
            print("Ce cours est déjà enregistré...!")
        else:
            SQL = """INSERT INTO Cours (
                            code_cours,
                            nom_cours,
                            nom_faculte)
                    VALUES (?, ?, ?)"""
            self.cursor.execute(SQL,
                                (cours.code_cours,
                                 cours.nom_cours,
                                 cours.nom_faculte))
            self.conn.commit()
            print("Cours enregistré avec succès.")
        pause()

    def afficher(self):
        """Methode pour afficher les cours."""
        effacer_ecran()
        self.cursor.execute("SELECT * FROM Cours")
        tous_cours = self.cursor.fetchall()
        if tous_cours:
            for cours in tous_cours:
                print(f"Code du cours : {cours[0]}")
                print(f"Nom du cours : {cours[1]}")
                print(f"Nom de la faculté : {cours[2]}\n")
        else:
            print("Aucun cours enregistré.")
        pause()

    def rechercher(self, code_cours):
        """Methode pour rchercher un cours."""
        effacer_ecran()
        self.cursor.execute("SELECT * FROM\
            Cours WHERE code_cours=?", (code_cours,))
        cours_trouve = self.cursor.fetchone()
        if cours_trouve:
            print(f"Code du cours : {cours_trouve[0]}")
            print(f"Nom du cours : {cours_trouve[1]}")
            print(f"Nom de la faculté : {cours_trouve[2]}")
        else:
            print("Aucun cours trouvé avec ce code.")
        pause()

    def supprimer(self, code_cours):
        """Methode pour supprimer un cours."""
        effacer_ecran()
        self.cursor.execute("SELECT * FROM \
            Cours WHERE code_cours=?", (code_cours,))
        cours_trouve = self.cursor.fetchone()
        if cours_trouve:
            self.cursor.execute("DELETE FROM Cours\
                WHERE code_cours=?", (code_cours,))
            self.conn.commit()
            print("Cours supprimé avec succès.")
        else:
            print("Aucun cours trouvé avec ce code.")
        pause()

    def modifier(self, code_cours):
        """Methode pour modifier un cours."""
        effacer_ecran()
        self.cursor.execute("SELECT * FROM\
             Cours WHERE code_cours=?", (code_cours,))
        cours_trouve = self.cursor.fetchone()
        if cours_trouve:
            while True:
                choix = menu_modifier()
                if choix == 1:
                    self.modifier_nom_cours(cours_trouve)
                elif choix == 2:
                    self.modifier_nom_faculte(cours_trouve)
                elif choix == 3:
                    break
        else:
            print("Aucun cours trouvé avec ce code.")
            pause()

    def modifier_nom_cours(self, cours_trouve):
        """Methode permettant de modifier \
        le nom d'un cours deja enregistrer."""
        nom_cours = input("Entrer le nouveau nom du cours : ").capitalize()
        self.cursor.execute('''UPDATE Cours
                               SET nom_cours=?
                               WHERE code_cours=?''',
                            (nom_cours, cours_trouve[0]))
        self.conn.commit()
        print("Nom du cours mis à jour avec succès.")
        pause()

    def modifier_nom_faculte(self, cours_trouve):
        """Methode permettant de modifier \
la faculte d'un cours deja enregistrer."""
        nom_faculte = input("Entrer le nouveau nom de la faculté : ")
        self.cursor.execute('''UPDATE Cours
                               SET nom_faculte=?
                               WHERE code_cours=?''',
                            (nom_faculte, cours_trouve[0]))
        self.conn.commit()
        print("Nom de la faculté mis à jour avec succès.")
        pause()


def input_texte(prompt):
    """Fonction permet de verifier \
le nom cours et d'autres champ de texte."""
    while True:
        texte = input(prompt)
        if texte.isalnum() and texte[0].isalpha():
            return texte
        print("ce champ doit contenir \
uniquement des lettres(au commencement) et des chiffres.")
        pause()


def menu_modifier():
    """Menu pour modifier les cours enregistrer."""
    while True:
        effacer_ecran()
        print("*********************************************")
        print("*        Que voulez-vous modifier ?         *")
        print("*********************************************")
        print("1. Pour modifier le nom du cours")
        print("2. Pour modifier le nom de la faculté")
        print("3. Pour quitter")
        choix = input("Veuillez choisir un numéro : ")
        try:
            choix = int(choix)
            if 1 <= choix <= 3:
                break
            print("Veuillez choisir un nombre entre 1 et 3.")
        except ValueError:
            print("Choisir un entier entre 1 et 3.")
    return choix


def pour_enregistrer():
    """Fonction pour enregistrer les cours."""
    a = Gestion_authentification(db_name)
    verify_auth = a.verifier_authentifier()
    if verify_auth:
        # pour cours
        nom_cours = input_texte("Entrer le nom du cours : ").capitalize()
        # pour faculté
        faculte = input_texte("Entrer la faculté : ").capitalize()
        code = (f"{nom_cours[:3]}-{faculte[:3]}-\
{str(randint(100,999))}").lower()
        gcours = Gestion_cours(db_name)
        verify = gcours.verify_cours_faculte(nom_cours, faculte)

        if verify:
            print("Ce cours est deja enregistre pour cette faculte")
            pause()
        else:
            cours = Cours(code, nom_cours, faculte)
            gcours.enregistrer(cours)
    else:
        print("Mot de passe et/ou ID incorrect")
        pause()


def pour_afficher():
    """Pour afficher les cours."""
    c = Gestion_cours(db_name)
    c.afficher()


def pour_rechercher():
    """Pour afficher un cours."""
    c = Gestion_cours(db_name)
    code = input("Entrer le code du cours à rechercher : ").lower()
    c.rechercher(code)


def pour_supprimer():
    """Pour suprimer un cours."""
    a = Gestion_authentification(db_name)
    verify_auth = a.verifier_authentifier()
    if verify_auth:
        code = input("Entrer le code du cours à supprimer : ").lower()
        c = Gestion_cours(db_name)
        c.supprimer(code)
    else:
        print("Mot de passe et/ou ID incorrect")
        pause()


def pour_modifier():
    """Pour modifier un cours."""
    a = Gestion_authentification(db_name)
    verify_auth = a.verifier_authentifier()
    if verify_auth:
        code = input("Entrer le code du cours à modifier : ").lower()
        c = Gestion_cours(db_name)
        c.modifier(code)
    else:
        print("Mot de passe et/ou ID incorrect")
        pause()


def menu_cours():
    """Menu principal de gestion des cours."""
    while True:
        effacer_ecran()
        print("*************************************")
        print("*          Menu Gestion Cours       *")
        print("*************************************")
        print("1. Pour Enregistrer un Cours")
        print("2. Pour Afficher les Cours")
        print("3. Pour Rechercher un Cours")
        print("4. Pour Modifier un Cours")
        print("5. Pour Supprimer un Cours")
        print("6. Pour quitter le Menu")
        choixx = input("Que voulez-vous faire ?\
 Veuillez choisir un numéro : \n")
        try:
            choix_principal = int(choixx)
            if 1 <= choix_principal <= 6:
                break
            print("Choisir un entier entre 1 et 6.")
            pause()
        except ValueError:
            print("Choisir un entier entre 1 et 6.")
            pause()
    return choix_principal


def main_cours():
    """Menu pour la gestion des fontionalites de ce module."""
    while True:
        effacer_ecran()
        menu = menu_cours()
        if menu == 1:
            pour_enregistrer()
        elif menu == 2:
            pour_afficher()
        elif menu == 3:
            pour_rechercher()
        elif menu == 4:
            pour_modifier()
        elif menu == 5:
            pour_supprimer()
        else:
            break

# if __name__ == "__main__":
#     main_cours()
