from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timezone

app = Flask(__name__)
app.secret_key = 'secret_key'

client = MongoClient("mongodb://localhost:27017/")
db = client["sondages_db"]
sondages_collection = db["sondages"]
users_collection = db["users"]


# _____ Route home _____

@app.route('/')
def index():
    return render_template('index.html')


# _____ Route display all polls _____

@app.route('/sondages/list')
def list_polls():
    try:
        polls = list(sondages_collection.find({}, {"_id": 1, "name": 1}))
        
        if not polls:
            return jsonify({"message": "No polls found"}), 404

        return render_template('polls.html', polls=polls)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# _____ Route display one poll _____

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


# _____ Route create poll _____

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
    
    
# _____ Route update poll _____

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


# _____ Route delete poll _____

@app.route('/sondages/<poll_id>', methods=['DELETE'])
def delete_poll(poll_id):
    try:
        result = sondages_collection.delete_one({"_id": ObjectId(poll_id)})
        
        if result.deleted_count == 0:
            return jsonify({"message": "Poll not found"}), 404

        return jsonify({"message": f"Poll with ID {poll_id} deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# _____ Route send answer _____

reponses_collection = db["reponses"]

@app.route('/sondages/<poll_id>/answer', methods=['POST'])
def submit_response(poll_id):
    try:
        data = request.json
        responses = data.get("responses")

        if not responses:
            return jsonify({"error": "Aucune réponse fournie"}), 400

        response_data = {
            "poll_id": ObjectId(poll_id),
            "submitted_at": datetime.now(timezone.utc),
            "responses": [
                {"question_id": ObjectId(response["question_id"]), "answer": response["answer"]}
                for response in responses
            ]
        }

        reponses_collection.insert_one(response_data)

        return jsonify({"message": "Réponses enregistrées avec succès"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# _____ Route display answers _____

@app.route('/sondages/<poll_id>/reponses')
def show_responses(poll_id):
    try:
        poll = sondages_collection.find_one({"_id": ObjectId(poll_id)})
        if not poll:
            return jsonify({"message": "Poll not found"}), 404
        
        responses = list(reponses_collection.find({"poll_id": ObjectId(poll_id)}))

        formatted_responses = []
        for response in responses:
            formatted_responses.append({
                "submitted_at": response.get("submitted_at").strftime('%Y-%m-%d %H:%M'),
                "responses": response.get("responses")
            })

        return render_template('responses.html', poll=poll, responses=formatted_responses)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -------------------- LOGIN --------------------

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data["_id"])
        self.username = user_data["username"]
        self.password = user_data["password"]

    def get_id(self):
        return self.id

login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)

@login_manager.user_loader
def load_user(user_id):
    user_data = users_collection.find_one({"_id": ObjectId(user_id)})
    if user_data:
        return User(user_data)
    return None


# _____ Route registration _____

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        if users_collection.find_one({"username": username}):
            flash("Username already taken", 'error')
            return redirect(url_for('register'))
        
        users_collection.insert_one({"username": username, "password": hashed_password})
        flash("Registration successful", 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')


# _____ Route login _____

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user_data = users_collection.find_one({"username": username})
        
        if user_data and bcrypt.check_password_hash(user_data['password'], password):
            user = User(user_data)
            login_user(user)
            flash("Login successful", 'success')
            return redirect(url_for('index'))
        else:
            flash("Invalid credentials", 'error')
            return redirect(url_for('login'))
    
    return render_template('login.html')


# _____ Route logout _____

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Déconnexion réussie", 'success')
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)