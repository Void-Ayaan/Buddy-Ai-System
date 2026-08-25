import os
import ast
import shutil
import sys
import subprocess
from core.llm import ask_ai
from tools.package_manager import ensure_package_in_requirements

BUDDY_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def create_backup(filepath):
    if os.path.exists(filepath):
        backup_path = f"{filepath}.bak"
        shutil.copy2(filepath, backup_path)
        return backup_path
    return None

def restore_backup(filepath):
    backup_path = f"{filepath}.bak"
    if os.path.exists(backup_path):
        shutil.copy2(backup_path, filepath)
        os.remove(backup_path)

def validate_python_code(code_str):
    try:
        ast.parse(code_str)
        return True, ""
    except SyntaxError as e:
        return False, str(e)

def self_upgrade(user_request):
    """Self-upgrader engine: Generates new features, tools, or code modifications for Buddy."""
    print(f"\n[ 🛠️ SELF-UPGRADE INITIATED ]: \"{user_request}\"")

    prompt = (
        f"You are Buddy's self-improvement module. The user requested an upgrade: '{user_request}'.\n"
        f"Write Python code or function to fulfill this upgrade.\n"
        f"Provide ONLY valid executable Python code block wrapped in ```python and ``` without markdown explanations."
    )

    code_response = ask_ai(prompt)

    # Extract code inside ```python ... ```
    if "```python" in code_response:
        raw_code = code_response.split("```python")[1].split("```")[0].strip()
    elif "```" in code_response:
        raw_code = code_response.split("```")[1].split("```")[0].strip()
    else:
        raw_code = code_response.strip()

    is_valid, err = validate_python_code(raw_code)
    if not is_valid:
        clean_prompt = f"Fix Python syntax error in code: {err}. Code: {raw_code}"
        fixed_response = ask_ai(clean_prompt)
        if "```python" in fixed_response:
            raw_code = fixed_response.split("```python")[1].split("```")[0].strip()
        elif "```" in fixed_response:
            raw_code = fixed_response.split("```")[1].split("```")[0].strip()
        else:
            raw_code = fixed_response.strip()

    is_valid, err = validate_python_code(raw_code)
    if not is_valid:
        return f"Self-upgrade failed due to code syntax validation: {err}"

    # Check for new imports in raw_code and auto-record in requirements.txt
    try:
        parsed_ast = ast.parse(raw_code)
        for node in ast.walk(parsed_ast):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    ensure_package_in_requirements(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    base_mod = node.module.split(".")[0]
                    ensure_package_in_requirements(base_mod)
    except Exception:
        pass

    # Write new tool module to tools/
    feature_slug = "".join([c if c.isalnum() else "_" for c in user_request.lower()[:20]]).strip("_")
    new_module_name = f"custom_{feature_slug}.py"
    target_file = os.path.join(BUDDY_DIR, "tools", new_module_name)

    try:
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(raw_code)

        return f"Self-upgrade successful! Added new tool module {new_module_name} to my codebase and updated requirements.txt, Boss!"
    except Exception as e:
        return f"Failed to save self-upgrade: {e}"
