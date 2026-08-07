from pathlib import Path
import ast
import json

# ======================================================
# تنظیمات
# ======================================================

ROOT = Path.cwd()

IGNORE_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    ".idea",
    ".vscode",
    "node_modules",
    "dist",
    "build",
}

IGNORE_FILES = {
    ".DS_Store",
}

# ======================================================
# استخراج اطلاعات فایل‌های پایتون
# ======================================================

def analyze_python(file_path: Path):

    try:
        source = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        source = file_path.read_text(encoding="latin1")

    try:
        tree = ast.parse(source)
    except Exception:
        return {
            "lines": len(source.splitlines()),
            "classes": [],
            "functions": [],
            "methods": {},
            "imports": [],
            "error": "Syntax Error"
        }

    classes = []
    functions = []
    imports = []
    methods = {}

    for node in tree.body:

        if isinstance(node, ast.Import):
            for n in node.names:
                imports.append(n.name)

        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module or "")

        elif isinstance(node, ast.FunctionDef):
            functions.append(node.name)

        elif isinstance(node, ast.ClassDef):

            classes.append(node.name)

            method_list = []

            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    method_list.append(item.name)

            methods[node.name] = method_list

    return {
        "lines": len(source.splitlines()),
        "classes": classes,
        "functions": functions,
        "methods": methods,
        "imports": sorted(set(imports)),
    }

# ======================================================
# تولید فایل Tree
# ======================================================

tree_lines = []

def build_tree(folder, prefix=""):

    items = sorted(
        [
            p for p in folder.iterdir()
            if p.name not in IGNORE_DIRS
            and p.name not in IGNORE_FILES
        ],
        key=lambda x: (x.is_file(), x.name.lower())
    )

    for i, item in enumerate(items):

        last = i == len(items)-1

        branch = "└── " if last else "├── "

        line = prefix + branch + item.name

        tree_lines.append(line)

        if item.is_dir():

            extension = "    " if last else "│   "

            build_tree(item, prefix + extension)

# ======================================================
# اسکن پروژه
# ======================================================

project = {}

for file in ROOT.rglob("*.py"):

    if any(part in IGNORE_DIRS for part in file.parts):
        continue

    relative = file.relative_to(ROOT)

    project[str(relative)] = analyze_python(file)

build_tree(ROOT)

# ======================================================
# ذخیره خروجی‌ها
# ======================================================

tree_file = ROOT / "project_tree.txt"

with open(tree_file, "w", encoding="utf-8") as f:

    f.write(ROOT.name + "\n")

    for line in tree_lines:
        f.write(line + "\n")

json_file = ROOT / "project_details.json"

with open(json_file, "w", encoding="utf-8") as f:

    json.dump(
        project,
        f,
        indent=4,
        ensure_ascii=False
    )

print("="*50)
print("Done")
print("Tree File   :", tree_file)
print("Details File:", json_file)
print("="*50)