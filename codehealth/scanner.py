import os

EXCLUDE_DIRS = {'.git', '__pycache__', 'venv', '.venv', 'env',
                 'node_modules', '.idea', '.vscode', 'dist', 'build'}

INCLUDE_EXTENSIONS = {'.py'}

results = []

for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith('.')]

    for filename in files:
        ext = os.path.splitext(filename)[1]
        if ext not in INCLUDE_EXTENSIONS:
            continue

        filepath = os.path.join(root, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                line_count = len(content.splitlines())
                results.append({"path": filepath, "lines": line_count})
        except UnicodeDecodeError:
            print(f"Skipping {filepath} (not readable as text)")

print(results)