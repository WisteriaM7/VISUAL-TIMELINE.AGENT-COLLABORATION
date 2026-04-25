import requests
import time
from datetime import datetime

AGENT_PROMPTS = {
    "Researcher": (
        "You are a Researcher agent. Your role is to gather and present key facts, "
        "background information, and relevant data about the given topic. "
        "Be factual, concise, and structured. Respond in 3-5 sentences."
    ),
    "Analyst": (
        "You are an Analyst agent. Your role is to analyze the topic critically, "
        "identify trends, implications, and insights. "
        "Be analytical and logical. Respond in 3-5 sentences."
    ),
    "Critic": (
        "You are a Critic agent. Your role is to challenge assumptions, point out "
        "limitations, risks, or counterarguments related to the topic. "
        "Be balanced but skeptical. Respond in 3-5 sentences."
    ),
    "Summarizer": (
        "You are a Summarizer agent. Your role is to synthesize the overall discussion "
        "about the topic into a clear, concise summary with key takeaways. "
        "Be clear and actionable. Respond in 3-5 sentences."
    ),
}

AGENT_COLORS = {
    "Researcher": "#1f77b4",
    "Analyst": "#ff7f0e",
    "Critic": "#d62728",
    "Summarizer": "#2ca02c",
}

AGENT_ICONS = {
    "Researcher": "🔍",
    "Analyst": "📊",
    "Critic": "⚡",
    "Summarizer": "📝",
}


def query_ollama(model: str, system_prompt: str, user_message: str) -> str:
    """Send a request to Ollama local API and return the response text."""
    url = "http://localhost:11434/api/chat"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        "stream": False,
    }
    try:
        response = requests.post(url, json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        return data.get("message", {}).get("content", "No response received.")
    except requests.exceptions.ConnectionError:
        return "❌ Error: Could not connect to Ollama. Make sure Ollama is running (`ollama serve`)."
    except requests.exceptions.Timeout:
        return "❌ Error: Request timed out. The model may be too slow or unavailable."
    except Exception as e:
        return f"❌ Error: {str(e)}"


def run_agents(topic: str, agent_names: list, model: str) -> list:
    """
    Run each agent sequentially on the topic.
    Returns a list of log entries with timestamps.
    """
    logs = []
    context = f"Topic: {topic}"

    for agent_name in agent_names:
        system_prompt = AGENT_PROMPTS.get(
            agent_name,
            "You are a helpful AI agent. Respond concisely in 3-5 sentences."
        )

        start_time = datetime.now()
        start_ts = start_time.isoformat()

        # Build user message with accumulated context
        user_message = context

        response_text = query_ollama(model, system_prompt, user_message)

        end_time = datetime.now()
        duration_sec = (end_time - start_time).total_seconds()

        log_entry = {
            "agent": agent_name,
            "icon": AGENT_ICONS.get(agent_name, "🤖"),
            "color": AGENT_COLORS.get(agent_name, "#888888"),
            "topic": topic,
            "timestamp": start_ts,
            "timestamp_display": start_time.strftime("%H:%M:%S"),
            "date_display": start_time.strftime("%Y-%m-%d"),
            "duration_sec": round(duration_sec, 2),
            "input": user_message,
            "output": response_text,
        }

        logs.append(log_entry)

        # Accumulate context for next agent
        context += f"\n\n[{agent_name} said]: {response_text}"

        # Small delay so timestamps are distinct
        time.sleep(0.5)

    return logs
