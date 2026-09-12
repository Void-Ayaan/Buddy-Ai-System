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
from tools.system_tools import open_app
from tools.reminder_tools import parse_timer_command

TOOL_REGISTRY = {
    "turbo_boost": {
        "description": "Execute full system performance turbo boost (RAM clean + DNS flush + temp cleanup)",
        "func": lambda args: run_turbo_boost()
    },
    "optimize_ram": {
        "description": "Reclaim and optimize RAM memory headroom",
        "func": lambda args: optimize_ram_memory()
    },
    "clean_temp": {
        "description": "Clear Windows temporary cache and junk files",
        "func": lambda args: clean_temp_files()
    },
    "kill_all_processes": {
        "description": "Safely terminate all non-essential user background applications",
        "func": lambda args: kill_all_user_processes()
    },
    "kill_named_process": {
        "description": "Kill a specific named background process (e.g. chrome.exe, notepad.exe)",
        "func": lambda args: kill_named_process(args.get("process_name", ""))
    },
    "minimize_all_windows": {
        "description": "Minimize all open windows and show desktop (Win + D)",
        "func": lambda args: minimize_all_windows()
    },
    "lock_pc": {
        "description": "Lock Windows workstation screen",
        "func": lambda args: lock_pc()
    },
    "sleep_pc": {
        "description": "Put Windows PC into sleep state",
        "func": lambda args: sleep_pc()
    },
    "save_code_to_desktop": {
        "description": "Write code or script to Desktop file",
        "func": lambda args: save_code_to_desktop(args.get("code", ""), args.get("filename"))
    },
    "make_master_prompt": {
        "description": "Generate Master Prompt from raw user idea",
        "func": lambda args: create_master_prompt(args.get("idea", ""))
    },
    "run_speed_test": {
        "description": "Run real-time network download/upload speed test",
        "func": lambda args: run_quick_speed_test()
    },
    "check_ping": {
        "description": "Check network ping latency to host",
        "func": lambda args: check_ping_latency(args.get("host", "8.8.8.8"))
    },
    "check_website": {
        "description": "Check if a website is online or experiencing downtime",
        "func": lambda args: check_website_status(args.get("url", ""))
    },
    "volume_up": {
        "description": "Increase system audio volume",
        "func": lambda args: volume_up()
    },
    "volume_down": {
        "description": "Decrease system audio volume",
        "func": lambda args: volume_down()
    },
    "toggle_mute": {
        "description": "Mute or unmute system audio",
        "func": lambda args: toggle_mute()
    },
    "evaluate_math": {
        "description": "Evaluate mathematical calculations",
        "func": lambda args: evaluate_math(args.get("expression", ""))
    },
    "get_weather": {
        "description": "Get live weather conditions for a city",
        "func": lambda args: get_weather(args.get("city", "London"))
    },
    "get_top_news": {
        "description": "Get latest top news headlines",
        "func": lambda args: get_latest_news()
    },
    "add_note": {
        "description": "Add a user note or task to local notes manager",
        "func": lambda args: add_note(args.get("note", ""))
    },
    "get_notes": {
        "description": "Retrieve all saved user notes",
        "func": lambda args: get_notes()
    },
    "open_app": {
        "description": "Open or launch a desktop application",
        "func": lambda args: open_app(args.get("app_name", "vscode"))
    },
    "locate_last_saved_file": {
        "description": "Locate and open the last saved code project file",
        "func": lambda args: locate_last_saved_file()
    },
    "set_timer": {
        "description": "Set a timer or reminder alarm",
        "func": lambda args: parse_timer_command(args.get("prompt", "25 minutes"))
    }
}

def execute_registered_tool(tool_name, args=None):
    """Execute a registered tool by name with arguments."""
    if args is None:
        args = {}
    tool = TOOL_REGISTRY.get(tool_name)
    if not tool:
        return f"Tool '{tool_name}' not found in registry."
    try:
        return tool["func"](args)
    except Exception as e:
        return f"Tool execution error for '{tool_name}': {e}"
