import random
import string
import re
import time
import matplotlib.pyplot as plt
from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes

def pad(data): #fonction qui remplit automatiquement le mdp en multiple de 8 pour ensuite appliquer le chiffrement DES sans problème de bytes
    block_size = DES.block_size
    padding_size = block_size - len(data) % block_size #Calcule le remplissage nécessaire en obtenant le reste de la divsion euclidienne
    padding = bytes([padding_size]) * padding_size  #Applique le remplissage avec la taille nécessaire
    return data + padding

def encryptDES(data, key): #fonction de chiffrement DES, elle applique la méthode classique des 16 rounds
    iv = get_random_bytes(DES.block_size) #initialization vector : il est totalement arbitraire et se multiple avec un XOR aux parties du mot en clair
    data = pad(data) #on appelle la fonction de remplissage avant de mettre le mot de passe dans l'algorithme
    cipher = DES.new(key, DES.MODE_CBC, iv) #On génère une encryption avec le mode CBC et en prenant les IV
    encrypted = iv + cipher.encrypt(data)
    return encrypted

def getUserInput(): #fonction permettant juste de vérifier qu'un msg a bien été saisi ou respecte les le charset définit
    msgListe = [] #Liste qui peut garder plusieurs msgListe différents écrits à la suite
    while True:
        msg = input("Entrez le msg ou appuyez sur Entrée pour terminer : ") #on attend la saisie utilisateur
        if not msg:
            break
        if re.match("^[A-Za-z0-9]+$", msg): #si le mdp respecte les conditions,
            msgListe.append(msg.encode())           #on peut alors convertir en bytes le msg et passer à la suite
        else:
            print("caractères autorisés : majuscules, minuscules ou chiffres")
    return msgListe

def spaAttack(data): #fonction de l'attaque Simple power Analysis
    # Initialisation de listes vides de traces et mesures de courant qui seront remplies au fur et à mesure
    traces = []
    mesures_courant = []

    start_time = time.time()

    for round_num in range(16): #Il aurait fallu que la boucle mesure les 16 rounds en théorie lors du chiffrement DES pour mesurer les temps etc.
        current_time = time.time()
        time_diff = (current_time - start_time) * 1e-3

        for block_num in range(8): #de même, cette boucle aurait du observer les 8 blocs de 64 bits chiffrés dans chaque round pendant le chiffrement
            power_consumption = random.uniform(0, 5)
            traces.append(power_consumption)
            #En dépit de valeurs exhaustives, les valeurs de puisssances et consommations sont ici totalement aléatoires
            current_measurement = random.uniform(-0.5, 2.5)
            mesures_courant.append(current_measurement)

    end_time = time.time()
    time_associated_power = [(t - start_time) * 1e-3 for t in range(len(traces))]  #on génère le nombre traces nécessaires pour associer les temps
    min_time = min(time_associated_power) #on cherche le temps exact où la 1ère mesure a été enregistrée
    time_associated_power = [t - min_time for t in time_associated_power]  #cette différence sert uniquement à afficher des temps "cohérents" après 0

    # l'attaque est censée effectuer ces observations pendant le chiffrement, ici nous manquons de réalisme
    # le but était de m'aider à visualiser l'attaque même si ce n'est en aucun cas réaliste

    return time_associated_power, traces, mesures_courant

key = get_random_bytes(DES.block_size)  #on appelle la fonction de la librairie pycryptodome
msgListe = getUserInput()  #on appelle la fonction de vérification de msgListe bien saisis
keyHexa = key.hex()
#print("Clé DES générée aléatoirement:", key)
print("Clé DES générée aléatoirement:", keyHexa)
time.sleep(1)

if not msgListe:
    print("Pas de message entré")
else:
    timeList = []  #On va créér des listes de traces, temps et mesures de courant qui seront utilisées dans un graphique de puissance
    tracesList = []
    mesures_de_courantList = []

    for msg in msgListe:
        encrypted_msg = encryptDES(msg, key)  #on chiffre avec la fonction dédiée
        time_associated_power, traces, mesures_courant = spaAttack(encrypted_msg)  #on appelle la fonction SPA pour avoir les valeurs retournés
        timeList.append(time_associated_power)
        tracesList.append(traces) #Pas utilisée
        mesures_de_courantList.append(mesures_courant) #on ajoute des valeurs déduites de l'attaques (même si les valeurs restent aléatoires)

    for i, (time_associated_power, traces, mesures_courant) in enumerate(
            zip(timeList, tracesList, mesures_de_courantList)):  #on reprend les données des listes pour générer un graphique de consommation
        plt.figure(figsize=(12, 6))
        # notez que les traces ne sont pas exploités dans le graphique, il aurait été utile d'en avoir plusieurs différentes pour avoir plus de précision

        plt.plot(time_associated_power, mesures_courant, label=f'msg {i + 1}', color='blue')
        plt.xlabel("Temps (µs)")
        plt.ylabel("Courant (µA)")
        plt.legend()

        """
        plt.subplot(2,1,1)
        plt.plot(time_associated_power, mesures_courant, label=f'msg {i + 1}', color='blue')
        plt.xlabel("Temps (µs)")
        plt.ylabel("Courant (µA)")
        plt.legend()

        plt.subplot(2, 1, 2)
        plt.plot(time_associated_power, mesures_courant, label=f'msg {i + 2}', color='red')
        plt.xlabel("Temps (µs)")
        plt.ylabel("Courant (µA)")
        plt.legend()
        """
        plt.tight_layout()
        plt.show()
