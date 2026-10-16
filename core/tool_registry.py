import os
import sys

# Import all tool functions for JSON schema dispatch
from tools.system_booster import run_turbo_boost, toggle_battery_saver
from tools.kill_tools import kill_all_user_processes, kill_named_process
from tools.system_tools import minimize_all_windows
from tools.power_tools import lock_pc, sleep_pc, shutdown_pc, restart_pc
from tools.ram_cleaner import optimize_ram_memory
from tools.cleanup_tools import clean_temp_files
from tools.code_file_tools import save_code_to_desktop, locate_last_saved_file
from tools.prompt_master import create_master_prompt
from tools.speed_tools import check_website_status
from tools.speed_test_tools import run_quick_speed_test
from tools.ping_tools import check_ping_latency
from tools.wifi_tools import check_wifi_signal_quality
from tools.media_tools import volume_up, volume_down, toggle_mute, play_pause
from tools.sound_test_tools import test_speaker_audio
from tools.calc_tools import evaluate_math
from tools.converter_tools import convert_units
from tools.dictionary_tools import get_word_definition
from tools.weather_tools import get_weather
from tools.news_tools import get_latest_news
from tools.notes_tools import add_note, get_notes, clear_notes
from tools.system_tools import open_app, open_chrome
from tools.reminder_tools import parse_timer_command
from tools.screen_tools import take_screenshot
from tools.process_tools import get_system_uptime
from tools.spec_tools import get_hardware_specs

def _code_agent_dispatch(args):
    from agents.coding_agent import CodingAgent
    agent = CodingAgent()
    req = args.get("request") or args.get("idea") or args.get("code") or ""
    return agent.process_code_request(req)

