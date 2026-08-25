import os

def print_tech_banner():
    """Render a crisp, futuristic tactical ASCII HUD header for terminal execution."""
    os.system('') # Enable ANSI colors in Windows CMD

    CYAN = '\033[96m'
    WHITE = '\033[97m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

    banner = f"""
{CYAN}+====================================================================+
|  {WHITE}{BOLD}BUDDY AI - TACTICAL COMMAND HUD v2.5{CYAN}                              |
|  {YELLOW}ENCRYPTION: ACTIVE {CYAN}| {YELLOW}CORE STATUS: ONLINE {CYAN}| {YELLOW}PRIMARY NODE: ACCESSIBLE{CYAN}  |
+====================================================================+
|                                                                    |
|  {WHITE}{BOLD} [BBBBB]  [U   U] [DDDD ] [DDDD ] [Y   Y]    [AAA ] [I]{CYAN}          |
|  {WHITE}{BOLD} [B   B]  [U   U] [D   D] [D   D]  [Y Y]     [A  A] [I]{CYAN}          |
|  {WHITE}{BOLD} [BBBBB]  [U   U] [D   D] [D   D]   [Y]      [AAAA] [I]{CYAN}          |
|  {WHITE}{BOLD} [B   B]  [U   U] [D   D] [D   D]   [Y]      [A  A] [I]{CYAN}          |
|  {WHITE}{BOLD} [BBBBB]  [UUUUU] [DDDD ] [DDDD ]   [Y]      [A  A] [I]{CYAN}          |
|                                                                    |
+====================================================================+
|  {YELLOW}[ HARDWARE ]{WHITE} CPU/RAM: MONITORING {CYAN}| {YELLOW}[ VISION ]{WHITE} CAM: CAPABLE            |
|  {YELLOW}[ SPEECH ]{WHITE} TTS/STT: ONLINE    {CYAN}| {YELLOW}[ WEB HUD ]{WHITE} HTTP://127.0.0.1:5000   |
+====================================================================+{RESET}
"""
    print(banner)

if __name__ == "__main__":
    print_tech_banner()
