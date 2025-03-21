from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # Enable CORS
from database import students_collection, faculty_collection, courses_collection
from llm import generate_mongo_query
import json

app = Flask(__name__, template_folder="templates")
CORS(app)  # Allow frontend to access backend

# Collection mapping
db_collections = {
    "students": students_collection,
    "faculty": faculty_collection,
    "courses": courses_collection
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/query", methods=["POST"])
def process_query():
    data = request.json
    print("Received data:", data)  # Debugging print
    
    if not data or "question" not in data or "collection" not in data:
        return jsonify({"error": "Invalid request parameters"}), 400

    user_query = data["question"].strip()
    collection_name = data["collection"].strip()
    
    if collection_name not in db_collections:
        return jsonify({"error": "Invalid collection name"}), 400
    
    try:
        mongo_query = generate_mongo_query(user_query)
        print("Generated MongoDB Query:", mongo_query)  # Debugging
        
        # Ensure valid query format
        mongo_query = json.loads(mongo_query) if isinstance(mongo_query, str) else mongo_query
        if not isinstance(mongo_query, dict):
            return jsonify({"error": "Invalid MongoDB query"}), 500
        
        # Execute MongoDB query
        result = list(db_collections[collection_name].find(mongo_query, {"_id": 0}))
        print("Query Result:", result)  # Debugging
        
        return jsonify({"response": result})
    except Exception as e:
        print("Query Error:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
