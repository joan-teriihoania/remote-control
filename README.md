# Remote control

[![N|Solid](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

[![Build Status](https://travis-ci.org/joan-teriihoania/remote-control.svg?branch=master)](https://travis-ci.org/joan-teriihoania/remote-control)

Développé en plusieurs couches, remote-control est une architecture de console à distance sécurisé. Le système repose sur des applications client et serveur et dispose d'un serveur centralisé permettant l'échange sécurisé des données via un système d'enregistrement, de connexion et d'échange authentifié.

Les applications clientes et serveur d'arrivée sont développées en Python. Le serveur central d'échange est développé en NodeJS et ne sert qu'à la gestion de l'échange client-serveur. Ceux-ci s'échange grâce à une nomenclature utilisant une structure de donnée JSON et se base sur des requêtes GET afin de récupérer et poster des données au serveur central qui s'occupe de les redistribuer.

# Installation
## Prérequis
Il vous faut avoir installé [Python](https://www.python.org/).
## Client
Pour installer la console cliente de remote-control, il vous suffit de télécharger le fichier `client.py`. Il vous permettra d'accéder à une console type shell permettant d'entrer des commandes.
## Serveur
Pour installer un serveur **d'arrivée**, il vous suffit de télécharger le fichier `server.py`. Il vous permettra de lancer une instance de recueil et d'exécution des commandes envoyées à destination de ce serveur en particulier. Vous pouvez spécifier des identifiants de connexion spécifiques.

**Note :** Sous Windows, il est possible d'exécuter une instance du script `server.py` en boucle afin d'éviter tout crash serveur. Le fichier `server.bat` est un fichier de commande batch sous Windows qui, une fois lancé, instanciera un serveur d'arrivée et le relancera automatiquement en boucle si celui-ci venait à crasher.