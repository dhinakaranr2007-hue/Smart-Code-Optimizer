from analyzer import analyze_code
from optimizer import optimize_code
from validator import validate_code
from benchmark import compare_performance


def extract_code(ai_response):
    """
    Extract only the optimized Python code
    from Qwen response.
    """
    start_marker = "OPTIMIZED_CODE_START"
    end_marker = "OPTIMIZED_CODE_END"

    if start_marker not in ai_response:
        return ""

    if end_marker not in ai_response:
        return ""

    # Get content between the markers
    code = ai_response.split(start_marker, 1)[1]
    code = code.split(end_marker, 1)[0]
    code = code.strip()

    # Remove Markdown code fences if Qwen adds them
    if code.startswith("```python"):
        code = code[len("```python"):].strip()
    elif code.startswith("```"):
        code = code[3:].strip()

    if code.endswith("```"):
        code = code[:-3].strip()

    return code


def main():
    # ============================================================
    # HEADER
    # ============================================================
    print("=" * 60)
    print("       SMART CODE OPTIMIZER")
    print("=" * 60)

    print("\nPaste your Python code below.")
    print("Type END on a new line when finished.\n")

    # ============================================================
    # INPUT
    # ============================================================
    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)

    code = "\n".join(lines)

    if not code.strip():
        print("\nNo code entered.")
        return

    # ============================================================
    # STEP 1 - ANALYSIS
    # ============================================================
    print("\n[1] Analyzing code...")
    try:
        analysis = analyze_code(code)
    except Exception as e:
        print("\nCode analysis failed.")
        print(f"Error: {e}")
        return

    print("\nCode Analysis:")
    print(analysis)

    # ============================================================
    # STEP 2 - AI OPTIMIZATION
    # ============================================================
    print("\n[2] Generating optimized code using Qwen...")
    optimized_response = optimize_code(code, analysis)

    if not optimized_response:
        print("\nAI Optimization Failed.")
        print("No response received from Ollama.")
        return

    if optimized_response.startswith("Error:"):
        print("\nAI Optimization Failed.")
        print(optimized_response)
        return

    print("\nAI Optimization Result:")
    print(optimized_response)

    # ============================================================
    # STEP 3 - EXTRACT OPTIMIZED CODE
    # ============================================================
    optimized_code = extract_code(optimized_response)
    print("\n[3] Optimized Code Extracted:")
    print("-" * 60)

    if not optimized_code:
        print("ERROR: Optimized code could not be extracted.")
        print("\nQwen response did not contain valid optimized code.")
        return

    print(optimized_code)
    print("-" * 60)

    # ============================================================
    # STEP 4 - VALIDATION
    # ============================================================
    print("\n[4] Validation")
    try:
        validation = validate_code(code, optimized_code)
    except Exception as e:
        print("\nValidation failed.")
        print(f"Error: {e}")
        return

    print("\nValidation Result:")
    print(validation.get("message", "No validation message."))

    # ------------------------------------------------------------
    # VALIDATION FAILED
    # ------------------------------------------------------------
    if not validation.get("valid", False):
        print("\nValidation Status: FAILED")
        if "original_output" in validation:
            print("\nOriginal Output:")
            print(validation["original_output"])
        if "optimized_output" in validation:
            print("\nOptimized Output:")
            print(validation["optimized_output"])
        if "optimized" in validation:
            optimized_result = validation["optimized"]
            if optimized_result.get("error"):
                print("\nOptimized Code Error:")
                print(optimized_result["error"])
        return

    # ------------------------------------------------------------
    # VALIDATION PASSED
    # ------------------------------------------------------------
    print("\nOriginal Output:")
    print(validation["original_output"])
    print("\nOptimized Output:")
    print(validation["optimized_output"])
    print("\nValidation Status: PASSED")

    # ============================================================
    # STEP 5 - BENCHMARK
    # ============================================================
    print("\n[5] Benchmarking Performance...")
    try:
        performance = compare_performance(code, optimized_code)
    except Exception as e:
        print("\nBenchmark failed.")
        print(f"Error: {e}")
        return

    original_time = performance["original_time"]
    optimized_time = performance["optimized_time"]
    improvement = performance["improvement_percentage"]

    print("\nPerformance Comparison:")
    print("-" * 60)
    print(f"Original Execution Time : {original_time:.8f} seconds")
    print(f"Optimized Execution Time: {optimized_time:.8f} seconds")
    print(f"Performance Improvement : {improvement:.2f}%")

    # ============================================================
    # STEP 6 - FINAL REPORT
    # ============================================================
    print("\n[6] Final Performance Report")
    print("-" * 60)

    if improvement > 0:
        print("Result: Optimization improved execution performance.")
    elif improvement < 0:
        print("Result: Optimized code is slower for this test.")
    else:
        print("Result: No significant performance difference.")

    print(f"Execution Time Change: {improvement:.2f}%")

    # ============================================================
    # FINAL STATUS
    # ============================================================
    print("\nOptimization Status: SUCCESS")
    print("Validation Status: PASSED")
    print("Benchmark Status: COMPLETED")

    print("\n" + "=" * 60)
    print("       PROJECT PIPELINE COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()



