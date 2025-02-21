# Sondages App

Ce projet est une application Flask de sondages permettant de créer, gérer et répondre à des sondages via une interface web. Les données sont stockées dans une base de données MongoDB.

## Endpoints disponibles

Voici la liste des endpoints disponibles dans l'application :

- **GET /**  
  Afficher la page d'accueil.

- **GET /sondages/list**  
  Récupérer la liste de tous les sondages.

- **GET /sondages/<poll_id>**  
  Afficher un sondage spécifique.

- **POST /sondages**  
  Créer un nouveau sondage.

- **PUT /sondages/<poll_id>**  
  Mettre à jour un sondage existant.

- **GET /sondages/edit/<poll_id>**  
  Afficher la page pour éditer un sondage spécifique.

- **DELETE /sondages/<poll_id>**  
  Supprimer un sondage.

- **POST /sondages/<poll_id>/answer**  
  Soumettre des réponses à un sondage.

- **GET /sondages/<poll_id>/reponses**  
  Afficher les réponses soumises pour un sondage spécifique.

## Comment remplir la base de données

1. Assurez-vous que MongoDB est en cours d'exécution sur votre machine.

2. Clonez ce dépôt et accédez au dossier du projet.

3. Ouvrez un terminal et lancez le script pour initialiser les données :

    ```bash
    python ./static/initDB.py
    ```

    Ce script va supprimer toutes les données existantes dans les collections `sondages` et `reponses`, puis insérer des sondages de test dans la base de données MongoDB.

4. Démarrez le serveur Flask avec la commande suivante :

    ```bash
    python app.py
    ```

    Le serveur sera accessible à l'adresse [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

## Liste des compétences et points techniques

### Backend

- [x] Connexion à MongoDB avec `pymongo`
- [x] Création de routes REST avec Flask
- [x] Gestion des erreurs et des exceptions dans Flask
- [x] CRUD des sondages
- [x] Réception des réponses aux sondages
- [x] Affichage des réponses aux sondages
- [x] Utilisation de `ObjectId` pour les identifiants MongoDB
- [x] Gestion des questions et réponses en format JSON

### Frontend

- [x] Affichage des sondages et des réponses avec Flask et `render_template`
- [x] Soumission des sondages via des requêtes HTTP POST avec `fetch`
- [x] Ajout dynamique de questions dans les formulaires avec JavaScript
- [x] Affichage des réponses avec une date

### Gestion de la base de données

- [x] Suppression et ajout de données dans MongoDB à l'initialisation
- [ ] Vérification des doublons dans la base de données (nom de sondage unique)
- [x] Insertion de réponses avec les IDs des questions correspondantes
