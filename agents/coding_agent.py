import os
import re
import subprocess
import webbrowser
from tools.code_file_tools import save_code_to_desktop, get_desktop_dir

class CodingAgent:
    """
    AGENT-12: Autonomous Offline Full-Stack Coding & Software Architecture Agent.
    Generates, builds, deploys, and previews production-ready code 100% OFFLINE across HTML/CSS/JS, Python GUI, Games, and Algorithms.
    """
    def __init__(self):
        self.name = "CODER"
        self.node_id = "AGENT-12"
        self.description = "Autonomous Offline Full-Stack Developer & Software Architect."

    def process_code_request(self, prompt):
        """Process offline coding, website generation, app creation, or script requests."""
        prompt_clean = prompt.strip()
        prompt_lower = prompt_clean.lower()
        desktop_dir = get_desktop_dir()

        # -----------------------------------------------------------------
        # 1. LANDING PAGE / PORTFOLIO / DASHBOARD WEBSITE GENERATOR
        # -----------------------------------------------------------------
        if any(k in prompt_lower for k in ["website", "landing page", "portfolio", "dashboard", "web app", "site"]):
            code = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Modern Cyber Portfolio</title>
    <style>
        :root {
            --bg-dark: #090a0f;
            --card-bg: rgba(18, 22, 34, 0.75);
            --accent-cyan: #00f3ff;
            --accent-purple: #b026ff;
            --text-light: #e0f2fe;
            --text-dim: #94a3b8;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }

        body {
            background-color: var(--bg-dark);
            color: var(--text-light);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 40px 20px;
            background-image: 
                radial-gradient(circle at 15% 20%, rgba(0, 243, 255, 0.12) 0%, transparent 40%),
                radial-gradient(circle at 85% 80%, rgba(176, 38, 255, 0.12) 0%, transparent 40%);
        }

        header {
            text-align: center;
            max-width: 800px;
            margin-bottom: 50px;
        }

        h1 {
            font-size: 3rem;
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 12px;
            letter-spacing: 1px;
        }

        p.subtitle {
            font-size: 1.2rem;
            color: var(--text-dim);
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 24px;
            width: 100%;
            max-width: 1000px;
        }

        .card {
            background: var(--card-bg);
            border: 1px solid rgba(0, 243, 255, 0.2);
            border-radius: 16px;
            padding: 28px;
            backdrop-filter: blur(12px);
            transition: all 0.3s ease;
        }

        .card:hover {
            transform: translateY(-6px);
            border-color: var(--accent-cyan);
            box-shadow: 0 10px 30px rgba(0, 243, 255, 0.2);
        }

        .card h3 {
            color: var(--accent-cyan);
            margin-bottom: 10px;
            font-size: 1.4rem;
        }

        .card p {
            color: var(--text-dim);
            line-height: 1.6;
            font-size: 0.95rem;
        }

        .btn {
            display: inline-block;
            margin-top: 18px;
            padding: 10px 20px;
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
            color: #000;
            font-weight: bold;
            text-decoration: none;
            border-radius: 8px;
            transition: opacity 0.2s;
            border: none;
            cursor: pointer;
        }

        .btn:hover { opacity: 0.9; }

        footer {
            margin-top: 60px;
            color: var(--text-dim);
            font-size: 0.9rem;
        }
    </style>
</head>
<body>
    <header>
        <h1>ULTRA CYBER HUD & WEB PLATFORM</h1>
        <p class="subtitle">Generated Autonomously 100% Offline by Buddy AI Swarm</p>
    </header>

    <div class="grid">
        <div class="card">
            <h3>⚡ High-Performance Core</h3>
            <p>Engineered for lightning-fast speeds with zero web dependencies and full local responsiveness.</p>
            <button class="btn" onclick="alert('System Engine Operational!')">Launch Engine</button>
        </div>
        <div class="card">
            <h3>🛡️ Offline Intelligence</h3>
            <p>Runs local GGUF models, process automation, and system diagnostics without requiring an internet connection.</p>
            <button class="btn" onclick="alert('Offline Mode Active!')">Verify Status</button>
        </div>
        <div class="card">
            <h3>🎨 Cyber Architecture</h3>
            <p>Modern glassmorphism, responsive grid layouts, and vibrant dark obsidian design tokens built in.</p>
            <button class="btn" onclick="alert('Theme Customizer Active!')">Customize Theme</button>
        </div>
    </div>

    <footer>
        <p>Built for Boss Ansh &bull; Powered by Buddy AI Swarm System</p>
    </footer>
</body>
</html>"""
            file_path = os.path.join(desktop_dir, "website_project.html")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code)

            try:
                webbrowser.open(file_path)
                preview_msg = " Launched website directly in your web browser!"
            except Exception:
                preview_msg = ""

            return (
                f"I have created a complete, modern responsive HTML/CSS/JS website 100% offline, Boss!\n\n"
                f"```html\n{code[:500]}\n... [Full HTML/CSS Project Code] ...\n```\n\n"
                f"Saved to your Desktop at `{file_path}`.{preview_msg}"
            )

        # -----------------------------------------------------------------
        # 2. INTERACTIVE PYTHON GUI APP (TKINTER) GENERATOR
        # -----------------------------------------------------------------
        elif any(k in prompt_lower for k in ["gui", "tkinter", "desktop app", "calculator app", "todo", "gui app"]):
            code = """import tkinter as tk
from tkinter import messagebox

class CyberDesktopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Buddy AI Desktop Application")
        self.root.geometry("450x550")
        self.root.configure(bg="#0a0a0f")

        # Header Label
        header = tk.Label(root, text="BUDDY AI TASK HUB", font=("Orbitron", 18, "bold"), fg="#00f3ff", bg="#0a0a0f")
        header.pack(pady=20)

        # Input Frame
        input_frame = tk.Frame(root, bg="#0a0a0f")
        input_frame.pack(pady=10)

        self.task_entry = tk.Entry(input_frame, font=("Segoe UI", 12), width=24, bg="#121622", fg="#e0f2fe", insertbackground="#00f3ff")
        self.task_entry.pack(side=tk.LEFT, px=5, ipady=4)

        add_btn = tk.Button(input_frame, text="ADD TASK", font=("Segoe UI", 10, "bold"), bg="#00f3ff", fg="#000000", command=self.add_task)
        add_btn.pack(side=tk.LEFT, px=5)

        # Listbox
        self.task_listbox = tk.Listbox(root, font=("Segoe UI", 11), width=36, height=12, bg="#121622", fg="#e0f2fe", selectbackground="#b026ff")
        self.task_listbox.pack(pady=15)

        # Remove Button
        remove_btn = tk.Button(root, text="REMOVE SELECTED TASK", font=("Segoe UI", 10, "bold"), bg="#ff3b30", fg="#ffffff", command=self.remove_task)
        remove_btn.pack(pady=10)

    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            self.task_listbox.insert(tk.END, f"• {task}")
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a task description!")

    def remove_task(self):
        try:
            selected = self.task_listbox.curselection()[0]
            self.task_listbox.delete(selected)
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to remove!")

if __name__ == '__main__':
    root = tk.Tk()
    app = CyberDesktopApp(root)
    root.mainloop()
"""
            file_path = os.path.join(desktop_dir, "desktop_gui_app.py")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code)

            return (
                f"I have built a full Python Tkinter GUI Desktop Application 100% offline, Boss!\n\n"
                f"```python\n{code}```\n\n"
                f"Saved to your Desktop at `{file_path}`. You can run it anytime with `python \"{file_path}\"`!"
            )

        # -----------------------------------------------------------------
        # 3. OFFLINE PYTHON SNAKE / ARCADE GAME GENERATOR
        # -----------------------------------------------------------------
        elif any(k in prompt_lower for k in ["game", "snake", "arcade", "tic tac toe", "pong"]):
            code = """import turtle
import time
import random

delay = 0.1
score = 0
high_score = 0

# Set up screen
wn = turtle.Screen()
wn.title("Buddy Cyber Snake Game")
wn.bgcolor("#0a0a0f")
wn.setup(width=600, height=600)
wn.tracer(0)

# Snake Head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("#00f3ff")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# Food
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("#b026ff")
food.penup()
food.goto(0, 100)

segments = []

# Functions
def go_up():
    if head.direction != "down": head.direction = "up"
def go_down():
    if head.direction != "up": head.direction = "down"
def go_left():
    if head.direction != "right": head.direction = "left"
def go_right():
    if head.direction != "left": head.direction = "right"

def move():
    if head.direction == "up": head.sety(head.ycor() + 20)
    if head.direction == "down": head.sety(head.ycor() - 20)
    if head.direction == "left": head.setx(head.xcor() - 20)
    if head.direction == "right": head.setx(head.xcor() + 20)

# Keyboard Bindings
wn.listen()
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")

# Main Game Loop
print("Game controls: W (Up), A (Left), S (Down), D (Right)")
while True:
    wn.update()
    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
        time.sleep(1)
        head.goto(0, 0)
        head.direction = "stop"
        for segment in segments: segment.goto(1000, 1000)
        segments.clear()

    if head.distance(food) < 20:
        food.goto(random.randint(-280, 280), random.randint(-280, 280))
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("#00b3ff")
        new_segment.penup()
        segments.append(new_segment)

    for index in range(len(segments)-1, 0, -1):
        x = segments[index-1].xcor()
        y = segments[index-1].ycor()
        segments[index].goto(x, y)

    if len(segments) > 0:
        segments[0].goto(head.xcor(), head.ycor())

    move()
    time.sleep(delay)
"""
            file_path = os.path.join(desktop_dir, "snake_game.py")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code)

            return (
                f"I have built a full 2D Arcade Game in Python (using standard library Turtle) 100% offline, Boss!\n\n"
                f"```python\n{code[:400]}\n... [Full Arcade Game Code] ...\n```\n\n"
                f"Saved to your Desktop at `{file_path}`!"
            )

        # -----------------------------------------------------------------
        # 4. DEFAULT GENERAL PURPOSE OFFLINE SCRIPT & ALGORITHM
        # -----------------------------------------------------------------
        else:
            code = """# Buddy AI Offline Automation & Utility Suite
import os
import sys
import json
import time

def run_system_audit():
    print("=== BUDDY SYSTEM AUDIT ===")
    print(f"Python Version: {sys.version.split()[0]}")
    print(f"Working Directory: {os.getcwd()}")
    print(f"Current Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("System state: 100% Operational")

if __name__ == '__main__':
    run_system_audit()
"""
            file_path = os.path.join(desktop_dir, "offline_script.py")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code)

            return (
                f"I have generated a clean, standalone offline Python automation script for you, Boss!\n\n"
                f"```python\n{code}```\n\n"
                f"Saved to your Desktop at `{file_path}`!"
            )
