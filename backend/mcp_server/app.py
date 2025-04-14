from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

# Get path to data folder
DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data'))

# 🔐 Safe JSON handling utilities
def load_json(file_path):
    try:
        with open(file_path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return []

def save_json(file_path, data):
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error saving {file_path}: {e}")

@app.route('/schema')
def schema():
    return jsonify({
        "name": "Studentend Life Organizer",
        "description":"MCP API exposing class schedule for AI assistant",
        "resources": {
            "schedules": {
                "type": "list",
                "description": "Class schedule with day, time and location",
                "fields": ["course", "day", "time", "location"]
            },
            "journals": {
                "type": "list",
                "description": "Daily mood and journal entries",
                "fields": ["date", "mood", "entry"]
            },
            "study_tasks": {
                "type": "list",
                "description": "To-do list of study tasks",
                "fields": ["title", "due_date", "status", "priority"]
            },
            "notes": {
                "type": "list",
                "description": "Lecture notes and summaries",
                "fields": ["title", "course", "tags", "summary"]
            },
            "projects": {
                "type": "list",
                "description": "Tracks academic or GitHub projects",
                "fields": ["name", "type", "status", "deadline"]
            }
        }
    })

# 📦 General route structure
RESOURCE_FILES = {
    "schedule": "schedule.json",
    "journals": "journals.json",
    "study_tasks": "study_tasks.json",
    "notes": "notes.json",
    "projects": "projects.json"
}

def register_resource_routes(resource, filename):
    filepath = os.path.join(DATA_PATH, filename)

    def get():
        data = load_json(filepath)
        return jsonify(data)

    def post():
        data = load_json(filepath)
        new_item = request.get_json()
        if not new_item:
            return jsonify({"error": "Invalid JSON data"}), 400
        data.append(new_item)
        save_json(filepath, data)
        return jsonify({"message": f"{resource} added", resource[:-1]: new_item}), 201

    def put(index):
        data = load_json(filepath)
        if index < 0 or index >= len(data):
            return jsonify({"error": f"Invalid {resource[:-1]} index"}), 404
        updated_item = request.get_json()
        if not updated_item:
            return jsonify({"error": "Invalid JSON data"}), 400
        data[index] = updated_item
        save_json(filepath, data)
        return jsonify({"message": f"{resource[:-1]} updated", resource[:-1]: updated_item}), 200

    def delete(index):
        data = load_json(filepath)
        if index < 0 or index >= len(data):
            return jsonify({"error": f"Invalid {resource[:-1]} index"}), 404
        deleted_item = data.pop(index)
        save_json(filepath, data)
        return jsonify({"message": f"{resource[:-1]} deleted", resource[:-1]: deleted_item}), 200

    app.add_url_rule(f"/resources/{resource}", f"get_{resource}", get, methods=["GET"])
    app.add_url_rule(f"/resources/{resource}", f"post_{resource}", post, methods=["POST"])
    app.add_url_rule(f"/resources/{resource}/<int:index>", f"put_{resource}", put, methods=["PUT"])
    app.add_url_rule(f"/resources/{resource}/<int:index>", f"delete_{resource}", delete, methods=["DELETE"])

for resource, filename in RESOURCE_FILES.items():
    register_resource_routes(resource, filename)

if __name__ == '__main__':
    app.run(debug=True, port=8000)