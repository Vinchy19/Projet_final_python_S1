"""Module permettant de gerer les salles."""

import sqlite3
from os import system, name
from authentification import Gestion_authentification, effacer_ecran, pause
from batiments import Gestion_batiments


class Salle:
    """Classe pour créer l'instance des salles."""

    def __init__(self, code_salle, code_batiment, num_etage, statut):
        """Pour creer l'instance salle."""
        self.code_salle = code_salle
        self.code_batiment = code_batiment
        self.num_etage = num_etage
        self.statut = statut


db_name = "data/projet.db"


class Gestion_salle:
    """Classe pour la gestion des salles."""

    def __init__(self, db_name):
        """Pour creer l'instance de gestion des salles."""
        self.db_name = db_name
        self.connexion = sqlite3.connect(db_name)
        self.curseur = self.connexion.cursor()
        print('Connexion Assurée!')
        self.table_salle()

    def table_salle(self):
        """Création de la table salle."""
        SQL = """CREATE TABLE IF NOT EXISTS salles (
                    code_salle TEXT PRIMARY KEY,
                    code_batiment TEXT,
                    niveau INTEGER,
                    statut TEXT
                )"""
        self.curseur.execute(SQL)
        self.connexion.commit()

    def verify_salle(self, nom_salle):
        """Pour verifier si une salle est enregistrer."""
        SQL = "SELECT * FROM Salles WHERE code_salle = ?"
        self.curseur.execute(SQL, (nom_salle,))
        return self.curseur.fetchone() is not None

    def verify_statut_salle(self, id_salle):
        """Methode pour verifier le statut d'une salle."""
        effacer_ecran()
        SQL = "SELECT statut_salle FROM salles WHERE code_salle = ?"
        self.curseur.execute(SQL, (id_salle))
        return self.curseur.fetchone() is not None

    def enregistrer(self, salle):
        """Enregistrement des salles."""
        SQL = """SELECT * FROM salles WHERE code_salle= ?"""
        self.curseur.execute(SQL, (salle.code_salle,))
        salleTrouve = self.curseur.fetchone()
        if salleTrouve:
            print('Cette Salle est déjà enregistrée!')
            pause()
        else:
            SQL = "INSERT INTO salles (code_salle, code_batiment, niveau, statut) \
                VALUES (?, ?, ?, ?)"
            self.curseur.execute(SQL, (salle.code_salle,
            salle.code_batiment, salle.num_etage, salle.statut))
            self.connexion.commit()
            print('Enregistrement réussi!')
            pause()

    def afficher(self):
        """Affichage de toutes les salles enregistrées."""
        effacer_ecran()
        sql = "SELECT * FROM salles"
        self.curseur.execute(sql)
        salles = self.curseur.fetchall()
        if salles:
            for salle in salles:
                print(f"Code Salle : {salle[0]}")
                print(f"Code Bâtiment : {salle[1]}")
                print(f"Niveau : {salle[2]}")
                print(f"Statut : {salle[3]}")
                print('\n')
        else:
            print('Aucune salle enregistrée!')
        pause()

    def rechercher(self, codesalle):
        """Recherche une salle par son code."""
        SQL = "SELECT * FROM salles WHERE code_salle= ?"
        self.curseur.execute(SQL, (codesalle,))
        sallefind = self.curseur.fetchone()
        if sallefind:
            print(f'Code Salle : {sallefind[0]}')
            print(f'Code Bâtiment : {sallefind[1]}')
            print(f'Niveau : {sallefind[2]}')
            print(f'Statut : {sallefind[3]}')
        else:
            print(f'La salle {codesalle} n\'est pas enregistrée!')
        pause()

    def supprimer(self, codesalle):
        """Supprime une salle par son code."""
        effacer_ecran()
        SQL = """SELECT * FROM salles WHERE code_salle= ?"""
        self.curseur.execute(SQL, (codesalle,))
        salledel = self.curseur.fetchone()
        if salledel:
            SQL = "DELETE FROM salles WHERE code_salle= ?"
            self.curseur.execute(SQL, (codesalle,))
            self.connexion.commit()
            print(f'La salle {codesalle} a été supprimée avec succès!')
        else:
            print(f'La salle {codesalle} n\'est pas enregistrée!')
        pause()

    def qte_salle(self, niveau, batiment):
        """Vérifie si la quantité de salles d'un bâtiment pour un niveau spécifique est atteinte."""
        SQL = "SELECT COUNT(niveau) FROM salles WHERE niveau=? AND code_batiment= ?"
        self.curseur.execute(SQL, (niveau, batiment))
        result = self.curseur.fetchone()[0]
        return result == 6

    def fermer_connexion(self):
        """Ferme la connexion à la base de données."""
        self.connexion.close()


def effacer_ecran():
    """Efface l'écran."""
    system("cls" if name == "nt" else "clear")


