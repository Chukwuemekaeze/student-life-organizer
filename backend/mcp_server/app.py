from flask import Flask, jsonify
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

@app.route('/resources/journals')
def get_journals():
    with open(os.path.join(DATA_PATH, 'journals.json')) as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/resources/study_tasks')
def get_study_tasks():
    with open(os.path.join(DATA_PATH, 'study_tasks.json')) as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/resources/notes')
def get_notes():
    with open(os.path.join(DATA_PATH, 'notes.json')) as f:
        data = json.load(f)
    return jsonify(data)




if __name__ == '__main__':
    app.run(debug=True, port=8000)