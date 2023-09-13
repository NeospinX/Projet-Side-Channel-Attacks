# Projet-Side-Channel-Attacks

<u>Installation</u>
Après avoir téléchargé les codes, installez la librairie pycryptodome sur votre IDE pour s'assurer que le programme puisse bien reprendre les modules proposés notamment encryptDES, decryptDES...

```bash
pip install pycryptodome
```


Vous trouverez les codes suivants
- STA_no_Cipher.py montre une Timing attack classique sans aucun procédé de chiffrement. C'est le niveau simple de l'attaque.
- STA_DES.py reprend le modèle du précédant en tentant d'ajouter des étapes de chiffrement DES avant de lancer une pseudo Timing attack.
- SPA_DES.py est un code qui reprend les fonctions de chiffrement et tente de retrouver la consommation de puissance avec du Simple Power Analysis. 

Rq: Notez que comme mentionné dans le rapport, les 2 derniers programmes ne sont pas réalistes ou fidèles à ce que l'on attendrait réellement. Ces codes ont été créé avec de l'aléatoire pour remplacer des véritables mesures mais cherchent à reproduire hyptothétiquement les actions d'un véritable hackeur. Autrement dit, c'est la visualisation globale et la structure de l'attaque que j'ai essayé de comprendre et les faire à ma manière. 

