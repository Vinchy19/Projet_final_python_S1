"""Module Horaires."""

# Importation des modules nécessaires
import sqlite3

from authentification import Gestion_authentification, effacer_ecran, pause
from salles import Gestion_salle
from professeurs import Gestion_professeurs
from cours import Gestion_cours

db_name = "data/projet.db"

# Instanciation
auth = Gestion_authentification(db_name)
salle = Gestion_salle(db_name)
professeurs = Gestion_professeurs(db_name)
cours = Gestion_cours(db_name)


class Horaire:
    """Classe pour definir(creer) les horaires."""

    def __init__(self, code_horaire, code_salle, code_cours,
                 jours, heure_debut, heure_fin, statut,
                 code_prof, session, annee):
        """Creation de l'instance horaire."""
        self.code_horaire = code_horaire
        self.code_salle = code_salle
        self.code_cours = code_cours
        self.jours = jours
        self.heure_debut = heure_debut
        self.heure_fin = heure_fin
        self.statut = statut
        self.code_prof = code_prof
        self.session = session
        self.annee = annee


class Gestion_horaires:
    """Classe pour la gestion des horaires."""

    def __init__(self, db_name):
        """Creation de l'instance gestion des horaires."""
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.table_horaires()

    def table_horaires(self):
        """Creer la table Horaires."""
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Horaires (
                            code_horaire TEXT PRIMARY KEY,
                            code_salle TEXT,
                            code_cours TEXT,
                            jours TEXT,
                            heure_debut TEXT,
                            heure_fin TEXT,
                            statut TEXT,
                            code_prof TEXT,
                            session INTEGER,
                            annee INTEGER
                            )""")
        self.conn.commit()

    def horaire_chevauche(self, jour, heure_debut, heure_fin, exclusions=[]):
        """Vérifie si un horaire chevauche un autre horaire existant."""
        self.cursor.execute("""
            SELECT * FROM Horaires
            WHERE jours=? AND
                  ((heure_debut BETWEEN ? AND ?) OR
                   (heure_fin BETWEEN ? AND ?) OR
                   (? BETWEEN heure_debut AND heure_fin) OR
                   (? BETWEEN heure_debut AND heure_fin))
        """, (jour, heure_debut, heure_fin, heure_debut, heure_fin,
              heure_debut, heure_fin))
        horaires = self.cursor.fetchall()
        for horaire in horaires:
            if horaire[0] not in exclusions:
                return horaire
        return None

    def verifier_conflits(self, horaire):
        """Vérifie les conflits d'horaires pour un professeur, \
une salle, et un cours."""
        jour = horaire.jours
        heure_debut = horaire.heure_debut
        heure_fin = horaire.heure_fin
        code_prof = horaire.code_prof
        code_salle = horaire.code_salle
        code_cours = horaire.code_cours

        # Vérifier conflit pour le professeur
        conflit_prof = self.horaire_chevauche(jour, heure_debut,
                                              heure_fin, exclusions =
                                              [horaire.code_horaire])
        if conflit_prof and conflit_prof[7] == code_prof:
            return f"Conflit pour le professeur {code_prof} \
avec l'horaire {conflit_prof[0]}."

        # Vérifier conflit pour la salle
        conflit_salle = self.horaire_chevauche(jour, heure_debut,
                                               heure_fin, exclusions =
                                                [horaire.code_horaire])
        if conflit_salle and conflit_salle[1] == code_salle:
            return f"Conflit pour la salle {code_salle} avec l'horaire \
{conflit_salle[0]}."

        # Vérifier conflit pour le cours
        conflit_cours = self.horaire_chevauche(jour, heure_debut,
                                               heure_fin, exclusions=
                                               [horaire.code_horaire])
        if conflit_cours and conflit_cours[2] == code_cours and \
           conflit_cours[7] != code_prof:
            return f"Conflit pour le cours {code_cours} avec l'horaire \
{conflit_cours[0]}, enseigné par un autre professeur."

        self.cursor.execute("""
            SELECT * FROM Horaires
            WHERE code_cours = ? AND jours = ? AND code_prof != ?
                            AND code_horaire != ?
        """, (code_cours, jour, code_prof, horaire.code_horaire))
        conflit_faculte = self.cursor.fetchall()
        if conflit_faculte:
            return f"Conflit : Le cours {code_cours} est déjà attribué à \
un autre professeur dans la même faculté."
        return None

    def enregistrer_horaire(self, horaire):
        """Enregistre un nouvel horaire dans la base de données \
après vérification des conflits."""
        conflit = self.verifier_conflits(horaire)
        if conflit:
            print(conflit)
            return

        self.cursor.execute("""INSERT INTO Horaires (code_horaire,
                            code_salle, code_cours, jours, heure_debut,
                            heure_fin, statut,
                            code_prof, session, annee)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                            (horaire.code_horaire, horaire.code_salle,
                             horaire.code_cours, horaire.jours,
                             horaire.heure_debut, horaire.heure_fin,
                             horaire.statut, horaire.code_prof,
                             horaire.session, horaire.annee))
        self.conn.commit()
        print("Horaire enregistré avec succès.")

    def modifier_horaire(self, code_horaire, nouvelle_valeur):
        """Modifie un horaire existant dans la base de données \
après vérification des conflits."""
        conflit = self.verifier_conflits(nouvelle_valeur)
        if conflit:
            print(conflit)
            return

        self.cursor.execute("SELECT * FROM Horaires WHERE code_horaire=?",
                             (code_horaire,))
        horaire_trouve = self.cursor.fetchone()
        if horaire_trouve:
            self.cursor.execute("""UPDATE Horaires SET code_horaire=?,
                                code_salle=?, code_cours=?,
                                jours=?, heure_debut=?, heure_fin=?,
                                statut=?, code_prof=?,
                                session=?, annee=?
                                WHERE code_horaire=?""",
                                (nouvelle_valeur.code_horaire,
                                 nouvelle_valeur.code_salle,
                                 nouvelle_valeur.code_cours,
                                 nouvelle_valeur.jours,
                                 nouvelle_valeur.heure_debut,
                                 nouvelle_valeur.heure_fin,
                                 nouvelle_valeur.statut,
                                 nouvelle_valeur.code_prof,
                                 nouvelle_valeur.session,
                                 nouvelle_valeur.annee, code_horaire))
            self.conn.commit()
            print("Horaire modifié avec succès.")
        else:
            print("Horaire introuvable.")

    def afficher_horaires(self, filtre=None, valeur_filtre=None):
        """Affiche tous les horaires ou filtre par nom \
de cours, professeur ou salle."""
        if filtre and valeur_filtre:
            self.cursor.execute(f"SELECT * FROM Horaires\
                                 WHERE {filtre}=?", (valeur_filtre,))
        else:
            self.cursor.execute("SELECT * FROM Horaires")

        tous_horaires = self.cursor.fetchall()
        if tous_horaires:
            for horaire in tous_horaires:
                self.afficher_details_horaire(horaire)
        else:
            print("Aucun horaire trouvé.")

    def afficher_details_horaire(self, horaire):
        """Affiche les détails d'un horaire."""
        print("------------Votre horaire--------------")
        print(f"Code de l'horaire: {horaire[0]}")
        print(f"Nom de la salle : {horaire[1]}")
        print(f"Code du cours : {horaire[2]}")
        print(f"Jours : {horaire[3]}")
        print(f"Heure de début : {horaire[4]}")
        print(f"Heure de fin : {horaire[5]}")
        print(f"Statut : {horaire[6]}")
        print(f"Code du professeur : {horaire[7]}")
        print(f"Session : {horaire[8]}")
        print(f"Année : {horaire[9]}")
        print("------------------------------------------")

    def supprimer_horaire(self, code_horaire):
        """Supprime un horaire de la base de données."""
        self.cursor.execute("SELECT * FROM Horaires \
                             WHERE code_horaire=?", (code_horaire,))
        horaire_trouve = self.cursor.fetchone()
        if horaire_trouve:
            self.cursor.execute("DELETE FROM Horaires \
                                WHERE code_horaire=?", (code_horaire,))
            self.conn.commit()
            print("Horaire supprimé avec succès.")
        else:
            print("Horaire introuvable !")

    def __del__(self):
        """Close datbase."""
        self.conn.close()


# Instanciation
gestion_horaires = Gestion_horaires(db_name)


def menu_horaires():
    """Menu principal pour la gestion des horaires."""
    while True:
        effacer_ecran()
        print("*********************************************")
        print("*          Gestion des horaires           *")
        print("*                                         *")
        print("*  1 - Enregistrer un nouvel horaire       *")
        print("*  2 - Afficher tous les horaires          *")
        print("*  3 - Rechercher un horaire               *")
        print("*  4 - Modifier un horaire                 *")
        print("*  5 - Supprimer un horaire                *")
        print("*  6 - Quitter                             *")
        print("*********************************************")
        try:
            choix = int(input("Entrez votre choix : "))
            if choix in range(1, 7):
                return choix
            print("Choix invalide. Veuillez entrer un nombre entre 1 et 6.")
            pause()
        except ValueError:
            print("Choix invalide. Veuillez entrer un nombre.")
            pause()


def menu_rechercher():
    """Cette fonction permer de gere la recherche des horaires."""
    while True:
        effacer_ecran()
        print("***********************************************************")
        print("*                    Menu de recherche                   *")
        print("*                                                        *")
        print("*  1 -  Rechercher un horaire pour un cours               *")
        print("*  2 -  Rechercher un horaire pour un jour                *")
        print("*  3 -  Rechercher un horaire pour un professeur          *")
        print("*  4 -  Rechercher un horaire pour une salle pour un jour *")
        print("*  5 - Quitter                                            *")
        print("***********************************************************")
        try:
            choix = int(input("Entrez votre choix : "))
            if choix in range(1,  6):
                return choix
            print("Choix invalide. Veuillez entrer un nombre entre 1 et 5.")
            pause()
        except ValueError:
            print("Choix invalide. Veuillez entrer un nombre.")
            pause()


def menu_afficher():
    """Cette fonction permet de gerer f'affichage des \
horaires selon un filtre."""
    while True:
        effacer_ecran()
        print("********************************************************")
        print("*                      Menu afficher                  *")
        print("*                                                     *")
        print("*  1 -  Affficher horaire pour un cours                *")
        print("*  2 -  Affficher horaire pour un jour                 *")
        print("*  3 -  Affficher horaire pour un professeur           *")
        print("*  4 -  Affficher horaire pour une salle pour un jour  *")
        print("*  5 - Quitter                                         *")
        print("********************************************************")
        try:
            choix = int(input("Entrez votre choix : "))
            if choix in range(1,  6):
                return choix
            print("Choix invalide. Veuillez entrer un nombre entre 1 et 5.")
            pause()
        except ValueError:
            print("Choix invalide. Veuillez entrer un nombre.")
            pause()


def gestion_menu_afficher_ou_rechercher(menu):
    """Cette fonction permet de gerer le menu afficher ou rechercher."""
    while True:
        choix = menu
        if choix == 1:
            afficher_horaire_pour_cours()
            break
        if choix == 2:
            afficher_horaire_pour_jour()
            break
        if choix == 3:
            afficher_horaire_pour_professeur()
            break
        if choix == 4:
            afficher_horaire_pour_salle_pour_jour()
            break
        break


def afficher_horaire_pour_professeur():
    """Cette fonction permet afficher les horaires pour un professeur."""
    code_prof = input("Entrez le code du professeur : ").strip().lower()
    verify = professeurs.verify_code_professeur(code_prof)
    if verify:
        gestion_horaires.afficher_horaires(filtre="code_prof",
                                           valeur_filtre=code_prof)
    else:
        print("Ce professeur n'est pas enregistré.")
        pause()


def afficher_horaire_pour_jour():
    """Cette fonction permet afficher les horaires pour un jour."""
    jours = input("Entrez le jours : ").strip().lower()
    if jours in LISTE_JOURS:
        gestion_horaires.afficher_horaires(filtre="jours",
                                           valeur_filtre=jours)
    else:
        print("Jours invalides.")
        pause()


def afficher_horaire_pour_cours():
    """Cette fonction permet afficher les horaires pour un cours."""
    code_cours = input("Entrez le code du cours : ").strip().lower()
    verify = cours.verify_cours(code_cours)
    if verify:
        gestion_horaires.afficher_horaires(filtre="code_cours",
                                           valeur_filtre=code_cours)
    else:
        print("Ce cours n'est pas enregistré.")
        pause()


def afficher_horaire_pour_salle_pour_jour():
    """Cette fonction permet aafficher les \
horaires pour un jour d'une salle donnee."""
    code_salle = input("Entrez le code de la salle : ").strip().upper()
    verify = salle.verify_salle(code_salle)
    if verify:
        jours = input("Entrez le jours : ").strip().lower()
        if jours in LISTE_JOURS:
            gestion_horaires.cursor.execute("SELECT * FROM \
                                            Horaires WHERE code_salle=? \
                                            AND jours=?",
                                            (code_salle, jours))
            horaires = gestion_horaires.cursor.fetchall()
            if horaires:
                for horaire in horaires:
                    gestion_horaires.afficher_details_horaire(horaire)
            else:
                print("Aucun horaire trouvé pour cette salle et ce jour.")
                pause()
        else:
            print("Jours invalides.")
            pause()
    else:
        print("Cette salle n'est pas enregistrée.")
        pause()


# Fonctions spécifiques aux actions du menu
def enregistrer_horaire():
    """Enregistre un nouvel horaire dans la base de données."""
    verify = auth.verifier_authentifier()
    if verify:
        dict_ = collecter_informations_horaire()
        code_horaire = dict_["code_horaire"]
        code_salle = dict_["code_salle"]
        code_cours = dict_["code_cours"]
        jours = dict_["jours"]
        heure_debut = dict_["heure_debut"]
        heure_fin = dict_["heure_fin"]
        statut = dict_["statut"]
        code_prof = dict_["code_prof"]
        session = dict_["session"]
        annee = dict_["annee"]
        horaire = Horaire(code_horaire, code_salle, code_cours,
                          jours, heure_debut, heure_fin,
                          statut, code_prof, session, annee)
        try:
            gestion_horaires.enregistrer_horaire(horaire)
        except sqlite3.IntegrityError as e:
            print(f'il y une erreur: {e} ces informations sont \
similaires aux informations deja enregistrer.')
            pause()
        pause()
    else:
        print("Vous devez être administrateur \
pour effectuer cette opération.")
        pause()


LISTE_JOURS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi"]


def collecter_informations_horaire(fact = " ", factf = " "):
    """Cette fonction permet de collecter des \
informations pour les horaires."""
    def obtenir_heure_debut():
        """Cette fonction permet d'obtenir l'heure de debut."""
        while True:
            heure_debut = input(f"Entrez l{factf}heure \
de début (HH:MM) : ").strip()
            if len(heure_debut) == 5 and heure_debut[2] == ":" \
            and heure_debut[:2].isdigit() and heure_debut[3:].isdigit():
                return heure_debut
            print("Heure invalide.")
            pause()

    def obtenir_heure_fin(heure_debut):
        """Cette fonction permet d'obtenir l'heure de fin."""
        while True:
            heure_fin = input(f"Entrez l{factf}heure \
de fin (HH:MM) : ").strip()
            if len(heure_fin) == 5 and heure_fin[2] == ":" \
               and heure_fin[:2].isdigit() \
               and heure_fin[3:].isdigit():
                if heure_fin > heure_debut:
                    return heure_fin
                print("L'heure de fin doit être supérieure \
à l'heure de début.")
            else:
                print("Heure invalide.")
            pause()

    def obtenir_salle():
        """Cette fonction permet d'obtenir le code de la salle."""
        while True:
            code_salle = input(f"Entrez le{fact}nom \
de la salle : ").strip().upper()
            if salle.verify_salle(code_salle):
                return code_salle
            print("Cette salle n'est pas enregistrée.")
            pause()

    def obtenir_cours():
        """Cette fonction permet d'obtenir le cours."""
        while True:
            code_cours = input(f"Entrez le{fact}code \
du cours : ").strip().lower()
            if cours.verify_cours(code_cours):
                return code_cours
            print("Ce cours n'est pas enregistré.")
            pause()

    def obtenir_professeur():
        """Cette fonction permet d'obtenir  le code du professeur."""
        while True:
            code_prof = input(f"Entrez le{fact}code \
du professeur : ").strip().lower()
            if professeurs.verify_code_professeur(code_prof):
                return code_prof
            print("Ce professeur n'est pas enregistré.")
            pause()

    def obtenir_jours():
        """Cette fonction permet d'obtenir le jour."""
        while True:
            jours = input(f"Entrez le{fact}jours : ").strip().lower()
            if jours in LISTE_JOURS:
                return jours
            print("Jours invalides.")
            pause()


    def obtenir_statut():
        """Cette fonction permert d'obtenir le statut de la salle."""
        return "Occupee"

    def obtenir_session():
        """Cette fonction permet d'obetnir la Session."""
        while True:
            try:
                session = int(input(f"Entrez la{factf}session(1 ou 2) \
: ").strip())
                if session in [1, 2]:
                    return session
                print("Choisir 1 ou 2")
            except ValueError:
                print("Erreur: La session doit être un nombre \
entier(1 ou 2).")

    def obtenir_annee():
        """Cette fonction permet d'obetnir l'annee."""
        while True:
            try:
                annee = int(input(f"Entrez la{factf}année : ").strip())
                if 1000 <= annee <= 2024:
                    return annee
                print("L'annee doit compris entre 1000 et 2024")
            except ValueError:
                print("Erreur: L'année doit être un nombre \
entier entre 1000 et 2024.")

    dict_ = {}
    dict_["code_salle"] = obtenir_salle()
    dict_["code_cours"] = obtenir_cours()
    dict_["jours"] = obtenir_jours()
    dict_["heure_debut"] = obtenir_heure_debut()
    dict_["heure_fin"] = obtenir_heure_fin(dict_["heure_debut"])
    dict_["statut"] = obtenir_statut()
    dict_["code_prof"] = obtenir_professeur()
    dict_["session"] = obtenir_session()
    dict_["annee"] = obtenir_annee()
    code_horaire = (f"{dict_['code_salle'][:3]}-\
{dict_['code_cours'][:3]}-{dict_['jours'][:3]}-{dict_['session']}-\
{dict_['annee']}").lower()
    dict_["code_horaire"] = code_horaire
    return dict_


def modifier_horaire():
    """Modifie un horaire existant dans la base de données."""
    code_horaire = input("Entrez l'ID de l'horaire à \
modifier : ").strip().lower()
    verify = auth.verifier_authentifier()
    if verify:
        # Récupérer les informations actuelles de l'horaire
        gestion_horaires.cursor.execute("SELECT * FROM \
                                        Horaires WHERE \
                                        code_horaire=?", (code_horaire,))
        horaire_trouve = gestion_horaires.cursor.fetchone()
        if horaire_trouve:
            dict_ = collecter_informations_horaire(' nouveau ', ' nouvelle ')
            # Demander les {factf}s valeurs à l'utilisateur
            code_horaire = dict_["code_horaire"]
            code_salle = dict_["code_salle"]
            code_cours = dict_["code_cours"]
            jours = dict_["jours"]
            heure_debut = dict_["heure_debut"]
            heure_fin = dict_["heure_fin"]
            statut = dict_["statut"]
            code_prof = dict_["code_prof"]
            session = dict_["session"]
            annee = dict_["annee"]
            nouvelle_valeur = Horaire(code_horaire, code_salle, code_cours,
                                      jours, heure_debut, heure_fin,
                                      statut, code_prof, session, annee)
            gestion_horaires.modifier_horaire(code_horaire, nouvelle_valeur)
        else:
            print("Horaire introuvable.")
    else:
        print("Vous devez être administrateur pour effectuer \
cette opération.")
        pause()


def supprimer_horaire():
    """Supprime un horaire de la base de données."""
    verify = auth.verifier_authentifier()
    if verify:
        code_horaire = input("Entrez le code de l'horaire à \
supprimer : ").strip().lower()
        gestion_horaires.supprimer_horaire(code_horaire)
    else:
        print("Vous devez être administrateur pour effectuer \
cette opération.")
        pause()


def main_horaire():
    """Cette focntion permet la gestion \
des differentes parties de l'horaire."""
    while True:
        choix = menu_horaires()
        if choix == 1:
            enregistrer_horaire()
        elif choix == 2:
            gestion_menu_afficher_ou_rechercher(menu_afficher())
            pause()
        elif choix == 3:
            gestion_menu_afficher_ou_rechercher(menu_rechercher())
            pause()
        elif choix == 4:
            modifier_horaire()
            pause()
        elif choix == 5:
            supprimer_horaire()
            pause()
        elif choix == 6:
            print("Au revoir!")
            break
        else:
            print("Choix invalide.")
            pause()

# if __name__ == "__main__":
#     main_horaire()
