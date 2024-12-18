# PROJET API : Ville Lumière
**Mathys SOUSA, Mohammed FALL, Mehdi TARCHOUL, Jeyron JEYARAJ**

![Mon image](./img/logo_SL1.jpg)

## C'est quoi le projet ?  

C'est un projet qu'on a réalisé lors de notre BTS SIO, plus précisément en 2ème année, Une **API** est une interface qui permet à des logiciels de communiquer en échangeant des données ou des fonctionnalités.

On a utilisé une API déjà existante gratuite, sur le thème du football car dans notre groupe on est tous des fans et c'est ce lien qui nous a réuni à faire le projet ensemble.

Le championnat français de football, Ligue 1, est l'une des compétitions les plus suivies dans le monde du sport. Ce projet vise à créer une plateforme d'information dédiée à la Ligue 1 pour offrir aux fans, journalistes, et analystes un accès rapide et complet aux données et actualités du championnat.

Notre objectif est de récupérer les données de l'API et les utiliser sur notre propre site web.


## Fonctionnalités

- Actualités principales : Articles, interviews, rumeurs de transferts. = api_ligue/LUN/templates/home.html à partir de la ligne 28
- Classement du championnat = api_ligue/LUN/templates/ranking.html
- Recherche d'une équipe avec informations générales: Matchs, scores et dates = api_ligue/LUN/templates/equipes.html
- Quizz : par rapport à un match 
- Favoris : Mettre des équipes en favoris 


## Contraintes
- Accées limités aux differentes API football, ceci est nottament dû au fait que la plupart des API sont payantes. 
- 100 Reqûetes par jour pour 4 personnes.
- Possible lancement de page lente pour récupérer un maximum d'info et cibler ensuite sur ce que l'utilisateur a besoin.

## Installation et paramettrage

### Les prérequis :
- Navigateur WEB 
- Compte Github
- Python
- SQL
- Visual Studio Code 

### Commandes à exécuter 
Dans le terminal on changera de dossier pour accéder au code :
- cd api_ligue/
- py manage.py runserver

### BDD 
Base de donnée hébergé dans Alwaysdata, il n'y a rien besoin de faire à ce propos.


