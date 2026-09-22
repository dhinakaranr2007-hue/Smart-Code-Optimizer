import requests

def optimize_code(code, analysis):
    prompt = f"""
You are an expert Python code optimization system.

Your task is to optimize the user's Python code while preserving EXACTLY the same behavior and output.

ORIGINAL PYTHON CODE:
{code}

CODE ANALYSIS:
{analysis}

Follow these rules strictly:

1. Analyze the original code.
2. Identify possible performance or readability improvements.
3. Preserve the exact functionality and output.
4. The optimized code MUST be a COMPLETE, STANDALONE Python program.
5. Include ALL required variables, imports, functions, and input data from the original code.
6. Do NOT remove variables that are required by the optimized code.
7. Do NOT assume that any variable exists outside the optimized code.
8. The optimized code must run independently using Python.
9. Do not use explanations inside the optimized code.
10. Return the optimized code ONLY between OPTIMIZED_CODE_START and OPTIMIZED_CODE_END.

Use EXACTLY this format:

PROBLEMS:

* Problem 1
* Problem 2

TIME_COMPLEXITY:
O(...)

SPACE_COMPLEXITY:
O(...)

OPTIMIZED_CODE_START
<complete standalone Python code>
OPTIMIZED_CODE_END

EXPLANATION:
Explain the optimization.

IMPORTANT:
The code between OPTIMIZED_CODE_START and OPTIMIZED_CODE_END must be directly executable Python code.
Do not put Markdown `python or ` inside the markers.
Do not omit original variable definitions.
"""

    try:
        response = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={
                "model": "qwen2.5-coder:7b",
                "prompt": prompt,
                "stream": False
            },
            timeout=300
        )

        response.raise_for_status()
        data = response.json()
        return data["response"]

    except requests.exceptions.Timeout:
        return "Error: Ollama took too long to respond."

    except requests.exceptions.ConnectionError:
        return "Error: Cannot connect to Ollama. Make sure Ollama is running."

    except Exception as e:
        return f"Error: {e}"





