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


#GET SCHEDULE
@app.route('/resources/schedule')
def get_schedule():
    with open(os.path.join(DATA_PATH, 'schedule.json')) as f:
        data = json.load(f)
    return jsonify(data)

#ADD TO SCHEDULE
@app.route('/resources/schedule', methods=['POST'])
def add_schedule_item():
    try:
        with open(os.path.join(DATA_PATH, 'schedule.json')) as f:
            schedule = json.load(f)
    except json.JSONDecodeError:
        schedule = []

    new_item = request.get_json()
    if not new_item:
        return jsonify({"error": "Invalid JSON data"}), 400

    schedule.append(new_item)

    with open(os.path.join(DATA_PATH, 'schedule.json'), 'w') as f:
        json.dump(schedule, f, indent=2)

    return jsonify({"message": "Schedule item added", "item": new_item}), 201

#UPDATE SCHEDULE
@app.route('/resources/schedule/<int:index>', methods=['PUT'])
def update_schedule_item(index):
    try:
        with open(os.path.join(DATA_PATH, 'schedule.json')) as f:
            schedule = json.load(f)
    except json.JSONDecodeError:
        return jsonify({"error": "Could not read schedule"}), 500

    if index < 0 or index >= len(schedule):
        return jsonify({"error": "Invalid index"}), 404

    updated_item = request.get_json()
    if not updated_item:
        return jsonify({"error": "Invalid JSON data"}), 400

    schedule[index] = updated_item

    with open(os.path.join(DATA_PATH, 'schedule.json'), 'w') as f:
        json.dump(schedule, f, indent=2)

    return jsonify({"message": "Schedule updated", "item": updated_item}), 200

#DELETE FROM SCHEDULE
@app.route('/resources/schedule/<int:index>', methods=['DELETE'])
def delete_schedule_item(index):
    try:
        with open(os.path.join(DATA_PATH, 'schedule.json')) as f:
            schedule = json.load(f)
    except json.JSONDecodeError:
        return jsonify({"error": "Could not read schedule"}), 500

    if index < 0 or index >= len(schedule):
        return jsonify({"error": "Invalid index"}), 404

    deleted_item = schedule.pop(index)

    with open(os.path.join(DATA_PATH, 'schedule.json'), 'w') as f:
        json.dump(schedule, f, indent=2)

    return jsonify({"message": "Schedule item deleted", "item": deleted_item}), 200



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


#GET NOTES
@app.route('/resources/notes')
def get_notes():
    with open(os.path.join(DATA_PATH, 'notes.json')) as f:
        data = json.load(f)
    return jsonify(data)

#ADD NOTES
@app.route('/resources/notes', methods=['POST'])
def add_note():
    try:
        with open(os.path.join(DATA_PATH, 'notes.json')) as f:
            notes = json.load(f)
    except json.JSONDecodeError:
        notes = []

    new_note = request.get_json()
    if not new_note:
        return jsonify({"error": "Invalid JSON data"}), 400

    notes.append(new_note)

    with open(os.path.join(DATA_PATH, 'notes.json'), 'w') as f:
        json.dump(notes, f, indent=2)

    return jsonify({"message": "Note added", "note": new_note}), 201

#UPDATE NOTES
@app.route('/resources/notes/<int:index>', methods=['PUT'])
def update_note(index):
    try:
        with open(os.path.join(DATA_PATH, 'notes.json')) as f:
            notes = json.load(f)
    except json.JSONDecodeError:
        return jsonify({"error": "Could not read notes"}), 500

    if index < 0 or index >= len(notes):
        return jsonify({"error": "Invalid note index"}), 404

    updated_note = request.get_json()
    if not updated_note:
        return jsonify({"error": "Invalid JSON data"}), 400

    notes[index] = updated_note

    with open(os.path.join(DATA_PATH, 'notes.json'), 'w') as f:
        json.dump(notes, f, indent=2)

    return jsonify({"message": "Note updated", "note": updated_note}), 200

#DELET NOTES
@app.route('/resources/notes/<int:index>', methods=['DELETE'])
def delete_note(index):
    try:
        with open(os.path.join(DATA_PATH, 'notes.json')) as f:
            notes = json.load(f)
    except json.JSONDecodeError:
        return jsonify({"error": "Could not read notes"}), 500

    if index < 0 or index >= len(notes):
        return jsonify({"error": "Invalid note index"}), 404

    deleted_note = notes.pop(index)

    with open(os.path.join(DATA_PATH, 'notes.json'), 'w') as f:
        json.dump(notes, f, indent=2)

    return jsonify({"message": "Note deleted", "note": deleted_note}), 200


#GET PROJECTS
@app.route('/resources/projects')
def get_projects():
    with open(os.path.join(DATA_PATH, 'projects.json')) as f:
        data = json.load(f)
    return jsonify(data)

#ADD PROJECTS
@app.route('/resources/projects', methods=['POST'])
def add_project():
    try:
        with open(os.path.join(DATA_PATH, 'projects.json')) as f:
            projects = json.load(f)
    except json.JSONDecodeError:
        projects = []

    new_project = request.get_json()
    if not new_project:
        return jsonify({"error": "Invalid JSON data"}), 400

    projects.append(new_project)

    with open(os.path.join(DATA_PATH, 'projects.json'), 'w') as f:
        json.dump(projects, f, indent=2)

    return jsonify({"message": "Project added", "project": new_project}), 201

#UPDATE PROJECTS
@app.route('/resources/projects/<int:index>', methods=['PUT'])
def update_project(index):
    try:
        with open(os.path.join(DATA_PATH, 'projects.json')) as f:
            projects = json.load(f)
    except json.JSONDecodeError:
        return jsonify({"error": "Could not read projects"}), 500

    if index < 0 or index >= len(projects):
        return jsonify({"error": "Invalid project index"}), 404

    updated_project = request.get_json()
    if not updated_project:
        return jsonify({"error": "Invalid JSON data"}), 400

    projects[index] = updated_project

    with open(os.path.join(DATA_PATH, 'projects.json'), 'w') as f:
        json.dump(projects, f, indent=2)

    return jsonify({"message": "Project updated", "project": updated_project}), 200

#DELETE PROJECTS
@app.route('/resources/projects/<int:index>', methods=['DELETE'])
def delete_project(index):
    try:
        with open(os.path.join(DATA_PATH, 'projects.json')) as f:
            projects = json.load(f)
    except json.JSONDecodeError:
        return jsonify({"error": "Could not read projects"}), 500

    if index < 0 or index >= len(projects):
        return jsonify({"error": "Invalid project index"}), 404

    deleted_project = projects.pop(index)

    with open(os.path.join(DATA_PATH, 'projects.json'), 'w') as f:
        json.dump(projects, f, indent=2)

    return jsonify({"message": "Project deleted", "project": deleted_project}), 200





if __name__ == '__main__':
    app.run(debug=True, port=8000)