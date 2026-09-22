from scanner import results 
from scanner import content 
from pathlib import Path
import ast 

def find_long_functions(source: str, max_lines: int = 50) -> list[dict]:
    """Return one issue dict per function longer than max_lines."""
    tree = ast.parse(source)  
    issues = []

    for node in ast.walk(tree) :
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            length = node.end_lineno - node.lineno + 1 
            if length > max_lines:
                issues.append({
                    "type": "longe_function",
                    "name": node.name,
                    "line": node.lineno,
                    "length": length,
                    "max_allowed": max_lines,
                })

                return issues


def _mark_name(node):
     """Return the mark name for `pytest.mark.x`, `pytest.mark.x(...)` or `mark.x` . 
     
     Returns None for anything that isn't reconisably a pytest mark
     """

     if isinstance (node, ast.Call) : 
         node = node.func 
         if not isinstance (node, ast.Attribute):
             return None 
         base = node.value 
         is_pytest_mark = (
             (isinstance(base. ast.Attribute) and base.attr == "mark")
             or (isinstance (base, ast.Name) and base.id == "mark")
         )
         return node.attr if is_pytest_mark else None 
     
def _collect(value):
    """Yield mark names from the right-hand side of a pytestmark assignment."""
    if isinstance(value, (ast.List, ast.Tuple, ast.Set)):
        for elt in value.elts:
            yield from _collect(elt)
    elif isinstance(value, ast.BinOp) and isinstance(value.op, ast.Add):
        yield from _collect(value.left)   # pytestmark = [a] + [b]
        yield from _collect(value.right)
    else:
        name = _mark_name(value)
        if name:
            yield name

def _static_mark(path):
    """Return the module-level pytest mark names of a test file without executing it"""
    source = Path(path).read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str (path))
    marks = []
    for node in tree.body :
        if isinstance (node,ast.Assign):
            tragets = node.targets
        elif isinstance(node, (ast.AnnAssign, ast.AugAssing)):
            tragets = [node.target]
        else :
            continue
        if node.value is None :
            continue 
        if not any (isinstance (t, ast.Name) and t.id == "pytestmark" for t in tragets):
            continue

        if not isinstance (node, ast.AugAssign):
            marks.clear()
            marks.extend(_collect(node.value))

        return marks

