import re

def route(text):
    text_lower = text.lower().strip()

    # 0a. Master Prompt Engineering Architect Protocol
    if any(p in text_lower for p in ["make prompt", "create prompt", "master prompt", "build prompt", "write prompt", "prompt engineering", "listen and make prompt"]):
        return "make_master_prompt", text

    # 0. Autonomous Agent Learner Protocol
    learn_match = re.search(r"\b(?:learn\s+about|learn|study|research)\s+(.+)", text_lower)
    if learn_match:
        target = learn_match.group(1).strip()
        if target not in ["mode", "protocol", "status"]:
            return "learn_topic", target

    # 0b. Code File Save & Desktop Location Queries
    if ("save" in text_lower or "create" in text_lower or "write" in text_lower) and ("desktop" in text_lower or "file" in text_lower) and ("code" in text_lower or "python" in text_lower or "calculator" in text_lower or "script" in text_lower):
        return "save_code_desktop", text

    if any(p in text_lower for p in ["where is it", "where it is", "tell me where it is", "where is the file", "where is my file", "file location", "where is calculator"]):
        return "locate_code_file", None

    # 1. Storage Breakdown & Drive Space Analyzer
    if any(p in text_lower for p in ["disk usage", "storage breakdown", "disk space", "check drives", "drive space", "storage info"]):
        return "disk_storage", None

    # 2. Audio Diagnostics Inspector
    if any(p in text_lower for p in ["audio status", "sound status", "audio info"]):
        return "audio_diagnostics", None

    # 3. Empty Recycle Bin Tool
    if any(p in text_lower for p in ["empty recycle bin", "empty trash", "clean recycle bin", "trash clean"]):
        return "empty_recycle_bin", None

    # 4. Wi-Fi Signal & Network Quality Inspector
    if any(p in text_lower for p in ["wifi signal", "wifi quality", "check wifi", "wifi strength", "wifi speed info"]):
        return "check_wifi", None

    # 5. Process Killer & Manager
    kill_match = re.search(r"\b(?:kill|stop|force close|terminate)\s+(?:process\s+)?([a-zA-Z0-9.\s]+)", text_lower)
    if kill_match:
        target = kill_match.group(1).strip()
        if target not in ["it", "this", "window", "app"]:
            return "kill_process", target

    # 6. Network Ping & Latency Inspector
    if any(p in text_lower for p in ["ping", "check ping", "ping latency", "network ping", "my ping"]):
        return "check_ping", None

    # 7. RAM Memory Cleaner & Optimizer
    if any(p in text_lower for p in ["clean ram", "free ram", "optimize ram", "ram cleanup", "ram cleaner"]):
        return "optimize_ram", None

    # 8. Secure Password Generator
    if any(p in text_lower for p in ["generate password", "secure password", "random password", "make password", "create password"]):
        return "generate_password", None

    # 9. AI Agent Swarm Status
    if any(p in text_lower for p in ["swarm status", "agent swarm", "show swarm", "swarm"]):
        return "swarm_status", None

    # 10. Speaker Sound Diagnostic Test
    if any(p in text_lower for p in ["sound test", "test speaker", "test sound", "speaker test"]):
        return "sound_test", None

    # 11. Hardware Specs Summarizer
    if any(p in text_lower for p in ["pc specs", "hardware specs", "system specs", "specs"]):
        return "get_specs", None

    # 12. Quick Internet Speed Test
    if any(p in text_lower for p in ["speed test", "internet speed", "check speed", "test speed", "network speed"]):
        return "speed_test", None

    # 13. Quick Language Translator
    if text_lower.startswith("translate ") or " translate " in text_lower:
        return "translate_phrase", text

    # 14. Buddy Vision & Camera Control (Single Snapshot & Continuous 24/7 Live Vision Eye)
    if any(p in text_lower for p in ["live vision", "continuous vision", "watch through camera", "keep watching", "turn on camera", "turn on live vision", "activate live vision", "live camera mode"]):
        return "toggle_live_vision", True
    if any(p in text_lower for p in ["stop live vision", "turn off live vision", "close camera"]):
        return "toggle_live_vision", False
    if any(p in text_lower for p in ["see this", "look at this", "what do you see", "what's in front of camera", "what is in front of camera", "take picture", "take a picture", "take photo", "take a photo", "camera vision", "open camera", "what's inside", "what is inside", "whats inside", "whst's inside", "whsts inside", "what's in the image", "what is in the image", "whats in the image", "whst's in the image", "read image", "describe image", "read text in image", "what do you see in the photo", "what is in the photo", "give details of image", "give details of photo", "give image details", "details of image", "tell me about image", "tell me about photo", "show details of image"]):
        return "capture_vision", None

    # 15. Battery Details
    if any(p in text_lower for p in ["battery status", "battery percentage", "am i charging", "battery time"]):
        return "battery_details", None

    # 16. Word Dictionary & Definitions
    if text_lower.startswith("define ") or "meaning of " in text_lower or "what does " in text_lower and " mean" in text_lower:
        return "word_definition", text

    # 17. Health Status & Storage Diagnostics
    if any(p in text_lower for p in ["health check", "laptop health", "disk health", "health status", "system health"]):
        return "health_check", None

    # 18. Website Down & Latency Detector
    if any(p in text_lower for p in ["is google down", "is github down", "is website down", "check website"]):
        return "check_website", text

    # 19. Unit & Currency Conversion
    if text_lower.startswith("convert ") or " convert " in text_lower or re.search(r"\d+\s*(?:usd|inr|eur|gbp|miles|km|kg|lbs)\s+to", text_lower):
        return "convert_units", text

    # 20. Math Calculations
    if text_lower.startswith("calculate ") or "percent of" in text_lower or "square root of" in text_lower:
        return "calculate_math", text

    # 21. System Uptime & Top Memory Processes
    if any(p in text_lower for p in ["system uptime", "uptime", "how long has my pc been on", "how long laptop has been on"]):
        return "get_uptime", None
    if any(p in text_lower for p in ["top processes", "top memory", "running processes"]):
        return "top_processes", None

    # 22. Capabilities & Help Commands
    if any(p in text_lower for p in ["what can you do", "capabilities", "show features", "tell me your capabilities", "list commands", "help me", "what are your features"]):
        return "get_capabilities", None

    # 23. News & Live Headlines
    if any(p in text_lower for p in ["news", "latest news", "top news", "tell me news", "headlines"]):
        return "get_news", None

    # 24. Buddy System Scan & Comprehensive Test Diagnostics
    if any(p in text_lower for p in ["system scan", "full scan", "buddy scan", "run diagnostic", "system diagnostic", "hud scan", "test everything", "test eerthing", "test eerything", "test system", "system test", "test all", "test buddy"]):
        return "jarvis_scan", None

    # 25. Buddy Workflows & Protocols
    if any(p in text_lower for p in ["coding mode", "code mode", "coding protocol", "developer mode"]):
        return "coding_mode", None
    if any(p in text_lower for p in ["work mode", "focus mode", "work protocol"]):
        return "work_mode", None
    if any(p in text_lower for p in ["relax mode", "gaming mode", "relax protocol"]):
        return "relax_mode", None

    # 26. Disk Cleanup & Temp File Removal
    if any(p in text_lower for p in ["clean temp", "clean temp files", "clean system", "free space", "disk cleanup", "clean junk"]):
        return "clean_temp", None

    # 27. Emotion & Mood Queries
    if any(p in text_lower for p in ["how are you feeling", "what is your mood", "how do you feel", "how are you"]):
        return "get_mood", None

    # 28. Volume Percentage Control
    if re.search(r"\b(?:set|change)\s+volume\s+to\s+\d+", text_lower) or re.search(r"\bvolume\s+\d+\s*%?", text_lower):
        return "set_volume_percent", text

    # 29. Network & IP Diagnostics
    if any(p in text_lower for p in ["ip address", "my ip", "wifi status", "internet status", "network status", "network info"]):
        return "network_info", None

    # 30. Notes & To-Do List Management
    if any(p in text_lower for p in ["add note", "take note", "note down", "add todo"]):
        return "add_note", text
    if any(p in text_lower for p in ["show notes", "read notes", "get notes", "my notes", "list notes"]):
        return "get_notes", None
    if any(p in text_lower for p in ["clear notes", "delete notes", "remove notes"]):
        return "clear_notes", None

    # 31. Jokes, Facts & Quotes
    if any(p in text_lower for p in ["joke", "make me laugh"]):
        return "get_joke", None
    if any(p in text_lower for p in ["fact", "tell me a fact"]):
        return "get_fact", None
    if any(p in text_lower for p in ["quote", "motivation"]):
        return "get_quote", None

    # 32. Weather & Temperature Queries
    if any(p in text_lower for p in ["weather", "temperature", "how is the weather"]):
        city_match = re.search(r"\b(?:in|at|for)\s+([a-zA-Z\s]+)", text_lower)
        city = city_match.group(1).strip() if city_match else None
        return "weather", city

    # 33. PC Power & Security Controls
    if any(p in text_lower for p in ["lock pc", "lock laptop", "lock my pc", "lock my laptop", "lock screen"]):
        return "lock_pc", None
    if any(p in text_lower for p in ["sleep pc", "sleep laptop", "put pc to sleep"]):
        return "sleep_pc", None
    if any(p in text_lower for p in ["cancel shutdown", "abort shutdown"]):
        return "cancel_shutdown", None
    if any(p in text_lower for p in ["shutdown pc", "shutdown laptop", "turn off pc", "turn off laptop"]):
        return "shutdown_pc", None
    if any(p in text_lower for p in ["restart pc", "restart laptop", "reboot pc", "reboot laptop"]):
        return "restart_pc", None

    # 34. Clipboard Management
    if any(p in text_lower for p in ["read clipboard", "what did i copy", "check clipboard", "clipboard content"]):
        return "read_clipboard", None
    copy_clip = re.search(r"\bcopy\s+(?:to\s+clipboard\s+)?(.+)", text_lower)
    if copy_clip and "file" not in text_lower:
        return "copy_clipboard", copy_clip.group(1).strip()

    # 35. Microphone Diagnostics & Windows Voice Typing
    if any(p in text_lower for p in ["fix mic", "fix microphone", "mic not working", "microphone not working", "check mic", "mic broken"]):
        return "fix_mic", None
    if any(p in text_lower for p in ["dictation", "voice typing", "windows dictation"]):
        return "dictation", None

    # 36. Self-Upgrade & Code Modifications
    if any(p in text_lower for p in ["upgrade yourself", "update yourself", "code yourself", "self upgrade", "add new feature", "improve yourself", "write code to"]):
        return "self_upgrade", text

    # 37. File Management Commands
    if any(p in text_lower for p in ["organize", "arrange", "clean up", "clean downloads", "clean desktop"]):
        folder = "downloads"
        if "desktop" in text_lower:
            folder = "desktop"
        elif "documents" in text_lower:
            folder = "documents"
        return "organize_files", folder

    move_match = re.search(r"\bmove\s+(?:file\s+)?(.+?)\s+to\s+(.+)", text_lower)
    if move_match:
        src = move_match.group(1).strip()
        dst = move_match.group(2).strip()
        return "move_file", (src, dst)

    copy_match = re.search(r"\bcopy\s+(?:file\s+)?(.+?)\s+to\s+(.+)", text_lower)
    if copy_match:
        src = copy_match.group(1).strip()
        dst = copy_match.group(2).strip()
        return "copy_file", (src, dst)

    delete_match = re.search(r"\b(?:delete|remove)\s+(?:file\s+|folder\s+)?(.+)", text_lower)
    if delete_match:
        target = delete_match.group(1).strip()
        if target not in ["it", "window", "app", "this"]:
            return "delete_file", target

    find_match = re.search(r"\b(?:find|search for)\s+file\s+(.+)", text_lower)
    if find_match:
        target = find_match.group(1).strip()
        return "find_file", target

    # 38. Timer & Reminder System
    if any(p in text_lower for p in ["timer", "remind me in", "set alarm"]):
        return "timer", text

    # 39. Time & Date Queries
    if "time" in text_lower:
        return "time", None
    if any(p in text_lower for p in ["date", "today", "toady"]):
        return "date", None

    # 40. Close & Minimize Window Controls
    if any(p in text_lower for p in ["close it", "close window", "close app", "close this"]):
        return "close_app", "it"

    close_match = re.search(r"\bclose\s+([a-zA-Z0-9.\s]+)", text_lower)
    if close_match:
        target = close_match.group(1).strip()
        for filler in ["please", "for me", "the", "app", "window"]:
            target = target.replace(filler, "").strip()
        return "close_app", target

    if any(p in text_lower for p in ["minimize", "minimize window", "minimize tab"]):
        return "minimize", None

    # 41. Volume & Media Controls
    if any(p in text_lower for p in ["volume up", "increase volume", "louder"]):
        return "volume_up", None
    if any(p in text_lower for p in ["volume down", "decrease volume", "quieter"]):
        return "volume_down", None
    if any(p in text_lower for p in ["mute", "unmute"]):
        return "toggle_mute", None
    if any(p in text_lower for p in ["play", "pause", "play pause"]):
        return "play_pause", None
    if "next track" in text_lower or "next song" in text_lower:
        return "next_track", None
    if "previous track" in text_lower or "previous song" in text_lower:
        return "previous_track", None

    # 42. Screenshot Capture
    if any(p in text_lower for p in ["screenshot", "take screenshot", "capture screen", "snap screen"]):
        return "screenshot", None

    # 43. Web Search Tools
    if "search google for" in text_lower or text_lower.startswith("google "):
        query = text_lower.replace("search google for", "").replace("google", "").strip()
        return "google_search", query
    if "search youtube for" in text_lower or text_lower.startswith("youtube "):
        query = text_lower.replace("search youtube for", "").replace("youtube", "").strip()
        return "youtube_search", query
    if "search wikipedia for" in text_lower or text_lower.startswith("wikipedia "):
        query = text_lower.replace("search wikipedia for", "").replace("wikipedia", "").strip()
        return "wiki_search", query

    # 44. System Info & Laptop Health
    if any(p in text_lower for p in ["battery", "system info", "cpu usage", "ram usage", "laptop status", "laptop health", "performance"]):
        return "system_info", None

    # 45. Open Apps and Websites
    open_match = re.search(r"\bopen\s+([a-zA-Z0-9.\s]+)", text_lower)
    if open_match:
        target = open_match.group(1).strip()
        for filler in ["please", "for me", "the", "app", "website"]:
            target = target.replace(filler, "").strip()

        if target in ["chrome", "google chrome", "browser"]:
            return "open_chrome", "Chrome"
        elif "." in target or target in ["youtube", "instagram", "google", "facebook", "twitter", "reddit", "github"]:
            clean_name = target.replace("www.", "").replace(".com", "").capitalize()
            url = target if "." in target else f"www.{target}.com"
            return "open_url", (url, clean_name)
        elif target:
            return "open_app", target

    # 46. Memory Queries
    if any(p in text_lower for p in ["my name is", "remember", "call me", "i'm your boss", "i am your boss"]):
        return "remember", text
    if any(p in text_lower for p in ["who am i", "what's my name", "what is my name", "do you know me"]):
        return "recall", text

    return "chat", text
