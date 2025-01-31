from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client["sondages_db"]
sondages_collection = db["sondages"]


# _____ Route acceuil _____

@app.route('/')
def index():
    return render_template('index.html')


# _____ Route polls _____

@app.route('/sondages/list')
def list_polls():
    try:
        polls = list(sondages_collection.find({}, {"_id": 1, "name": 1}))
        
        if not polls:
            return jsonify({"message": "No polls found"}), 404

        return render_template('polls.html', polls=polls)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# _____ Route poll _____

@app.route('/sondages/<poll_id>')
def show_poll(poll_id):
    try:
        poll = sondages_collection.find_one({"_id": ObjectId(poll_id)})
        
        if not poll:
            return jsonify({"message": "Poll not found"}), 404

        for question in poll.get("questions", []):
            question["_id"] = str(question["_id"])

        return render_template('poll.html', poll=poll)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# _____ Route création _____

@app.route('/sondages', methods=['POST'])
def create_poll():
    try:
        data = request.json
        name = data.get('name')
        questions = data.get('questions')

        if sondages_collection.find_one({"name": name}):
            return jsonify({"error": "Poll name already used"}), 400
        
        if not name or not questions:
            return jsonify({"error": "All fields required"}), 400

        formatted_questions = [
            {
                "_id": ObjectId(),
                "title": q.get("title"),
                "type": q.get("type"),
                "reponses": q.get("reponses", [])
            }
            for q in questions
        ]

        new_poll = {
            "name": name,
            "questions": formatted_questions
        }

        result = sondages_collection.insert_one(new_poll)

        return jsonify({"message": "Creation successfull of : " + str(name)}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# _____ Route consultation _____

@app.route('/sondages', methods=['GET'])
def get_polls():
    try:
        polls = list(sondages_collection.find({}, {"_id": 0}))
        
        for poll in polls:
            for question in poll.get("questions", []):
                question["_id"] = str(question["_id"])

        if not polls:
            return jsonify({"message": "No polls found"}), 404
        
        return jsonify(polls), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
# _____ Route update _____

@app.route('/sondages/<poll_id>', methods=['PUT'])
def update_poll(poll_id):
    try:
        print(f"Réception d'une requête PUT pour le sondage {poll_id}")

        data = request.json
        print("Données reçues :", data)

        name = data.get('name')
        questions = data.get('questions')

        if not name or not questions:
            return jsonify({"error": "Tous les champs sont requis"}), 400

        existing_poll = sondages_collection.find_one({"_id": ObjectId(poll_id)})
        if not existing_poll:
            return jsonify({"error": "Sondage non trouvé"}), 404

        existing_questions = {str(q["_id"]): q for q in existing_poll.get("questions", [])}
        
        formatted_questions = []
        for q in questions:
            question_id = q.get("_id")

            if question_id and question_id in existing_questions:
                formatted_questions.append({
                    "_id": ObjectId(question_id),
                    "title": q.get("title"),
                    "type": q.get("type"),
                    "reponses": q.get("reponses", [])
                })
            else:
                formatted_questions.append({
                    "_id": ObjectId(),
                    "title": q.get("title"),
                    "type": q.get("type"),
                    "reponses": q.get("reponses", [])
                })

        print("Questions formatées après suppression :", formatted_questions)

        result = sondages_collection.update_one(
            {"_id": ObjectId(poll_id)},
            {"$set": {"name": name, "questions": formatted_questions}}
        )

        if result.matched_count == 0:
            return jsonify({"message": "Sondage non trouvé"}), 404

        return jsonify({"message": "Sondage mis à jour avec succès"}), 200

    except Exception as e:
        print("Erreur serveur :", str(e))
        return jsonify({"error": str(e)}), 500


@app.route('/sondages/edit/<poll_id>')
def edit_poll(poll_id):
    try:
        poll = sondages_collection.find_one({"_id": ObjectId(poll_id)})

        if not poll:
            return jsonify({"message": "Sondage introuvable"}), 404

        for question in poll.get("questions", []):
            question["_id"] = str(question["_id"])

        return render_template('edit_poll.html', poll=poll)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# _____ Route suppression _____

@app.route('/sondages/<poll_id>', methods=['DELETE'])
def delete_poll(poll_id):
    try:
        result = sondages_collection.delete_one({"_id": ObjectId(poll_id)})
        
        if result.deleted_count == 0:
            return jsonify({"message": "Poll not found"}), 404

        return jsonify({"message": f"Poll with ID {poll_id} deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)