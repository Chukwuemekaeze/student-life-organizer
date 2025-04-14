from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

#Get path to data folder
DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data'))

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


@app.route('/resources/schedule')
def get_schedule():
    with open(os.path.join(DATA_PATH, 'schedule.json')) as f:
        data = json.load(f)
    return jsonify(data)


# READ JOURNAL ENTRIES
@app.route('/resources/journals')
def get_journals():
    with open(os.path.join(DATA_PATH, 'journals.json')) as f:
        data = json.load(f)
    return jsonify(data)

# ADD JOURNAL ENTRIES
@app.route('/resources/journals', methods=['POST'])
def add_journal_entry():
    try:
        with open(os.path.join(DATA_PATH, 'journals.json')) as f:
            journals = json.load(f)
    except json.JSONDecodeError:
        journals = []

    new_entry = request.get_json()
    if not new_entry:
        return jsonify({"error": "Invalid JSON data"}), 400
    
    journals.append(new_entry)

    with open(os.path.join(DATA_PATH, 'journals.json'), 'w') as f:
        json.dump(journals, f, indent=2)

    return jsonify({"message": "Journal entry added", "entry": new_entry}), 201

#UPDATE JOURNAL ENTRIES
@app.route('/resources/journals/<int:index>', methods=['PUT'])
def update_journal_entry(index):
    try:
        with open(os.path.join(DATA_PATH, 'journals.json')) as f:
            journals = json.load(f)
    except json.JSONDecodeError:
        return jsonify({"error": "Could not read journal entries"}), 500

    if index < 0 or index >= len(journals):
        return jsonify({"error": "Invalid journal index"}), 404

    updated_entry = request.get_json()
    if not updated_entry:
        return jsonify({"error": "Invalid JSON data"}), 400

    journals[index] = updated_entry

    with open(os.path.join(DATA_PATH, 'journals.json'), 'w') as f:
        json.dump(journals, f, indent=2)

    return jsonify({"message": "Journal entry updated", "entry": updated_entry}), 200

#DELETE JOURNAL ENTRIES
@app.route('/resources/journals/<int:index>', methods=['DELETE'])
def delete_journal_entry(index):
    try:
        with open(os.path.join(DATA_PATH, 'journals.json')) as f:
            journals = json.load(f)
    except json.JSONDecodeError:
        return jsonify({"error": "Could not read journal entries"}), 500

    if index < 0 or index >= len(journals):
        return jsonify({"error": "Invalid journal index"}), 404

    deleted_entry = journals.pop(index)

    with open(os.path.join(DATA_PATH, 'journals.json'), 'w') as f:
        json.dump(journals, f, indent=2)

    return jsonify({"message": "Journal entry deleted", "entry": deleted_entry}), 200


# READ STUDY TASKS
@app.route('/resources/study_tasks')
def get_study_tasks():
    with open(os.path.join(DATA_PATH, 'study_tasks.json')) as f:
        data = json.load(f)
    return jsonify(data)

# ADD STUDY TASKS
@app.route('/resources/study_tasks', methods=['POST'])
def add_study_task():
    try:
        with open(os.path.join(DATA_PATH, 'study_tasks.json')) as f:
            tasks = json.load(f)
    except json.JSONDecodeError:
        tasks = []

    new_task = request.get_json()
    if not new_task:
        return jsonify({"error": "Invalid JSON"}), 400

    tasks.append(new_task)

    with open(os.path.join(DATA_PATH, 'study_tasks.json'), 'w') as f:
        json.dump(tasks, f, indent=2)

    return jsonify({"message": "Task added successfully", "task": new_task}), 201

# UPDATE STUDY TASKS
@app.route('/resources/study_tasks/<int:index>', methods=['PUT'])
def update_study_task(index):
    try:
        with open(os.path.join(DATA_PATH, 'study_tasks.json')) as f:
            tasks = json.load(f)
    except json.JSONDecodeError:
        return jsonify({"error": "Could not read study tasks"}), 500

    if index < 0 or index >= len(tasks):
        return jsonify({"error": "Invalid task index"}), 404

    updated_task = request.get_json()
    if not updated_task:
        return jsonify({"error": "Invalid JSON data"}), 400

    tasks[index] = updated_task

    with open(os.path.join(DATA_PATH, 'study_tasks.json'), 'w') as f:
        json.dump(tasks, f, indent=2)

    return jsonify({"message": "Task updated", "task": updated_task}), 200

# DELETE STUDY TASKS
@app.route('/resources/study_tasks/<int:index>', methods=['DELETE'])
def delete_study_task(index):
    try:
        with open(os.path.join(DATA_PATH, 'study_tasks.json')) as f:
            tasks = json.load(f)
    except json.JSONDecodeError:
        return jsonify({"error": "Could not read study tasks"}), 500

    if index < 0 or index >= len(tasks):
        return jsonify({"error": "Invalid task index"}), 404

    deleted_task = tasks.pop(index)

    with open(os.path.join(DATA_PATH, 'study_tasks.json'), 'w') as f:
        json.dump(tasks, f, indent=2)

    return jsonify({"message": "Task deleted", "task": deleted_task}), 200


@app.route('/resources/notes')
def get_notes():
    with open(os.path.join(DATA_PATH, 'notes.json')) as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/resources/projects')
def get_projects():
    with open(os.path.join(DATA_PATH, 'projects.json')) as f:
        data = json.load(f)
    return jsonify(data)





if __name__ == '__main__':
    app.run(debug=True, port=8000)