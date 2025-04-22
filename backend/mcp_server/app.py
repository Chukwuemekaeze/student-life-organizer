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

        if new_item in data:
            return jsonify({
                "message": f"Duplicate {resource[:-1]} detected. Entry not added.",
                resource[:-1]: new_item
            }), 200

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

    def delete(index=None):
        data = load_json(filepath)

        if index is None:
            body = request.get_json()
            if not body:
                return jsonify({"error": "No data provided for deletion"}), 400

            match = next(
                (
                    item for item in data
                    if all(body.get(k) == item.get(k) for k in body.keys())
                ),
                None
            )

            if match:
                data.remove(match)
                save_json(filepath, data)
                return jsonify({
                    "message": f"{resource[:-1]} deleted by field match",
                    resource[:-1]: match
                }), 200

            return jsonify({
                "error": f"{resource[:-1]} not found for deletion"
            }), 404

        if index < 0 or index >= len(data):
            return jsonify({"error": f"Invalid {resource[:-1]} index"}), 404

        deleted_item = data.pop(index)
        save_json(filepath, data)
        return jsonify({
            "message": f"{resource[:-1]} deleted by index",
            resource[:-1]: deleted_item
        }), 200

    app.add_url_rule(f"/resources/{resource}", f"get_{resource}", get, methods=["GET"])
    app.add_url_rule(f"/resources/{resource}", f"post_{resource}", post, methods=["POST"])
    app.add_url_rule(f"/resources/{resource}/<int:index>", f"put_{resource}", put, methods=["PUT"])
    app.add_url_rule(f"/resources/{resource}", f"delete_by_content_{resource}", delete, methods=["DELETE"])
    app.add_url_rule(f"/resources/{resource}/<int:index>", f"delete_by_index_{resource}", delete, methods=["DELETE"])

# ✅ NEW: Route for intelligent search
@app.route("/resources/<resource>/search")
def search_resource(resource):
    filename = RESOURCE_FILES.get(resource)
    if not filename:
        return jsonify({"error": "Invalid resource"}), 404

    filepath = os.path.join(DATA_PATH, filename)
    data = load_json(filepath)
    query = request.args.to_dict()

    def fuzzy_match(query_val, text_val):
        if not query_val or not text_val:
            return False
        query_tokens = query_val.lower().split()
        text = text_val.lower()
        return any(token in text for token in query_tokens)

    results = []
    for item in data:
        if all(
            fuzzy_match(query.get(k), str(item.get(k, "")))
            for k in query.keys()
        ):
            results.append(item)

    return jsonify(results)


# Register everything
for resource, filename in RESOURCE_FILES.items():
    register_resource_routes(resource, filename)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
