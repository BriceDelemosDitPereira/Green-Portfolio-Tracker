# Green-Portfolio-Tracker

## Les commandes pour la base de données avec Django

1. python manage.py makemigrations
    
    Vérifie ce qui a été ajouté dans models.py (ici les classes Investement et PortfolioTransaction). Après avoir vérifier les informations à l'intérieur, elle crée un "plan d'action" pour mettre à jour la base de données. Donc `Préparation des instructions`.

    Crée un fichier (dans : `api/migrations/` nommé : `0001_initial.py` car c'est le premier). Cela permet de voir si il y a un problème et aussi d'avoir une sauvegarde étape par étape de l'avancée de la BDD.

2. python manage.py migrate

    C'est un `exécuteur` qui prend les plans d'actions et les applique à la BDD.
    Dans ce projet la BDD est créé avec sqlite3 pour plus de facilité.

3. python manage.py createsuperuser

    On va stocker un utilisateur dans la table `auth_user` créé par migrate.
    Ce user a accès à l'interface admin de Django

4. python manage.py runserver

    Cela va permettre de lancer un serveur pour tester les précédentes commandes. Il sera lancé à cette adresse : `http://127.0.0.1:8000/admin/`.
    Le frontend visualisé est l'interface admin intégrée de Django (activée par défaut dans `INSTALLED_APS` avec `django.contrib.admin`).
    C'est une page auto-générée pour gérer la BDD.

Django fournit tout pour démarrer vite (auth, amdin, DB tools). Cela évite de coder from scratch comme avec Golang.

### Les systèmes de migration (petit rappel)

Une migration est une recette pour changer la BDD sans tout casser. Donc en python, on peut réaliser des migrations (ajouter une table, changer un champ, etc...) tout en versionnent les changements. Cela permet aussi d'assurer une db similaire à tout le monde.