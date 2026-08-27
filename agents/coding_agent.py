import re
import os
from tools.code_file_tools import save_code_to_desktop

class CodingAgent:
    """
    AGENT-12: Autonomous Coding & Software Architecture Agent.
    Generates, debugs, refactors, and deploys production-ready code across Python, JS, C++, HTML/CSS, and SQL.
    """
    def __init__(self):
        self.name = "CODER"
        self.node_id = "AGENT-12"
        self.description = "Autonomous Code Generator, Debugger, and Software Architect."

    def process_code_request(self, prompt):
        """Process coding, debugging, refactoring, or script generation requests."""
        prompt_clean = prompt.strip()
        prompt_lower = prompt_clean.lower()

        # 1. Calculator Program Request
        if "calculator" in prompt_lower:
            code = (
                "def add(a, b): return a + b\n"
                "def subtract(a, b): return a - b\n"
                "def multiply(a, b): return a * b\n"
                "def divide(a, b): return a / b if b != 0 else 'Error: Division by zero'\n\n"
                "print('=== BUDDY AI CALCULATOR ===')\n"
                "n1 = float(input('Enter first number: '))\n"
                "op = input('Enter operator (+, -, *, /): ')\n"
                "n2 = float(input('Enter second number: '))\n\n"
                "if op == '+': print('Result:', add(n1, n2))\n"
                "elif op == '-': print('Result:', subtract(n1, n2))\n"
                "elif op == '*': print('Result:', multiply(n1, n2))\n"
                "elif op == '/': print('Result:', divide(n1, n2))\n"
                "else: print('Invalid operator!')\n"
            )
            saved_msg = save_code_to_desktop(code, "calculator.py")
            return (
                f"Here is your Python Calculator code, Boss!\n\n"
                f"```python\n{code}```\n\n"
                f"{saved_msg}"
            )

        # 2. Web Scraper Request
        elif any(k in prompt_lower for k in ["scraper", "scrape", "web scraper", "crawler"]):
            code = (
                "import urllib.request\n"
                "from bs4 import BeautifulSoup\n\n"
                "def scrape_website(url):\n"
                "    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}\n"
                "    req = urllib.request.Request(url, headers=headers)\n"
                "    with urllib.request.urlopen(req) as resp:\n"
                "        html = resp.read().decode('utf-8')\n"
                "        soup = BeautifulSoup(html, 'html.parser')\n"
                "        title = soup.title.string if soup.title else 'No Title'\n"
                "        print(f'Page Title: {title}')\n"
                "        return title\n\n"
                "if __name__ == '__main__':\n"
                "    scrape_website('https://example.com')\n"
            )
            saved_msg = save_code_to_desktop(code, "web_scraper.py")
            return (
                f"Here is your Python Web Scraper script, Boss!\n\n"
                f"```python\n{code}```\n\n"
                f"{saved_msg}"
            )

        # 3. HTML / CSS Web Page Request
        elif any(k in prompt_lower for k in ["html", "website", "landing page", "web page"]):
            code = (
                "<!DOCTYPE html>\n"
                "<html lang=\"en\">\n"
                "<head>\n"
                "    <meta charset=\"UTF-8\">\n"
                "    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n"
                "    <title>Buddy AI Web Application</title>\n"
                "    <style>\n"
                "        body { background: #0a0a0f; color: #00f0ff; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }\n"
                "        .card { background: rgba(0,240,255,0.05); border: 1px solid #00f0ff; padding: 40px; border-radius: 12px; text-align: center; box-shadow: 0 0 20px rgba(0,240,255,0.2); }\n"
                "        h1 { margin-bottom: 10px; }\n"
                "    </style>\n"
                "</head>\n"
                "<body>\n"
                "    <div class=\"card\">\n"
                "        <h1>BUDDY AI APP</h1>\n"
                "        <p>Production Web Interface</p>\n"
                "    </div>\n"
                "</body>\n"
                "</html>\n"
            )
            saved_msg = save_code_to_desktop(code, "index.html")
            return (
                f"Here is your Production HTML/CSS Web Interface, Boss!\n\n"
                f"```html\n{code}```\n\n"
                f"{saved_msg}"
            )

        # 4. General Python Script
        else:
            code = (
                "# Autonomous Code Execution Script\n"
                "import os\n"
                "import sys\n\n"
                "def main():\n"
                "    print('Script execution initialized, Boss!')\n\n"
                "if __name__ == '__main__':\n"
                "    main()\n"
            )
            saved_msg = save_code_to_desktop(code, "script.py")
            return (
                f"Here is your Python script template, Boss!\n\n"
                f"```python\n{code}```\n\n"
                f"{saved_msg}"
            )
