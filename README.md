# 🧠 Student Life Organizer — Claude-Powered MCP Assistant

---

## 📘 Description
The Student Life Organizer is a natural-language-driven assistant designed to help students manage their academic life. It utilizes **Anthropic's Claude model** to interpret human language, read a **Model Context Protocol (MCP)** schema, and decide which backend endpoint to call. This prototype focuses on simulating real-world tool-use and backend integration for journaling, notes, study tasks, projects, and schedules.

---

## ✅ Features
- 🧠 Natural-language command parsing via Claude
- 📜 `/schema` endpoint using Model Context Protocol (MCP)
- 🔁 Claude tool-use simulation (`tool_use` ↔ `tool_result`)
- 🗃️ JSON-based resource storage (journals, notes, etc.)
- 🔒 Secure config with `.env`
- 🌐 Ngrok tunneling for API exposure to Claude
- 💬 Local prompt simulation using Claude’s API
- 🔍 Intelligent journal search via `/resources/journals/search` (supports fuzzy matching)
- 🗑️ Smart journal deletion via natural language (search first, then delete)
- 🧠 Automatic Claude chaining: search → select → delete without explicit user instruction

---

## 🚀 Getting Started

### 🧱 Prerequisites
- Python 3.10+
- pip
- An [Anthropic API key](https://console.anthropic.com/)
- [ngrok](https://ngrok.com/) account

### 📥 Installation
```bash
git clone https://github.com/Chukwuemekaeze/student-life-organizer.git
cd student-life-organizer
python -m venv venv
venv/Scripts/activate  # Windows
pip install -r requirements.txt
```

---

## 💡 Usage

### Step 1: Start Flask MCP server
```bash
python backend/mcp_server/app.py
```

### Step 2: Expose server with ngrok
```bash
ngrok http 8000
```
Take the HTTPS URL (e.g., `https://9a94-...ngrok-free.app`) and use it in your `.env`.

### Step 3: Set up your `.env`
```env
ANTHROPIC_API_KEY=your-key-here
MCP_SCHEMA_URL=https://your-ngrok-url.ngrok-free.app/schema
```

### Step 4: Run Claude interaction
```bash
python talk_to_claude.py
```
You’ll see Claude understand your instruction, interpret the schema, and suggest (or simulate) an endpoint call.

---

## ⚙️ Configuration

All config is stored in a `.env` file:
```env
ANTHROPIC_API_KEY=your-key-here
MCP_SCHEMA_URL=https://your-ngrok-url.ngrok-free.app/schema
```

Make sure to add `.env` to `.gitignore` so you never push secrets:
```
.env
```

---

## 📂 Project Structure
```
student-life-organizer/
├── backend/
│   └── mcp_server/
│       └── app.py          # Flask server with MCP routes
├── data/                   # All JSON data files
│   └── journals.json, notes.json, etc.
├── talk_to_claude.py       # Script to test tool-use manually
├── requirements.txt
└── .env                    # API keys + schema URL
```

---

## 🛣️ Roadmap
- [x] MCP `/schema` endpoint
- [x] Claude API integration
- [x] Tool use simulation (tool_use + tool_result)
- [x] Actually execute POST/GET calls from Claude replies
- [x] Intelligent journal search using fuzzy query
- [x] Automatic search-then-delete journal flow with Claude
- [ ] Add multi-turn memory or conversational chaining
- [ ] Create terminal-style Claude chatbot UI
- [ ] Deploy to Hugging Face or private cloud

---

## 📜 License
MIT License

---

## 👤 Credits
Built by [@Chukwuemeka🖤] as part of an experimental AI-powered student life planner. Architecture guidance and Claude tool-use design contributed by OpenAI ChatGPT-4o.

