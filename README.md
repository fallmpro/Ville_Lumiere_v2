# PROJET API : Ville Lumière
**Mathys SOUSA, Mohammed FALL, Mehdi TARCHOUL, Jeyron JEYARAJ**

![Mon image](./img/logo_SL1.jpg)

## C'est quoi le projet ?  

C'est un projet qu'on a réalisé lors de notre BTS SIO, plus précisément en 2ème année, Une **API** est une interface qui permet à des logiciels de communiquer en échangeant des données ou des fonctionnalités.

On a utilisé une API déjà existante gratuite "API-FOOTBALL", sur le thème du football car dans notre groupe on est tous des fans et c'est ce lien qui nous a réuni à faire le projet ensemble.

Le championnat français de football, Ligue 1, est l'une des compétitions les plus suivies dans le monde du sport. Ce projet vise à créer une plateforme d'information dédiée à la Ligue 1 pour offrir aux fans, journalistes, et analystes un accès rapide et complet aux données et actualités du championnat.

Notre objectif est de récupérer les données de l'API football et les utiliser sur notre propre site web dans lequel vous pourrez retrouver ddes informations sur vos équipes de ligue 1, les résultats de matchs, classement du championnat, dernières actualité et une page quizz avec des petites questions sur le championnats !


## Fonctionnalités

- Actualités principales : Articles, interviews, rumeurs de transferts. = api_ligue/LUN/templates/home.html à partir de la ligne 28 // On y trouve sur le site les dernières actualités sur la Ligue 1 
- Classement du championnat = api_ligue/LUN/templates/ranking.html  // un classement des équipes de l'équipe qui a le plus de points a celle qui en a le moins
- Recherche d'une équipe avec informations générales: Matchs, scores et dates = api_ligue/LUN/templates/equipes.html //  On y trouve une zone de texte pour rechercher une équipe et ensuite vous aurez les matchs qu'ils ont réalisés avec la date.
- Quizz : par rapport à un match = api_ligue/LUN/templates/quizz.html // Sur le site, on y retrouve des questions où tu peux essayer d'y répondre.
- Favoris : Mettre des équipes en favoris, on ajoute depuis la page classement = api_ligue/LUN/templates/ranking.html à partir de la ligne 31 // On y trouve la fonctionnalité de mettre en favoris une équipe en s'étant connecté au préalable.
- Résultat : Voir les résultats du championnat = api_ligue/LUN/templates/football_resulats.html // on y trouve les résultat des matchs de la ligue 1, en partant du dernier match au premier

## Fonctionnalités non faisable

- Résultat en direct pour les matchs 
- Biographie des joueurs
- Marché des transferts
- Détail sur les buteurs des matchs
- API sur les derniers matchs d'actualité, on a pu récupéré que ceux de 2023.

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
- Django

### Commandes à exécuter 
Dans un terminal bash dans visual studio code, il faut installer "pymysql" avec cette commande : 
- `$ pip3 install pymysql`
- On changera de dossier pour accéder au code :
- `cd api_ligue/`
- `py manage.py runserver`
- Si problème avec la base de donnée faire ça : 
-  `python manage.py import_football_data`

### BDD 
Base de donnée hébergé dans Alwaysvdata, il n'y a rien besoin de faire à ce propos.

### Démarrage du projet
Pour démarrer le projet il ne reste qu'a utiliser cette commande dans le terminal bash :
- `cd api_ligue/`
- `py manage.py runserver`

