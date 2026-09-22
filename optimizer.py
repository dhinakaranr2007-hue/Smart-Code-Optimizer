import os
import requests


def build_prompt(code, analysis):
    return f"""
You are an expert Python code optimizer.

Analyze the following Python code and optimize it without changing its output or functionality.

Analysis:
Functions: {analysis.get("functions", 0)}
Loops: {analysis.get("loops", 0)}
Conditions: {analysis.get("conditions", 0)}

Original Code:
{code}

Your response MUST contain:

OPTIMIZED_CODE_START
<only the optimized Python code>
OPTIMIZED_CODE_END

EXPLANATION
<short explanation>

Do not put any text inside OPTIMIZED_CODE_START and OPTIMIZED_CODE_END except valid Python code.
"""


def optimize_with_ollama(prompt):
    url = os.getenv(
        "OLLAMA_URL",
        "http://127.0.0.1:11434/api/generate"
    )

    model = os.getenv(
        "OLLAMA_MODEL",
        "qwen2.5-coder:7b"
    )

    response = requests.post(
        url,
        json={
            "model": model,
            "prompt": prompt,
            "stream": False,
            "temperature": 0.1
        },
        timeout=300
    )

    response.raise_for_status()

    data = response.json()
    return data.get("response", "")


def optimize_with_openrouter(prompt):
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise Exception(
            "OPENROUTER_API_KEY is not configured."
        )

    model = os.getenv(
        "OPENROUTER_MODEL",
        "qwen/qwen-2.5-coder-32b-instruct"
    )

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.1
        },
        timeout=300
    )

    response.raise_for_status()

    data = response.json()

    return data["choices"][0]["message"]["content"]


def optimize_code(code, analysis):
    prompt = build_prompt(code, analysis)

    ai_mode = os.getenv("AI_MODE", "local").lower()

    if ai_mode == "online":
        return optimize_with_openrouter(prompt)

    return optimize_with_ollama(prompt)





