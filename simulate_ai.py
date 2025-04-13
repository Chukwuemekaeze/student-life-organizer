import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def check_server():
    try:
        res = requests.get(f"{BASE_URL}/schema", timeout=2)
        if res.status_code == 200:
            return True
    except requests.exceptions.ConnectionError:
        print("🚫 ERROR: MCP server is not running on port 8000.")
        print("💡 Run: python backend/mcp_server/app.py in a separate terminal.")
        sys.exit(1)
    except requests.exceptions.Timeout:
        print("⏱️ ERROR: Server took too long to respond.")
        sys.exit(1)

check_server()

# 1. Get the schema
schema = requests.get(f"{BASE_URL}/schema").json()
print("📘 MCP Schema:")
print(json.dumps(schema, indent=2))

# 2. Read current study tasks
study_tasks = requests.get(f"{BASE_URL}/resources/study_tasks").json()
print("\n📋 Current Study Tasks:")
for task in study_tasks:
    print("-", task["title"], "| Due:", task["due_date"])

# 3. AI generates a new study task
new_task = {
    "title": "Practice past questions for Compiler Design",
    "due_date": "2025-04-21",
    "status": "incomplete",
    "priority": "medium"
}
print("\n🧠 AI Suggests New Task:")
print(json.dumps(new_task, indent=2))

# 4. AI posts the new task to your server
response = requests.post(
    f"{BASE_URL}/resources/study_tasks",
    json=new_task
)

print("\n📨 POST Response:")
print(response.status_code, response.json())

# 5. Verify the task was added
updated_tasks = requests.get(f"{BASE_URL}/resources/study_tasks").json()
print("\n✅ Updated Study Tasks:")
for task in updated_tasks:
    print("-", task["title"], "| Due:", task["due_date"])