def for_save():
    """Fonction permettant d'enregistrer les salles."""
    effacer_ecran()
    g = Gestion_authentification(db_name)
    if g.verifier_authentifier():
        while True:
            code_batiment = gbatiment()
            b = Gestion_batiments(db_name)
            verify = b.verify_batiment(code_batiment)
            if verify:
                niveau = niveauchoice()
                salle_ = Gestion_salle(db_name)
                if not salle_.qte_salle(niveau, code_batiment):
                    numero = choisir_numero_salle(niveau)
                    num = f'{niveau}0{numero}'
                    codesalle = f'{code_batiment}-{num}'
                    statut = 'N/A'
                    salle = Salle(codesalle, code_batiment, niveau, statut)
                    salle_.enregistrer(salle)
                else:
                    print(f'Toutes les salles du niveau {niveau} du bâtiment \
{code_batiment} ont déjà été enregistrées! Veuillez choisir un autre niveau')

                while True:
                    loop = input("Voulez-vous enregistrer \
une autre salle ? (Y/N): ").upper()
                    if loop in {"Y", "N"}:
                        break
                    print("Veuillez choisir Y/N")

                if loop == "N":
                    break
            else:
                print("Ce batiment n'est pas enregistré..")
                pause()
    else:
        print("ID et/ou mot de passe incorrect")
        pause()


def for_show():
    """Fonction pour afficher les salles enregistrer."""
    salle_ = Gestion_salle(db_name)
    salle_.afficher()


def for_search():
    """Fonction pour Rechercher une salle enregistrer."""
    codesalle = code_salle()
    salle_ = Gestion_salle(db_name)
    salle_.rechercher(codesalle)


def for_delete():
    """Fonction pour suprimmer une salle."""
    effacer_ecran()
    g = Gestion_authentification(db_name)
    if g.verifier_authentifier():
        codesalle = code_salle()
        salle_ = Gestion_salle(db_name)
        salle_.supprimer(codesalle)
    else:
        print("ID et/ou mot de passe incorrect")
        pause()


def batimentchoice():
    """Cette fonction permet de choisir un batiment \
pour faire une operation sur les salles."""
    print("*************************************")
    print("* Veuillez choisir un Bâtiment *")
    print("*************************************")
    print('1. A')
    print('2. B')
    print('3. C')
    print('4. D')
    while True:
        try:
            choix = int(input('Choisir le bâtiment de la salle: '))
            if 1 <= choix <= 4:
                break
            print("Choisir une valeur entre 1 et 4 !")
        except ValueError:
            print("Veuillez entrer un chiffre")
    return choix


def choisir_numero_salle(niveau):
    """Cette fonction permet de choisir le numero de la salle."""
    while True:
        print('*****************************')
        print('Choisir le numéro de la salle')
        print('*****************************')
        for i in range(1, 7):
            print(f'{i}. {niveau}0{i}')
        try:
            choix = int(input('Faire votre choix: '))
            if 1 <= choix <= 6:
                break
            print('Veuillez choisir entre 1 et 6')
        except ValueError:
            print('Veuillez entrer un entier')
    return choix


def code_salle():
    """Cette fonction permet de trouver le code de la salle."""
    effacer_ecran()
    bat = gbatiment()
    niveau = niveauchoice()
    print('*****************************')
    print('Veuillez choisir la salle')
    print('*****************************')
    for i in range(1, 7):
        print(f'{i}. {bat}-{niveau}0{i}')
    while True:
        try:
            choix = int(input('Faire votre choix: '))
            if 1 <= choix <= 6:
                code = f'{bat}-{niveau}0{choix}'
                break
            print('Veuillez choisir entre 1 et 6')
        except ValueError:
            print('Veuillez entrer un entier')
    return code


def gbatiment():
    """Cette fonction permet de retourner le batiment grace au numero choisi."""
    choice = batimentchoice()
    return ["A", "B", "C", "D"][choice - 1]


def niveauchoice():
    """Fonction permettant de choisir le niveau de la salle."""
    effacer_ecran()
    print("*************************************")
    print("* Veuillez choisir le niveau de la salle entre 1 à 3 *")
    print("*************************************")
    print('1. Pour choisir le niveau 1')
    print('2. Pour choisir le niveau 2')
    print('3. Pour choisir le niveau 3')
    while True:
        try:
            choix = int(input("Faire votre choix: "))
            if 1 <= choix <= 3:
                break
            print("Choisir une valeur entre 1 et 3 !")
        except ValueError:
            print("Veuillez entrer un chiffre")
    return choix


def menusalle():
    """Cette fonction permet de choisir ce \
que vous voulez faire dans la gestion des salles."""
    while True:
        effacer_ecran()
        print("*************************************")
        print("* Menu Gestion Salles *")
        print("*************************************")
        print("1. Pour Enregistrer une salle")
        print("2. Pour Afficher les salles")
        print("3. Pour Rechercher une salle")
        print("4. Pour Supprimer une salle")
        print("5. Pour quitter le Menu")
        try:
            choix = int(input("Faire votre choix: "))
            if 1 <= choix <= 5:
                break
            print("Choisir une valeur entre 1 et 5 !")
        except ValueError:
            print("Veuillez entrer un chiffre")
    return choix


def main_salle():
    """Cette fonction permet la gestion des \
differentes fonctionalites des salles."""
    while True:
        effacer_ecran()
        menu = menusalle()
        if menu == 1:
            for_save()
        elif menu == 2:
            for_show()
        elif menu == 3:
            for_search()
        elif menu == 4:
            for_delete()
        else:
            break


# if __name__ == "__main__":
#     main_salle()
