from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timezone

client = MongoClient("mongodb://localhost:27017/")
db = client["sondages_db"]
sondages_collection = db["sondages"]
reponses_collection = db["reponses"]

def initialize_data():
    try:
        sondages_collection.delete_many({})
        reponses_collection.delete_many({})

        sondages_data = [
            {
                "name": "One Piece",
                "questions": [
                    {
                        "_id": ObjectId(),
                        "title": "Parmi les suivants, quel est ton fruit du démon préféré ?",
                        "type": "qcm",
                        "reponses": ["Gomu Gomu no Mi", "Mera Mera no Mi", "Hie Hie no Mi", "Yami Yami no Mi"]
                    },
                    {
                        "_id": ObjectId(),
                        "title": "Parmi les personnages suivants, qui aimerais-tu voir rejoindre l'équipage de Luffy ?",
                        "type": "qcm",
                        "reponses": ["Shanks", "Trafalgar Law", "Nico Robin", "Boa Hancock", "Sabo"]
                    },
                    {
                        "_id": ObjectId(),
                        "title": "Quel est le personnage secondaire de One Piece que tu aimerais voir plus souvent ?",
                        "type": "ouverte",
                        "reponses": []
                    },
                    {
                        "_id": ObjectId(),
                        "title": "Quel est le combat de One Piece que tu trouves le plus épique ?",
                        "type": "ouverte",
                        "reponses": []
                    },
                    {
                        "_id": ObjectId(),
                        "title": "Si tu pouvais changer un événement majeur dans One Piece, lequel serait-ce et pourquoi ?",
                        "type": "ouverte",
                        "reponses": []
                    }
                ]
            },
            {
                "name": "League of Legends / Arcane",
                "questions": [
                    {
                        "_id": ObjectId(),
                        "title": "Quel est ton rôle préféré dans LoL ?",
                        "type": "qcm",
                        "reponses": ["Top", "Jungle", "Mid", "Bot", "Support"]
                    },
                    {
                        "_id": ObjectId(),
                        "title": "Quels changements aimerais-tu voir dans League of Legends à l'avenir ?",
                        "type": "ouverte",
                        "reponses": []
                    },
                    {
                        "_id": ObjectId(),
                        "title": "Quel personnage d'Arcane est ton préféré ?",
                        "type": "qcm",
                        "reponses": ["Vi", "Jinx", "Caitlyn", "Jayce", "Silco", "Mel"]
                    },
                    {
                        "_id": ObjectId(),
                        "title": "Penses-tu qu'Arcane a bien réussi à traduire l'univers de League of Legends en série animée ? Pourquoi ?",
                        "type": "ouverte",
                        "reponses": []
                    },
                    {
                        "_id": ObjectId(),
                        "title": "Si tu pouvais choisir un champion de League of Legends pour rejoindre l'univers d'Arcane, lequel serait-ce et pourquoi ?",
                        "type": "ouverte",
                        "reponses": []
                    }
                ]
            },
            {
                "name": "Les chats",
                "questions": [
                    {
                        "_id": ObjectId(),
                        "title": "Quel est ton type de chat préféré ?",
                        "type": "qcm",
                        "reponses": ["Persan", "Siamois", "Maine Coon", "Bengal", "Européen"]
                    },
                    {
                        "_id": ObjectId(),
                        "title": "Quel comportement de chat te fait le plus rire ?",
                        "type": "ouverte",
                        "reponses": []
                    },
                    {
                        "_id": ObjectId(),
                        "title": "Quel est le nom de ton chat ? Si tu n'en as pas, quel nom lui donnerais-tu ?",
                        "type": "ouverte",
                        "reponses": []
                    },
                    {
                        "_id": ObjectId(),
                        "title": "As-tu un chat chez toi ?",
                        "type": "qcm",
                        "reponses": ["Oui", "Non"]
                    },
                    {
                        "_id": ObjectId(),
                        "title": "Si tu pouvais adopter n'importe quel chat provenant d'un film ou d'une série, lequel choisirais-tu ?",
                        "type": "ouverte",
                        "reponses": []
                    }
                ]
            }
        ]

        for sondage in sondages_data:
            sondages_collection.insert_one(sondage)

        reponses_data = [
            {
                "poll_id": sondages_collection.find_one({"name": "One Piece"})["_id"],
                "submitted_at": datetime.now(timezone.utc),
                "responses": [
                    {"question_id": sondages_collection.find_one({"name": "One Piece"})["questions"][0]["_id"], "answer": "Gomu Gomu no Mi"},
                    {"question_id": sondages_collection.find_one({"name": "One Piece"})["questions"][1]["_id"], "answer": "Trafalgar Law"},
                    {"question_id": sondages_collection.find_one({"name": "One Piece"})["questions"][2]["_id"], "answer": "Trafalgar Law"},
                    {"question_id": sondages_collection.find_one({"name": "One Piece"})["questions"][3]["_id"], "answer": "Luffy vs. Usopp"},
                    {"question_id": sondages_collection.find_one({"name": "One Piece"})["questions"][4]["_id"], "answer": "La mort de Ace"}
                ]
            },
            {
                "poll_id": sondages_collection.find_one({"name": "League of Legends / Arcane"})["_id"],
                "submitted_at": datetime.now(timezone.utc),
                "responses": [
                    {"question_id": sondages_collection.find_one({"name": "League of Legends / Arcane"})["questions"][0]["_id"], "answer": "Bot"},
                    {"question_id": sondages_collection.find_one({"name": "League of Legends / Arcane"})["questions"][1]["_id"], "answer": "Une meilleure modération"},
                    {"question_id": sondages_collection.find_one({"name": "League of Legends / Arcane"})["questions"][2]["_id"], "answer": "Silco"},
                    {"question_id": sondages_collection.find_one({"name": "League of Legends / Arcane"})["questions"][3]["_id"], "answer": "Oui, la série traduit très bien l'univers, les personnages sont bien développés."},
                    {"question_id": sondages_collection.find_one({"name": "League of Legends / Arcane"})["questions"][4]["_id"], "answer": "Malphite ; il est dans les tréfonds de Zaun et pourrait ouvrir une intrigue sur le néant"}
                ]
            },
            {
                "poll_id": sondages_collection.find_one({"name": "Les chats"})["_id"],
                "submitted_at": datetime.now(timezone.utc),
                "responses": [
                    {"question_id": sondages_collection.find_one({"name": "Les chats"})["questions"][0]["_id"], "answer": "Maine Coon"},
                    {"question_id": sondages_collection.find_one({"name": "Les chats"})["questions"][1]["_id"], "answer": "Quand ils se cachent dans des boîtes"},
                    {"question_id": sondages_collection.find_one({"name": "Les chats"})["questions"][2]["_id"], "answer": "Mei-li et Youya"},
                    {"question_id": sondages_collection.find_one({"name": "Les chats"})["questions"][3]["_id"], "answer": "Oui"},
                    {"question_id": sondages_collection.find_one({"name": "Les chats"})["questions"][4]["_id"], "answer": "Le chat du Cheshire de Alice au pays des merveilles."}
                ]
            }
        ]

        for reponse in reponses_data:
            reponses_collection.insert_one(reponse)

        print("Données initialisées avec succès.")

    except Exception as e:
        print("Erreur lors de l'initialisation des données : ", e)

initialize_data()
