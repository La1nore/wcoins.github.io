from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://la1nor:noscope2374@cluster0.575re.mongodb.net/wcoin?retryWrites=true&w=majority"
mongo = PyMongo(app)
CORS(app)

@app.route('/api/coins', methods=['GET'])
def get_coins():
    user_id = request.args.get('user_id')
    user = mongo.db.users.find_one({"user_id": user_id})
    if user:
        return jsonify({"coins": user["coins"]})
    else:
        return jsonify({"coins": 0})

@app.route('/api/start', methods=['POST'])
def start():
    user_id = request.json.get('user_id')
    user = mongo.db.users.find_one({"user_id": user_id})
    if not user:
        mongo.db.users.insert_one({"user_id": user_id, "coins": 0, "last_checked": datetime.utcnow()})
    return jsonify({"status": "started"})

@app.route('/api/update', methods=['POST'])
def update():
    user_id = request.json.get('user_id')
    user = mongo.db.users.find_one({"user_id": user_id})
    if user:
        now = datetime.utcnow()
        last_checked = user["last_checked"]
        delta = (now - last_checked).total_seconds() // 60
        if delta >= 1:
            new_coins = user["coins"] + delta
            mongo.db.users.update_one({"user_id": user_id}, {"$set": {"coins": new_coins, "last_checked": now}})
        return jsonify({"coins": new_coins})
    else:
        return jsonify({"error": "user not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
