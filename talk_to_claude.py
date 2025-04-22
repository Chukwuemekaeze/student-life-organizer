import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
MCP_SCHEMA_URL = os.getenv("MCP_SCHEMA_URL")

user_prompt = "Delete the journal entry about being mentally drained and skipping class."

# Step 1: Ask Claude to generate a tool_use call
payload = {
    "model": "claude-3-haiku-20240307",
    "max_tokens": 1024,
    "temperature": 0.2,
    "system": (
        '''You are an API-powered assistant. When the user gives a command, you MUST respond by using the 'mcp' tool. "
        "Valid endpoints include ONLY the following: "
        "/resources/journals, /resources/notes, /resources/study_tasks, /resources/projects, /resources/schedule. "
        "You must include a 'method', 'endpoint', and 'body' field in your tool call input. "
        "Do not respond in natural language — only call the 'mcp' tool.
        
        You are an assistant that helps users manage their student life using the MCP API.

        When a user wants to delete an item (e.g., a journal, note, task), follow this strategy:

        1. Use the `/resources/<resource>/search` endpoint with query parameters derived from the user’s input (e.g., `?title=sad`).
        2. Pick the entry that best matches based on title and/or content.
        3. Then call the DELETE endpoint with the full entry (as it appears in the data) as the body.

        Always confirm that the entry was successfully deleted by reporting the result.
        After performing a search, you MUST immediately follow up with a DELETE request using the full content of the matched item.

        '''

    ),
    "tools": [
        {
            "name": "mcp",
            "description": "Model Context Protocol API for managing journal entries, notes, tasks, projects, and schedules.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "method": {"type": "string"},
                    "endpoint": {"type": "string"},
                    "body": {
                        "type": "object",
                        "description": "Data to send with the request",
                        "additionalProperties": True
                    }
                },
                "required": ["method", "endpoint", "body"]
            }
        }
    ],
    "messages": [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": user_prompt}
            ]
        }
    ]
}

print("--- Calling Claude (Step 1) ---")
response = requests.post(
    "https://api.anthropic.com/v1/messages",
    headers={
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    },
    data=json.dumps(payload)
)

if response.status_code != 200:
    print(f"❌ Claude request failed: {response.status_code}")
    print(response.text)
    exit()

data = response.json()
tool_use_block = next((block for block in data.get("content", []) if block.get("type") == "tool_use"), None)

if not tool_use_block:
    print("❌ No 'tool_use' block found in Claude's response.")
    print(json.dumps(data, indent=2))
    exit()

tool_id = tool_use_block["id"]
tool_input = tool_use_block["input"]
method = tool_input.get("method", "POST").upper()
endpoint = tool_input.get("endpoint")
body = tool_input.get("body", {})

if "/search" in endpoint and method == "GET":
    print("🧠 Claude requested a search. Performing it and following up with a DELETE...")

    search_url = MCP_SCHEMA_URL.replace("/schema", "") + endpoint
    backend_response = requests.get(search_url, params=body)
    backend_response.raise_for_status()
    search_results = backend_response.json()

    if not search_results:
        print("❌ No matching entries found. Nothing to delete.")
        exit()

    delete_url = MCP_SCHEMA_URL.replace("/schema", "") + endpoint.replace("/search", "")

    for match_to_delete in search_results:
        print("🗑️ Deleting:", json.dumps(match_to_delete, indent=2))

        delete_response = requests.delete(
            delete_url,
            json=match_to_delete,
            headers={"Content-Type": "application/json"}
        )

        delete_response.raise_for_status()
        delete_result = delete_response.json()


    # Send tool_result back to Claude
    tool_result_payload = {
        "model": "claude-3-haiku-20240307",
        "max_tokens": 1024,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_id,
                        "content": json.dumps(delete_result)
                    }
                ]
            }
        ],
        "tools": payload["tools"]
    }

    final_response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        },
        data=json.dumps(tool_result_payload)
    )

    print("\n✅ Final Claude response:\n")
    final_json = final_response.json()
    for block in final_json.get("content", []):
        if block.get("type") == "text":
            print("\n✅ Claude’s Final Reply:\n")
            print(block["text"])
            break
    else:
        print("⚠️ Claude did not return a natural language reply.")

    exit()


if not endpoint:
    print("❌ Claude did not include a valid 'endpoint' in the tool_use input.")
    exit()

base_url = MCP_SCHEMA_URL.replace("/schema", "")
full_url = f"{base_url}{endpoint}"

print(f"\n🌍 Calling Your Backend API:")
print(f"   Method: {method}")
print(f"   URL: {full_url}")
print(f"   Payload: {json.dumps(body, indent=2)}")

try:
    if method == "GET":
        backend_response = requests.get(full_url)
    elif method == "POST":
        backend_response = requests.post(full_url, json=body)
    elif method == "PUT":
        backend_response = requests.put(full_url, json=body)
    elif method == "DELETE":
        backend_response = requests.delete(full_url, json=body, headers={"Content-Type": "application/json"})
    else:
        print(f"❌ Unsupported HTTP method: {method}")
        exit()

    backend_response.raise_for_status()
    result_json = backend_response.json()
    print("\n✅ Backend API call successful.")

except requests.exceptions.RequestException as e:
    print(f"❌ Backend API call failed: {e}")
    if backend_response is not None:
        print(f"   Status Code: {backend_response.status_code}")
        print(f"   Response Text: {backend_response.text}")
    exit()

# Step 2: Send tool_result to Claude
tool_result_payload = {
    "model": "claude-3-haiku-20240307",
    "max_tokens": 1024,
    "messages": [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": user_prompt}
            ]
        },
        {
            "role": "assistant",
            "content": data["content"]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": tool_id,
                    "content": json.dumps(result_json)
                }
            ]
        }
    ],

    "tools": payload["tools"]
}

print("\n--- Calling Claude (Step 2) with Tool Result ---")
final_response = requests.post(
    "https://api.anthropic.com/v1/messages",
    headers={
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    },
    data=json.dumps(tool_result_payload)
)

if final_response.status_code == 200:
    final_data = final_response.json()
    final_text_content = next((block.get("text") for block in final_data.get("content", []) if block.get("type") == "text"), None)
    if final_text_content:
        print("\n✅ Claude’s Final Reply:\n")
        print(final_text_content)
    else:
        print("⚠️ Claude responded, but no text content was found.")
else:
    print(f"❌ Final Claude call failed: {final_response.status_code}")
    print(final_response.text)
