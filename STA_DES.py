import timeit
import time
from prettytable import PrettyTable
from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes

def pad(data):  #fonction qui remplit automatiquement le mdp pour ensuite appliquer le chiffrement DES
    block_size = DES.block_size
    padding_size = block_size - len(data) % block_size #ca calcule le remplissage nécessaire en obtenant le reste de la divsion euclidienne
    padding = bytes([padding_size]) * padding_size #on applique le remplissage avec la taille nécessaire
    return data + padding

def encryptDES(data, key): #fonction de chiffrement DES, elle applique la méthode classique des 16 rounds
    data = pad(data)
    iv = get_random_bytes(DES.block_size)  #initialization vector : il est totalement arbitraire et se multiple avec un XOR aux parties du mot en clair
    cipher = DES.new(key, DES.MODE_CBC, iv) #On génère une encryption avec le mode CBC et en prenant les IV
    encrypted = iv + cipher.encrypt(data)
    return encrypted

def decryptDES(encrypted_data, key):  #fonction inverse au chiffrement DES, elle utilise la même clé d'où le fait que le déchiffrement est instantané
    iv = encrypted_data[:DES.block_size]
    cipher = DES.new(key, DES.MODE_CBC, iv) #on amorce le déchiffrement
    decrypted = cipher.decrypt(encrypted_data[DES.block_size:]) #le résultat redonne le mot de passe en clair
    return decrypted

def staAttack(mdp_to_attack, key, encryption_time_list): #fonction de STA
    charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    mdp_length = len(mdp_to_attack)
    encryption_de_mdp = encryptDES(mdp_to_attack.encode(), key) #on appelle la fonction de chiffrement

    # on initialise des variables et listes vides qu'on remplira au fur et à mesure de l'attaque pour déduire des mesures de temps etc.
    mdpCracked = ''
    total_time_of_attack = 0
    charactersList = []
    timeList = []

    for i in range(mdp_length):
        start_time = timeit.default_timer()  #Pour chaque caractère, on va mesurer le temps pris pour exécuter l'attaque
        found = False          #la variable nous dit si le mot de passe a bien été trouvé ou non, ici on l'initialise
        for char in charset:
            time.sleep(0.1)   #Je fais exprès de freiner l'attaque de temps pour avoir des temps visibles
            try:
                #if char ==  encryption_de_mdp[i:i+1].decode(): ne fonctionne pas sans déchiffrer...
                if char == decryptDES(encryption_de_mdp, key)[i:i+1].decode():  #POUR SIMPLIFIER le processus et épargner des erreurs ou boucles infinies,
                                                                                # On force le déchiffrement avec la même clé en appelant la fonction dédiée
                    mdpCracked += char
                    found = True
                    end_time = timeit.default_timer()     #comme l'autre programme, on mesure les temps pris avant de passer au prochain caractère
                    time_taken = end_time - start_time    # On mesure une fois de plus la différence de temps et on l'ajoute dans la liste et temps total
                    total_time_of_attack += time_taken
                    charactersList.append(char)
                    timeList.append(f"{time_taken:.6f}")
                    encryption_time_list.append(encryption_time_list[i]) #on ajoute à la liste le caractère correspondant
                    print(mdpCracked)
                    break
            except UnicodeDecodeError:
                continue

        if not found:
            mdpCracked += "-"

        if mdpCracked == mdp_to_attack: #La boucle s'arrête si cohérence, sinon elle continue d'essayer de deviner les caractères même si c'est incorrect
            break

    #print(f"\nMDP cracké: {mdpCracked}")
    print(f"\nMot de passe trouvé en : {total_time_of_attack:.6f} secondes") #on met une précision de 6 chiffres apès la virgule

    attack_table = PrettyTable() #on créé un tableau qui résumera les temps pris STA pour trouver chaque caractère un par un
    #attack_table.field_names = ["Caractere", "Temps", "Temps de chiffrement"]
    attack_table.field_names = ["Caractère", "Temps associé"]
    for char, time_taken in zip(charactersList, timeList): #on associe dans des lignes le caractère trouvé et son temps respectif de recherche
        attack_table.add_row([char, time_taken])

    print("\nTemps pris pour chaque caractère :")
    attack_table.align = "r"
    print(attack_table) #On affiche le 2ème tableau

    #On veut savoir quel caractère a mis le plus de temps à être trouvé parmi la liste
    longest_time_value = max(float(time_taken) for time_taken in timeList)
    char_with_longest_time = charactersList[timeList.index(f"{longest_time_value:.6f}")]  #on recherche le caractère associé au temps le plus long
    print(f"\nLe Caractère '{char_with_longest_time}' a été le plus long à trouver: {longest_time_value:.6f} secondes") #on met une précision de 6 chiffres apès la virgule

    return mdpCracked

if __name__ == "__main__":
    mdp_to_attack = input("Entrer le mot de passe à attaquer : ") #On récupère la saisie utilisateur
    encryption_key_generation = get_random_bytes(DES.block_size) #on génère la clé
    encryption_time_list = []  # On crée une liste qui regroupe les temps de chiffrement avec DES

    print(f"Clé de chiffrement: {encryption_key_generation}")
    print("Chiffrement DES en cours...")
    encrypted_chars_list = []  #liste qui rassemble tous les caractères lorsqu'ils sont chiffrés avec la clé
    for char in mdp_to_attack:
        encrypted_time = timeit.timeit(lambda: encryptDES(char.encode(), encryption_key_generation), number=1) #on utilise timeit car la librairie basique n'est pas précise pour le temps
        encryption_time_list.append(f"{encrypted_time:.6f}") #on ajoute à la liste le temps de chaque caractère
        encrypted_data = encryptDES(char.encode(), encryption_key_generation) #on applique la fonction de chiffrement à la clé + caractère en question
        encrypted_chars_list.append(encrypted_data.hex())  # On convertit en hexadécimal les valeurs de chiffrement

    print("\nTable de temps et caractères lors du chiffrement :")
    encryption_table = PrettyTable() #on créé un tableau visuel qui rassemblera les listes liées au chiffrement avant l'attaque
    encryption_table.field_names = ["Caractère", "Temps de chiffrement", "Caractère chiffré en bloc"]
    for char, enc_time, enc_char in zip(mdp_to_attack, encryption_time_list, encrypted_chars_list):
        encryption_table.add_row([char, enc_time, enc_char])  #on ajoute au tableau des lignes avec les paramètres (quel caractère, temps, versions chiffrée)

    encryption_table.align = "r"   #on aligne à la droite les résultats du tableau
    print(encryption_table) #On affiche le 1er tableau

    print("\nLançement de l'attaque STA...")
    startAttack = staAttack(mdp_to_attack, encryption_key_generation, encryption_time_list)  #On appelle la fonction d'attaque STA sur la variable de mdp

    print(f"Le mot de passe était bien : {startAttack}")
    "mdpCracked = staAttack(mdp)"