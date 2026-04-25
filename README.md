# 🤖 Visual Timeline of Agent Collaboration

A Streamlit app that runs multiple AI agents via **Ollama** (local LLMs) and visualizes their collaboration in a rich, interactive timeline.

---

## ✨ Features

- **Multiple specialized agents**: Researcher, Analyst, Critic, Summarizer
- **Timestamped logs** for every agent interaction
- **Interactive Gantt chart** showing agent execution over time
- **Chronological card view** grouped by agent and topic
- **Session statistics** table (duration, output length, etc.)
- **Export as PDF or PNG** for reporting

---

## 🗂️ Project Structure

```
timeline_project/
├── app.py            # Main Streamlit application
├── agents.py         # Agent definitions and Ollama API calls
├── timeline.py       # Timeline rendering (charts + cards)
├── export_utils.py   # PDF and PNG export utilities
├── requirements.txt  # Python dependencies
└── README.md
```

---

## ⚙️ Setup

### 1. Install Ollama

Download and install from [https://ollama.com](https://ollama.com), then pull a model:

```bash
ollama pull llama3.2
# or
ollama pull mistral
```

Start the Ollama server:

```bash
ollama serve
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
streamlit run app.py
```

---

## 🧠 How It Works

1. You enter a **topic/task** and select which **agents** to run.
2. Each agent is sent the topic (plus accumulated context from previous agents) to Ollama.
3. Responses are logged with **timestamps** and **duration**.
4. The app renders:
   - A **Gantt chart** of agent execution timing
   - **Cards** showing each agent's response in order
   - A **stats table** summarizing the session
5. Optionally **export** the timeline as a PDF or PNG.

---

## 🤖 Agent Roles

| Agent | Role |
|---|---|
| 🔍 Researcher | Gathers facts and background information |
| 📊 Analyst | Identifies trends, insights, and implications |
| ⚡ Critic | Challenges assumptions and highlights risks |
| 📝 Summarizer | Synthesizes everything into key takeaways |

---

## 📤 Export

- **PDF**: Full text report with all agent responses and stats
- **PNG**: Visual chart (Gantt + output size bar chart)

---

## 🔧 Customization

- Add new agents by editing `AGENT_PROMPTS` in `agents.py`
- Change colors/icons via `AGENT_COLORS` and `AGENT_ICONS` in `agents.py`
- Any Ollama-supported model works (llama3.2, mistral, phi3, gemma2, etc.)
