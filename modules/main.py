"""Le module principal du projet."""

from authentification import main_authentification, effacer_ecran, pause
from batiments import main_batiment
from salles import main_salle
from professeurs import main_professeur
from cours import main_cours
from horaires import main_horaire

design = """
***************************************
*                                     *
*      C H C L  PROJET FINAL          *
*                                     *
***************************************
*                                     *
*       PROGRAMMATION PYTHON          *
*                                     *
"""


def menu_principal():
    """Fonction menu principal."""
    while True:
        effacer_ecran()
        print(design, end="")
        print("***************************************")
        print("*  BIENVENUE DANS LE MENU PRINCIPAL   *")
        print("*           DU PROGRAMME              *")
        print("***************************************")
        print("\n1. Pour Gestion des authentifiers")
        print("2. Pour Gestion des Batiments")
        print("3. Pour Gestion des Salles")
        print("4. Pour Gestion des professeurs")
        print("5. Pour Gestion des Cours")
        print("6. Pour Gestion des Horaire")
        print("7. Pour Quitter")
        choix = input("Que voulez-vous faire ? Veuillez choisir un numéro : ")
        try:
            choix_principal = int(choix)
            if 1 <= choix_principal <= 7:
                return choix_principal
            print("Choisir un nombre entre 1 et 7")
            pause()
        except ValueError:
            print("Choisir un nombre entre 1 et 7")
            pause()


def Gestion_menu_principal():
    """Fonction principal du projet qui permet \
d'appeler les differentes modules."""
    while True:
        choix = menu_principal()
        if choix == 1:
            main_authentification()
        elif choix == 2:
            main_batiment()
        elif choix == 3:
            main_salle()
        elif choix == 4:
            main_professeur()
        elif choix == 5:
            main_cours()
        elif choix == 6:
            main_horaire()
        else:
            print("Oups...!!! on va nous manquer , au revoir.")
            pause()
            break


if __name__ == "__main__":
    Gestion_menu_principal()
