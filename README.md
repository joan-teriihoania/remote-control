# Remote control

[![N|Solid](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

[![Build Status](https://travis-ci.org/joan-teriihoania/remote-control.svg?branch=master)](https://travis-ci.org/joan-teriihoania/remote-control)

Créé par [Joan TERIIHOANIA](http://joan-teriihoania.fr/) en Janvier 2020. Contact par mail : joprocorp@gmail.com ou teriihoaniaheimanu@gmail.com.

Développé en plusieurs couches, remote-control est une architecture de console à distance sécurisé. Le système repose sur des applications client et serveur et dispose d'un serveur centralisé permettant l'échange sécurisé des données via un système d'enregistrement, de connexion et d'échange authentifié.

Les applications clientes et serveur d'arrivée sont développées en Python. Le serveur central d'échange est développé en NodeJS et ne sert qu'à la gestion de l'échange client-serveur. Ceux-ci s'échange grâce à une nomenclature utilisant une structure de donnée JSON et se base sur des requêtes GET afin de récupérer et poster des données au serveur central qui s'occupe de les redistribuer.

# Installation

## Prérequis
Il vous faut avoir installé [Python](https://www.python.org/).

## Client
Pour installer la console cliente de remote-control, il vous suffit de télécharger le fichier `client.py`. Il vous permettra d'accéder à une console type shell permettant d'entrer des commandes.

## Serveur
Pour installer un serveur **d'arrivée**, il vous suffit de télécharger le fichier `server.py`. Il vous permettra de lancer une instance de recueil et d'exécution des commandes envoyées à destination de ce serveur en particulier. Vous pouvez spécifier des identifiants de connexion spécifiques.

> **Note :** Sous Windows, il est possible d'exécuter une instance du script `server.py` en boucle afin d'éviter tout crash serveur. Le fichier `server.bat` est un fichier de commande batch sous Windows qui, une fois lancé, instanciera un serveur d'arrivée et le relancera automatiquement en boucle si celui-ci venait à crasher.

# Fonctionnement
Comme cité plus haut, remote-control se base sur un système d'échange centralisé. L'architecture dispose en tout de 3 composants principaux : *client, serveur central, serveur d'arrivée*. Le client et le serveur d'arrivée sont les seuls outils à disposition des utilisateurs finaux. Le serveur central est un système mis gratuitement à la disposition des utilisateurs qui sert de lien entre les clients et les serveurs, néanmoins, son code source est disponible si besoin (**ajouter le lien ici**).

> **Note :** Il est possible de mettre en place remote-control sur un réseau local tant que celui-ci dispose des dispositifs nécessaires dont une architecture réseau connecté ainsi que d'une instance NodeJS du serveur central.

*Les échanges de données entre le client, le serveur central et le serveur d'arrivée sont faits via des requêtes GET et les données transférées sont structurées en JSON.*

## Serveur central
Le serveur central est une application NodeJS qui fonctionne en permanence et est disponible via une URL ou une IP accessible publiquement ou non (en fonction de l'étendu du réseau concerné par remote-control). Les clients postent leurs messages au serveur central qui les transfert aux serveurs d'arrivée et vice-versa.

L'application NodeJS du serveur central et le package express intégré permettent de contrôler les sessions de chaque instance souhaitant accéder aux données du serveur. Chaque session possédant un identifiant, il est ainsi possible de traquer les différents accès et vérifier les autorisations affectées de chacun d'entre eux.

## Client
Le client est une application Python locale lancé par un utilisateur. En démarrant, celle-ci doit se créer une session temporaire et se récupérer le token correspondant à cette session pour s'identifier auprès du serveur central. Pour cela, l'utilisateur doit, au lancement de l'application, entrer ses identifiants de connexion, sans quoi, le serveur central ne donnera aucun accès au client.

> **Note :** L'application stocke automatiquement le token envoyé de la session en cours. Lors du prochain lancement, elle tentera de s'authentifier via ce token pour voir s'il est toujours valable. Cette fonctionnalité a été intégrée dans le cas de fermetures involontaires de la fenêtre du client.

Une fois un token reçu et une session ouverte avec les accès correspondants, le client peut envoyer des requêtes au serveur central qui les relaiera au serveur d'arrivée correspondant. **Important : Une session inactive depuis plus de 5 minutes sera automatiquement fermée par le serveur central et sera inutilisable. La sortie volontaire de la console (via `quit remote`) ferme la session et la rend inutilisable.** Le serveur d'arrivée renverra une réponse via le serveur central. S'il ne répond pas dans le délais d'attente préétabli (15 cycles par défaut), le client considère qu'il n'y aura aucune réponse de la part du serveur et génèrera un rapport d'erreur (FAIL REPORT) avec des détails sur le statut de la requête.

> **Note :** Ce rapport d'erreur peut être soumis en tant qu'issue afin de reporter des erreurs qui ne sont pas normales et ne correspondent pas à un fonctionnement normal du système.

## Serveur d'arrivée
Le serveur d'arrivée est une application Python locale sur un environnement Windows (**Incompatibilité possible pour les environnements LINUX ou MAC**). Elle dispose d'un identifiant unique et utilisable par une instance recueillie par son administrateur vers le serveur central qui lui donne un accès spécial. Elle peut récupérer les demandes des utilisateurs, les exécuter et renvoyer les données résultantes au serveur central qui les redistribuera aux utilisateurs.

Elle dispose d'une commande spécifique `reboot` qui permet de redémarrer le serveur (**Important : Ne fonctionne que dans un environnement où le serveur est instancié en boucle via un script tel que `server.bat`**) et la commande `status` qui retourne des informations sur le statut du serveur, le répertoire ainsi que la date du dernier démarrage/redémarrage.