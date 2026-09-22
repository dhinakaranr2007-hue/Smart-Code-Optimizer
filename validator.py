import subprocess
import sys
import tempfile
import os


def run_code(code):
    temp_file = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            delete=False,
            encoding="utf-8"
        ) as f:
            f.write(code)
            temp_file = f.name

        result = subprocess.run(
            [sys.executable, temp_file],
            capture_output=True,
            text=True,
            timeout=10
        )

        return {
            "success": result.returncode == 0,
            "output": result.stdout.strip(),
            "error": result.stderr.strip()
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "output": "",
            "error": "Code execution timed out"
        }

    finally:
        if temp_file and os.path.exists(temp_file):
            os.remove(temp_file)


def validate_code(original_code, optimized_code):

    original_result = run_code(original_code)
    optimized_result = run_code(optimized_code)

    if not original_result["success"]:
        return {
            "valid": False,
            "message": "Original code has an error.",
            "original": original_result,
            "optimized": optimized_result
        }

    if not optimized_result["success"]:
        return {
            "valid": False,
            "message": "Optimized code has an error.",
            "original": original_result,
            "optimized": optimized_result
        }

    if original_result["output"] == optimized_result["output"]:
        return {
            "valid": True,
            "message": "Optimized code produces the same output.",
            "original_output": original_result["output"],
            "optimized_output": optimized_result["output"]
        }

    return {
        "valid": False,
        "message": "Optimized code produces different output.",
        "original_output": original_result["output"],
        "optimized_output": optimized_result["output"]
    }