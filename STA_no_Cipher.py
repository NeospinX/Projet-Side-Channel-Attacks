import time
from prettytable import PrettyTable

def staAttack(mdp): #fonction de STA
    charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    # on initialise des variables et listes vides qu'on remplira au fur et à mesure de l'attaque pour déduire des mesures de temps etc.
    mdp_length = len(mdp)
    mdpCracked = ''
    total_time_of_attack = 0
    charactersList = []
    timeList = []

    for i in range(mdp_length):
        start_time = time.time() #Pour chaque caractère, on va mesurer le temps pris pour exécuter l'attaque
        for char in charset:
            time.sleep(0.1) #Je fais exprès de freiner l'attaque de temps pour avoir des temps visibles
            if char == mdp[i]: #Si correspondance, on mesure
                mdpCracked += char
                end_time = time.time() #on mesure les temps pris avant de passer au prochain caractère
                time_taken_for_particular_character = end_time - start_time # On mesure la différence de temps et on l'ajoute dans la liste et temps total
                total_time_of_attack += time_taken_for_particular_character
                charactersList.append(char)
                timeList.append(f"{time_taken_for_particular_character:.6f}") #on ajoute aux listes le caractère en question et son temps associé
                print(mdpCracked)
                break

    attack_table = PrettyTable() #on créé un tableau qui résumera les temps pris STA pour trouver chaque caractère un par un
    attack_table.field_names = ["Caractères", "Temps associés"]
    for char, time_taken_for_particular_character in zip(charactersList, timeList):
        attack_table.add_row([char, time_taken_for_particular_character]) #on associe dans des lignes le caractère trouvé et son temps respectif de recherche
    print("\nTemps pris pour les caractères:")
    attack_table.align = "r"
    print(attack_table) #On affiche le tableau

    # On veut savoir quel caractère a mis le plus de temps à être trouvé parmi la liste
    longest_time_value = max(float(time_taken_for_particular_character) for time_taken_for_particular_character in timeList)
    char_with_longest_time = charactersList[timeList.index(f"{longest_time_value:.6f}")] #on cherche le temps le plus long et le caractère associé

    print(f"\nLe mot de passe a été trouvé: \033[31m {mdpCracked}\033[0m")  #On affiche maintenant le mot de passe récupéré et les mesures de temps voulus
    print(f"Temps pris pour le déterminer: \033[92m {total_time_of_attack:.6f} seconds\033[0m")
    print(f"Le caractère '{char_with_longest_time}' a été le plus long à trouver: \033[36m{longest_time_value:.6f} seconds\033[0m") #On a une précision de 6 chiffres après la virgule

    return mdpCracked

if __name__ == "__main__":
    mdp = input("Entrez un mot de passe à attaquer: ") #On attend la saisie utilisateur avant de lancer l'attaque
    print("\033[0;31mLançement de l'attaque STA\033[0m")
    mdpCracked = staAttack(mdp)   #On appelle la fonction d'attaque et met en argument le mdp

