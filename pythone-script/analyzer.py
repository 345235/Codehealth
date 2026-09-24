from scanner import results
from scanner import content
import ast


def find_long_functions(source: str, max_lines: int = 50) -> list[dict]:
    """Return one issue dict per function longer than max_lines."""
    tree =ast.parse(content)
    issues = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FuntionDef, ast.AsyncFunctionDef)):
            length =node.end_lineo - node.lineo + 1 
            if length > max_lines:
                issues.append({
                    "type": "long_function",
                    "name": node.lineno,
                    "length":length, 
                    "max_allowed":max_lines,
                })
        return issues

class MetricsVisitor(ast.NodeVisitor):
        def __init__(self):
            self.function_count =  0 
            self.class_count = 0 

        def visit_FunctionDef(self, node):
            self.function_count += 1
            self.generic_visit (node)

        def  visit_FunctionDef (self, node):
            self.class_count += 1
            self.generic_visit (node)

def analyze(content): 
    try: 
       tree = ast.parse(content)
    except SyntaxError as e : 
        return {"error": f"{e.msg} (line {e.lineno})"}

    visitor = MetricsVisitor()
    visitor.visit(tree)
    return {
        "loc": len(content.splitlines()),
        "functions": visitor.function_count,
        "classes": visitor.class_count,
    }