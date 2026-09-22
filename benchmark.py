import time
import contextlib
import io

def benchmark_code(code, runs=5):
    times = []
    for _ in range(runs):
        output = io.StringIO()
        start = time.perf_counter()
        with contextlib.redirect_stdout(output):
            exec(code, {})
        end = time.perf_counter()
        times.append(end - start)
    return sum(times) / len(times)


def compare_performance(original_code, optimized_code):
    original_time = benchmark_code(original_code)
    optimized_time = benchmark_code(optimized_code)

    if original_time > 0:
        improvement = ((original_time - optimized_time) / original_time) * 100
    else:
        improvement = 0

    return {
        "original_time": original_time,
        "optimized_time": optimized_time,
        "improvement_percentage": improvement
    }