TOOL_REGISTRY = {
    "turbo_boost": {
        "description": "Execute full system performance turbo boost (RAM clean + DNS flush + temp cleanup)",
        "parameters": {"type": "object", "properties": {}},
        "func": lambda args: run_turbo_boost()
    },
    "optimize_ram": {
        "description": "Reclaim and optimize RAM memory headroom",
        "parameters": {"type": "object", "properties": {}},
        "func": lambda args: optimize_ram_memory()
    },
    "clean_temp": {
        "description": "Clear Windows temporary cache and junk files",
        "parameters": {"type": "object", "properties": {}},
        "func": lambda args: clean_temp_files()
    },
    "kill_all_processes": {
        "description": "Safely terminate all non-essential user background applications",
        "parameters": {"type": "object", "properties": {}},
        "func": lambda args: kill_all_user_processes()
    },
    "kill_named_process": {
        "description": "Kill a specific named background process (e.g. chrome.exe, notepad.exe)",
        "parameters": {
            "type": "object",
            "properties": {
                "process_name": {"type": "string", "description": "Process executable name to terminate"}
            },
            "required": ["process_name"]
        },
        "func": lambda args: kill_named_process(args.get("process_name", ""))
    },
    "minimize_all_windows": {
        "description": "Minimize all open windows and show desktop (Win + D)",
        "parameters": {"type": "object", "properties": {}},
        "func": lambda args: minimize_all_windows()
    },
    "lock_pc": {
        "description": "Lock Windows workstation screen",
        "parameters": {"type": "object", "properties": {}},
        "func": lambda args: lock_pc()
    },
    "sleep_pc": {
        "description": "Put Windows PC into sleep state",
        "parameters": {"type": "object", "properties": {}},
        "func": lambda args: sleep_pc()
    },
    "code_agent": {
        "description": "Generate, build, or deploy custom software, Python scripts, Pygame games/animations, or web applications",
        "parameters": {
            "type": "object",
            "properties": {
                "request": {"type": "string", "description": "Description of the code, script, game, or web app to build"}
            },
            "required": ["request"]
        },
        "func": lambda args: _code_agent_dispatch(args)
    },
    "save_code_to_desktop": {
        "description": "Write code or script to Desktop file",
        "parameters": {
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "The script content to save"},
                "filename": {"type": "string", "description": "Optional file name like script.py"}
            },
            "required": ["code"]
        },
        "func": lambda args: save_code_to_desktop(args.get("code", ""), args.get("filename"))
    },
    "make_master_prompt": {
        "description": "Generate Master Prompt from raw user idea",
        "parameters": {
            "type": "object",
            "properties": {
                "idea": {"type": "string", "description": "Idea to engineer into a master prompt"}
            },
            "required": ["idea"]
        },
        "func": lambda args: create_master_prompt(args.get("idea", ""))
    },
    "run_speed_test": {
        "description": "Run real-time network download/upload speed test",
        "parameters": {"type": "object", "properties": {}},
        "func": lambda args: run_quick_speed_test()
    },
    "check_ping": {
        "description": "Check network ping latency to host",
        "parameters": {
            "type": "object",
            "properties": {
                "host": {"type": "string", "description": "Host address or IP (default 8.8.8.8)"}
            }
        },
        "func": lambda args: check_ping_latency(args.get("host", "8.8.8.8"))
    },
    "check_website": {
        "description": "Check if a website is online or experiencing downtime",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "URL of the website to test"}
            },
            "required": ["url"]
        },
        "func": lambda args: check_website_status(args.get("url", ""))
    },
    "volume_up": {
        "description": "Increase system audio volume",
        "parameters": {"type": "object", "properties": {}},
        "func": lambda args: volume_up()
    },
    "volume_down": {
        "description": "Decrease system audio volume",
        "parameters": {"type": "object", "properties": {}},
        "func": lambda args: volume_down()
    },
    "toggle_mute": {
        "description": "Mute or unmute system audio",
        "parameters": {"type": "object", "properties": {}},
        "func": lambda args: toggle_mute()
    },
    "evaluate_math": {
        "description": "Evaluate mathematical calculations or arithmetic expressions",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "Mathematical expression like 24 * 7"}
            },
            "required": ["expression"]
        },
        "func": lambda args: evaluate_math(args.get("expression", ""))
    },
    "get_weather": {
        "description": "Get live weather conditions and temperature for a city (or user location if omitted)",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "City name, or empty for auto-detected location"}
            }
        },
        "func": lambda args: get_weather(args.get("city", None))
    },
    "get_top_news": {
        "description": "Get latest top news headlines",
        "parameters": {"type": "object", "properties": {}},
        "func": lambda args: get_latest_news()
    },
    "add_note": {
        "description": "Add a user note or task to local notes manager",
        "parameters": {
            "type": "object",
            "properties": {
                "note": {"type": "string", "description": "The note text to store"}
            },
            "required": ["note"]
        },
        "func": lambda args: add_note(args.get("note", ""))
    },
    "get_notes": {
        "description": "Retrieve all saved user notes",
        "parameters": {"type": "object", "properties": {}},
        "func": lambda args: get_notes()
    },
    "open_app": {
        "description": "Open or launch a desktop application (chrome, vscode, notepad, calculator, terminal, etc.)",
        "parameters": {
            "type": "object",
            "properties": {
                "app_name": {"type": "string", "description": "Application name to launch"}
            },
            "required": ["app_name"]
        },
        "func": lambda args: open_app(args.get("app_name", "notepad"))
    },
    "locate_last_saved_file": {
        "description": "Locate and open the last saved code project file",
        "parameters": {"type": "object", "properties": {}},
        "func": lambda args: locate_last_saved_file()
    },
    "set_timer": {
        "description": "Set a timer or reminder alarm",
        "parameters": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string", "description": "Timer duration e.g. 25 minutes"}
            },
            "required": ["prompt"]
        },
        "func": lambda args: parse_timer_command(args.get("prompt", "25 minutes"))
    },
    "take_screenshot": {
        "description": "Take and save a screenshot of the current computer screen",
        "parameters": {"type": "object", "properties": {}},
        "func": lambda args: take_screenshot()
    },
    "get_system_uptime": {
        "description": "Get current operating system uptime since last boot",
        "parameters": {"type": "object", "properties": {}},
        "func": lambda args: get_system_uptime()
    },
    "get_hardware_specs": {
        "description": "Get CPU, RAM, disk, and GPU hardware system specifications",
        "parameters": {"type": "object", "properties": {}},
        "func": lambda args: get_hardware_specs()
    },
    "open_chrome": {
        "description": "Launch Google Chrome web browser",
        "parameters": {"type": "object", "properties": {}},
        "func": lambda args: open_chrome()
    }
}

