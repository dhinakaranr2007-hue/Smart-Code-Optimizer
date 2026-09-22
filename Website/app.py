from flask import Flask, request, jsonify, send_from_directory
from pathlib import Path
import sys

# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Allow importing project modules
sys.path.insert(0, str(PROJECT_ROOT))

from analyzer import analyze_code
from optimizer import optimize_code
from validator import validate_code
from benchmark import compare_performance


app = Flask(__name__)


def extract_code(ai_response):
    if not ai_response:
        return ""

    # Preferred format
    if "OPTIMIZED_CODE_START" in ai_response:

        section = ai_response.split(
            "OPTIMIZED_CODE_START", 1
        )[1]

        if "OPTIMIZED_CODE_END" in section:
            section = section.split(
                "OPTIMIZED_CODE_END", 1
            )[0]

        section = section.replace("```python", "")
        section = section.replace("```", "")

        return section.strip()

    # Markdown fallback
    if "```python" in ai_response:

        section = ai_response.split(
            "```python", 1
        )[1]

        if "```" in section:
            section = section.split(
                "```", 1
            )[0]

        return section.strip()

    return ""


@app.route("/")
def home():
    return send_from_directory(
        str(PROJECT_ROOT / "Website"),
        "index.html"
    )


@app.route("/<path:filename>")
def website_files(filename):
    return send_from_directory(
        str(PROJECT_ROOT / "Website"),
        filename
    )


@app.route("/api/optimize", methods=["POST"])
def optimize():

    try:

        # Get request data
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "No request data received."
            }), 400

        # Get Python code
        code = data.get("code", "").strip()

        if not code:
            return jsonify({
                "success": False,
                "error": "Python code is empty."
            }), 400

        # --------------------------------
        # STEP 1: Analyze code
        # --------------------------------

        analysis = analyze_code(code)

        # --------------------------------
        # STEP 2: AI optimization
        # --------------------------------

        ai_response = optimize_code(
            code,
            analysis
        )

        # --------------------------------
        # STEP 3: Extract optimized code
        # --------------------------------

        optimized_code = extract_code(
            ai_response
        )

        if not optimized_code:
            return jsonify({
                "success": False,
                "error": "AI did not return optimized code.",
                "ai_response": ai_response
            }), 500

        # --------------------------------
        # STEP 4: Validate
        # --------------------------------

        validation = validate_code(
            code,
            optimized_code
        )

        # --------------------------------
        # STEP 5: Benchmark
        # --------------------------------

        performance = compare_performance(
            code,
            optimized_code
        )

        # --------------------------------
        # STEP 6: Send result to website
        # --------------------------------

        return jsonify({

            "success": True,

            "analysis": {

                "functions":
                    analysis.get("functions", 0),

                "loops":
                    analysis.get("loops", 0),

                "conditions":
                    analysis.get("conditions", 0)
            },

            "optimized_code":
                optimized_code,

            "validation":
                str(validation),

            "performance": {

                "original_time":
                    performance.get(
                        "original_time",
                        0
                    ),

                "optimized_time":
                    performance.get(
                        "optimized_time",
                        0
                    ),

                "improvement_percentage":
                    performance.get(
                        "improvement_percentage",
                        0
                    )
            }

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


if __name__ == "__main__":

    print()
    print("=" * 55)
    print("       SMART CODE OPTIMIZER")
    print("=" * 55)
    print()
    print("Website:")
    print("http://127.0.0.1:5000")
    print()
    print("Backend: Flask")
    print("AI: Ollama + Qwen2.5-Coder:7b")
    print()
    print("Press CTRL+C to stop.")
    print("=" * 55)
    print()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )
