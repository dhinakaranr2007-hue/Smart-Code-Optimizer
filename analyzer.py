import ast

def analyze_code(code):
    tree = ast.parse(code)

    functions = 0
    loops = 0
    conditions = 0

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions += 1

        elif isinstance(node, (ast.For, ast.While)):
            loops += 1

        elif isinstance(node, ast.If):
            conditions += 1

    return {
        "functions": functions,
        "loops": loops,
        "conditions": conditions
    }