def get_openai_tool_schemas():
    """Export all registered tools in OpenAI-compatible JSON schema."""
    tools = []
    for name, item in TOOL_REGISTRY.items():
        tools.append({
            "type": "function",
            "function": {
                "name": name,
                "description": item.get("description", ""),
                "parameters": item.get("parameters", {"type": "object", "properties": {}})
            }
        })
    return tools

def execute_registered_tool(tool_name, args=None):
    """Execute a registered tool by name with arguments and semantic aliases."""
    if args is None:
        args = {}
    
    # Semantic alias handling
    if tool_name == "open_app":
        app_name = str(args.get("app_name", "")).lower().strip()
        if "chrome" in app_name:
            return open_chrome()

    tool = TOOL_REGISTRY.get(tool_name)
    if not tool:
        return f"Tool '{tool_name}' not found in registry."
    try:
        return tool["func"](args)
    except Exception as e:
        return f"Tool execution error for '{tool_name}': {e}"

# Fine-grained intent mapping: maps specific phrases to 1-2 exact tools
SPECIFIC_INTENTS = [
    (["screenshot", "capture screen", "snapshot"], ["take_screenshot"]),
    (["uptime", "how long has the pc been on", "how long on"], ["get_system_uptime"]),
    (["spec", "specs", "hardware", "cpu info", "gpu info", "system info"], ["get_hardware_specs"]),
    (["chrome", "google chrome"], ["open_chrome", "open_app"]),
    (["weather", "forecast", "temperature", "rain", "sunny", "climate"], ["get_weather"]),
    (["timer", "alarm", "remind", "stopwatch"], ["set_timer"]),
    (["calculate", "calc", "math", "plus", "minus", "multiplied by", "divided by", "solve", "*", "+", "/"], ["evaluate_math"]),
    (["ram", "memory headroom", "clean ram", "optimize memory"], ["optimize_ram"]),
    (["boost", "turbo", "speed up my pc"], ["turbo_boost"]),
    (["clean temp", "clear junk", "temp files"], ["clean_temp"]),
    (["kill process", "terminate task", "close app"], ["kill_named_process"]),
    (["lock pc", "lock computer", "lock screen"], ["lock_pc"]),
    (["sleep pc", "put to sleep"], ["sleep_pc"]),
    (["minimize all", "show desktop"], ["minimize_all_windows"]),
    (["news", "headlines", "latest news"], ["get_top_news"]),
    (["ping", "latency"], ["check_ping"]),
    (["speed test", "network speed", "internet speed"], ["run_speed_test"]),
    (["volume up", "louder", "increase volume"], ["volume_up"]),
    (["volume down", "quieter", "lower volume"], ["volume_down"]),
    (["mute", "unmute", "silence"], ["toggle_mute"]),
    (["note", "notes", "remember to"], ["add_note", "get_notes"]),
    (["vs code", "vscode", "code editor", "open code", "open editor", "open app", "launch"], ["open_app"]),
    (["code a", "write code", "create script", "build a game", "pygame", "python script"], ["code_agent", "locate_last_saved_file"])
]

def select_candidate_tools(query):
    """
    Intelligently select 1-3 relevant tool schemas based on specific user intent.
    Keeps prompt concise (<100 tokens) so CPU prompt evaluation completes in 1-2 seconds.
    If purely conversational or knowledge question, returns empty list so model responds directly.
    """
    if not query:
        return []

    q_lower = query.lower()
    selected_names = []

    for keywords, tool_list in SPECIFIC_INTENTS:
        if any(k in q_lower for k in keywords):
            for t_name in tool_list:
                if t_name not in selected_names and t_name in TOOL_REGISTRY:
                    selected_names.append(t_name)
                    if len(selected_names) >= 3:
                        break
        if len(selected_names) >= 3:
            break

    if not selected_names:
        return []

    tools = []
    for name in selected_names[:3]:
        item = TOOL_REGISTRY.get(name)
        if item:
            tools.append({
                "type": "function",
                "function": {
                    "name": name,
                    "description": item.get("description", ""),
                    "parameters": item.get("parameters", {"type": "object", "properties": {}})
                }
            })
    return tools


