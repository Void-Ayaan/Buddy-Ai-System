def get_capabilities_guide():
    """Render a comprehensive Buddy capability guide banner and return speech summary."""
    banner = """
+-----------------------------------------------------------------------+
|                       BUDDY AI CAPABILITIES GUIDE                     |
+-----------------------------------------------------------------------+
| [1] VISION EYE & CAMERA    - "see this", "read image", "open camera"  |
| [2] SYSTEM PERFORMANCE     - "clean ram", "clean temp", "system scan" |
| [3] MULTI-AGENT SWARM      - "swarm status", "ping", "speed test"     |
| [4] TACTICAL PROTOCOLS     - "coding mode", "work mode", "lock pc"    |
| [5] UTILITIES & SECURITY   - "generate password", "kill process"      |
+-----------------------------------------------------------------------+
"""
    print(banner)
    return "Here are my capabilities, Boss! I can analyze camera photos, read images, optimize RAM, clean temp files, kill processes, run speed tests, generate passwords, and execute system commands!"
