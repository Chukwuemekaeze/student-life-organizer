import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Secure values from environment
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
MCP_SCHEMA_URL = os.getenv("MCP_SCHEMA_URL")

# Your natural language command
user_prompt = "I want to add a journal entry saying I was mentally drained and skipped class today."

# Claude-compatible payload structure
payload = {
    "model": "claude-3-haiku-20240307",
    "max_tokens": 1024,
    "temperature": 0.2,
    "system": "You are an assistant that uses the MCP API schema to decide which endpoint to call and how to respond.",
    "messages": [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": user_prompt}
            ]
        },
        {
            "role": "assistant",
            "content": [
                {
                    "type": "tool_use",
                    "name": "mcp",
                    "id": "mcp_call_1",
                    "input": {
                        "schema": MCP_SCHEMA_URL
                    }
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "tool_result",
                    "tool_use_id": "mcp_call_1",
                    "content": "Schema received. Ready to proceed."
                }
            ]
        }
    ]

}

# Send to Claude API
response = requests.post(
    "https://api.anthropic.com/v1/messages",
    headers={
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    },
    data=json.dumps(payload)
)

# Output response
if response.status_code == 200:
    data = response.json()
    if "content" in data and data["content"]:
        print("\n✅ Claude's reply:\n")
        print(data["content"][0]["text"])
    else:
        print("🤖 Claude didn’t return a direct reply (maybe because the tool did the job).")
        print("Response:\n", json.dumps(data, indent=2))

else:
    print("❌ Claude request failed:", response.status_code)
    print(response.text)
