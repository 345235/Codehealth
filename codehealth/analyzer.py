import ast


def find_long_functions(tree: ast.AST, max_lines: int = 50) -> list[dict]:
    """Return one issue dict per function/method longer than max_lines."""
    issues = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            length = node.end_lineno - node.lineno + 1
            if length > max_lines:
                issues.append({
                    "type": "long_function",
                    "name": node.name,
                    "line": node.lineno,
                    "length": length,
                    "max_allowed": max_lines,
                })

    return issues


def find_unused_imports(tree: ast.AST) -> list[dict]:
    """Return one issue dict per imported name that's never referenced."""
    imported_names = {}  

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.asname or alias.name.split(".")[0]
                imported_names[name] = node.lineno
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name == "*":
                    continue 
                name = alias.asname or alias.name
                imported_names[name] = node.lineno

    used_names = {
        node.id for node in ast.walk(tree) if isinstance(node, ast.Name)
    }

    return [
        {"type": "unused_import", "name": name, "line": lineno}
        for name, lineno in imported_names.items()
        if name not in used_names
    ] 


class MetricsVisitor(ast.NodeVisitor):
    def __init__(self):
        self.function_count = 0
        self.class_count = 0

    def visit_FunctionDef(self, node):
        self.function_count += 1
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        self.function_count += 1
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.class_count += 1
        self.generic_visit(node)


def count_metrics(tree: ast.AST, content: str) -> dict:
    """Basic size metrics: lines of code, function count, class count."""
    visitor = MetricsVisitor()
    visitor.visit(tree)
    return {
        "loc": len(content.splitlines()),
        "functions": visitor.function_count,
        "classes": visitor.class_count,
    }


def analyze(content: str, max_lines: int = 50) -> dict:
    """
    Analyze one file's source and return the per-file result schema:
        {
            "error": str | None,
            "issues": [ {...}, ... ],
            "metrics": {"loc": int, "functions": int, "classes": int} | None,
        }
    If the file has a syntax error, issues/metrics are left empty/None
    rather than raising, so a bad file doesn't crash a whole scan.
    """
    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        return {
            "error": f"{e.msg} (line {e.lineno})",
            "issues": [],
            "metrics": None,
        }

    issues = find_long_functions(tree, max_lines) + find_unused_imports(tree)
    metrics = count_metrics(tree, content)

    return {
        "error": None,
        "issues": issues,
        "metrics": metrics,
    }

