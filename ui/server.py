import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import http.server
import socketserver
import json
import psutil
import threading
import subprocess

from core.pipeline import process_query_pipeline, PIPELINE_ACTION, PIPELINE_QUESTION
from agents.swarm_master import swarm
from core.self_upgrader import self_upgrade
from core.emotions import detect_emotion_from_input, get_current_emotion
from tools.help_tools import get_capabilities_guide
from tools.news_tools import get_latest_news
from tools.speed_test_tools import run_quick_speed_test
from tools.sound_test_tools import test_speaker_audio
from tools.spec_tools import get_hardware_specs
from tools.swarm_tools import get_agent_swarm_status
from tools.ram_cleaner import optimize_ram_memory
from tools.password_tools import generate_secure_password
from tools.kill_tools import kill_named_process
from tools.ping_tools import check_ping_latency
from tools.recycle_tools import empty_recycle_bin
from tools.wifi_tools import check_wifi_signal_quality
from tools.disk_analyzer import analyze_disk_storage
from tools.audio_diag import get_audio_diagnostics
from tools.translator_tools import translate_phrase
from tools.jarvis_hud import run_buddy_system_scan
from tools.jarvis_workflows import activate_coding_mode, activate_work_mode, activate_relax_mode
from tools.cleanup_tools import clean_temp_files
from tools.camera_tools import capture_vision, get_last_camera_b64
from tools.health_tools import run_health_check
from tools.speed_tools import check_website_status
from tools.battery_tools import get_battery_details
from tools.dictionary_tools import get_word_definition
from tools.converter_tools import convert_units
from tools.process_tools import get_system_uptime, get_top_processes
from tools.calc_tools import evaluate_math
from tools.code_file_tools import save_code_to_desktop, locate_last_saved_file
from tools.learner_tools import learn_topic_from_internet
from tools.prompt_master import create_master_prompt
from tools.qr_tools import get_mobile_connect_info
from tools.phone_bridge import initiate_mobile_audio_call
from tools.system_tools import (
    open_chrome,
    open_website,
    open_app,
    close_app,
    minimize_window,
    get_current_time,
    get_current_date,
    get_system_info,
    fix_microphone,
    trigger_dictation
)
from tools.weather_tools import get_weather
from tools.power_tools import lock_pc, sleep_pc, shutdown_pc, restart_pc, cancel_shutdown
from tools.clipboard_tools import read_clipboard, copy_to_clipboard
from tools.network_tools import get_network_info
from tools.notes_tools import add_note, get_notes, clear_notes
from tools.volume_slider import parse_volume_command
from tools.fun_tools import get_joke, get_fact, get_quote
from tools.file_tools import organize_folder, move_file, copy_file, delete_file, find_file
from tools.media_tools import volume_up, volume_down, toggle_mute, play_pause, next_track, previous_track
from tools.screen_tools import take_screenshot
from tools.web_search_tools import search_google, search_youtube, search_wikipedia
from tools.reminder_tools import parse_timer_command
from memory.memory_manager import parse_and_save_memory, load_memory
from memory.cache_manager import get_cached_response, save_cached_response
from core.llm import ask_ai
from voice.tts import speak, set_web_mode
from voice.listener import listen_from_microphone

set_web_mode(True)

PORT = 5000
UI_DIR = os.path.dirname(os.path.abspath(__file__))

# Global Multi-Device Event Sync Log Buffer
SYNC_LOG_BUFFER = []

def open_standalone_app_window(url):
    """Launch HUD in Full Screen Standalone App Window without tabs, address bars, or URL clutter."""
    try:
        subprocess.Popen(f'start msedge --app={url} --start-maximized', shell=True)
    except Exception:
        try:
            subprocess.Popen(f'start chrome --app={url} --start-maximized', shell=True)
        except Exception:
            import webbrowser
            webbrowser.open(url)

def get_telemetry_json():
    try:
        cpu = int(psutil.cpu_percent(interval=0.1))
        ram = int(psutil.virtual_memory().percent)
        battery = psutil.sensors_battery()
        bat_val = int(battery.percent) if battery else 100
        mood = get_current_emotion()["badge"]
        swarm_data = swarm.get_real_swarm_telemetry()
        return {
            "cpu": cpu,
            "ram": ram,
            "battery": bat_val,
            "mood": mood,
            "swarm": swarm_data
        }
    except Exception:
        return {
            "cpu": 15,
            "ram": 42,
            "battery": 90,
            "mood": "[ Mood: Loyal Assistant (o7) ]",
            "swarm": swarm.get_real_swarm_telemetry()
        }

def execute_command_string(user_input):
    mood = detect_emotion_from_input(user_input)
    pipeline_type, action, payload = process_query_pipeline(user_input)

    swarm.set_active_workflow(action)
    should_compact = False

    if pipeline_type == PIPELINE_ACTION:
        if action in ["open_chrome", "open_url", "open_app", "coding_mode", "work_mode", "google_search", "youtube_search", "minimize"]:
            should_compact = True

        if action == "make_master_prompt":
            result = create_master_prompt(payload)
        elif action == "connect_mobile_audio":
            call_info = initiate_mobile_audio_call(PORT)
            result = call_info["text"]
        elif action == "learn_topic":
            result = learn_topic_from_internet(payload)
        elif action == "save_code_desktop":
            result = save_code_to_desktop(payload)
        elif action == "locate_code_file":
            result = locate_last_saved_file()
        elif action == "disk_storage":
            result = analyze_disk_storage()
        elif action == "audio_diagnostics":
            result = get_audio_diagnostics()
        elif action == "empty_recycle_bin":
            result = empty_recycle_bin()
        elif action == "check_wifi":
            result = check_wifi_signal_quality()
        elif action == "kill_process":
            result = kill_named_process(payload)
        elif action == "check_ping":
            result = check_ping_latency()
        elif action == "optimize_ram":
            result = optimize_ram_memory()
        elif action == "generate_password":
            result = generate_secure_password()
        elif action == "swarm_status":
            result = get_agent_swarm_status()
        elif action == "sound_test":
            result = test_speaker_audio()
        elif action == "get_specs":
            result = get_hardware_specs()
        elif action == "speed_test":
            result = run_quick_speed_test()
        elif action == "translate_phrase":
            result = translate_phrase(payload)
        elif action == "capture_vision":
            result = capture_vision()
        elif action == "battery_details":
            result = get_battery_details()
        elif action == "word_definition":
            result = get_word_definition(payload)
        elif action == "health_check":
            result = run_health_check()
        elif action == "check_website":
            result = check_website_status(payload)
        elif action == "convert_units":
            result = convert_units(payload)
        elif action == "calculate_math":
            result = evaluate_math(payload)
        elif action == "get_uptime":
            result = get_system_uptime()
        elif action == "top_processes":
            result = get_top_processes()
        elif action == "get_capabilities":
            result = get_capabilities_guide()
        elif action == "get_news":
            result = get_latest_news()
        elif action == "jarvis_scan":
            result = run_buddy_system_scan()
        elif action == "coding_mode":
            result = activate_coding_mode()
        elif action == "work_mode":
            result = activate_work_mode()
        elif action == "relax_mode":
            result = activate_relax_mode()
        elif action == "clean_temp":
            result = clean_temp_files()
        elif action == "get_mood":
            current_badge = get_current_emotion()["badge"]
            result = f"I am currently in a great mood {current_badge}! Ready to accomplish whatever you need, Boss."
        elif action == "set_volume_percent":
            result = parse_volume_command(payload)
        elif action == "network_info":
            result = get_network_info()
        elif action == "add_note":
            result = add_note(payload)
        elif action == "get_notes":
            result = get_notes()
        elif action == "clear_notes":
            result = clear_notes()
        elif action == "get_joke":
            result = get_joke()
        elif action == "get_fact":
            result = get_fact()
        elif action == "get_quote":
            result = get_quote()
        elif action == "weather":
            result = get_weather(payload)
        elif action == "lock_pc":
            result = lock_pc()
        elif action == "sleep_pc":
            result = sleep_pc()
        elif action == "shutdown_pc":
            result = shutdown_pc(10)
        elif action == "restart_pc":
            result = restart_pc(10)
        elif action == "cancel_shutdown":
            result = cancel_shutdown()
        elif action == "read_clipboard":
            result = read_clipboard()
        elif action == "copy_clipboard":
            result = copy_to_clipboard(payload)
        elif action == "fix_mic":
            result = fix_microphone()
        elif action == "dictation":
            result = trigger_dictation()
        elif action == "self_upgrade":
            result = self_upgrade(payload)
        elif action == "organize_files":
            result = organize_folder(payload)
        elif action == "move_file":
            src, dst = payload
            result = move_file(src, dst)
        elif action == "copy_file":
            src, dst = payload
            result = copy_file(src, dst)
        elif action == "delete_file":
            result = delete_file(payload)
        elif action == "find_file":
            result = find_file(payload)
        elif action == "time":
            result = get_current_time()
        elif action == "date":
            result = get_current_date()
        elif action == "system_info":
            result = get_system_info()
        elif action == "close_app":
            result = close_app(payload)
        elif action == "minimize":
            result = minimize_window()
        elif action == "volume_up":
            result = volume_up()
        elif action == "volume_down":
            result = volume_down()
        elif action == "toggle_mute":
            result = toggle_mute()
        elif action == "play_pause":
            result = play_pause()
        elif action == "next_track":
            result = next_track()
        elif action == "previous_track":
            result = previous_track()
        elif action == "screenshot":
            result = take_screenshot()
        elif action == "google_search":
            result = search_google(payload)
        elif action == "youtube_search":
            result = search_youtube(payload)
        elif action == "wiki_search":
            result = search_wikipedia(payload)
        elif action == "timer":
            result = parse_timer_command(payload)
        elif action == "open_chrome":
            result = open_chrome()
        elif action == "open_url":
            url, name = payload
            result = open_website(url, name)
        elif action == "open_app":
            result = open_app(payload)
        elif action == "remember":
            result = parse_and_save_memory(payload)
        elif action == "recall":
            data = load_memory()
            if data:
                name = data.get("name")
                role = data.get("role")
                if name and role:
                    result = f"Your name is {name}, and you are my {role}."
                elif name:
                    result = f"Your name is {name}."
                else:
                    facts = ", ".join([f"{k} is {v}" for k, v in data.items()])
                    result = f"Here is what I remember: {facts}."
            else:
                result = "I don't have any facts stored about you yet."
        else:
            result = f"Executing protocol: {action}"
    else:
        cached_response = get_cached_response(user_input)
        if cached_response:
            result = cached_response
        else:
            result = ask_ai(user_input)
            save_cached_response(user_input, result)

    # Append to global multi-device log buffer for real-time synchronization
    SYNC_LOG_BUFFER.append({"command": user_input, "response": result})
    if len(SYNC_LOG_BUFFER) > 50:
        SYNC_LOG_BUFFER.pop(0)

    return result, should_compact

class CyberHUDHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            with open(os.path.join(UI_DIR, "index.html"), "rb") as f:
                self.wfile.write(f.read())
        elif self.path == "/phone_call.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            with open(os.path.join(UI_DIR, "phone_call.html"), "rb") as f:
                self.wfile.write(f.read())
        elif self.path == "/api/telemetry":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(get_telemetry_json()).encode("utf-8"))
        elif self.path == "/api/mobile_info":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(get_mobile_connect_info(PORT)).encode("utf-8"))
        elif self.path == "/api/sync_logs":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"logs": SYNC_LOG_BUFFER}).encode("utf-8"))
        elif self.path.startswith("/camera_view.jpg"):
            self.send_response(200)
            self.send_header("Content-Type", "image/jpeg")
            self.end_headers()
            cam_path = os.path.join(UI_DIR, "camera_view.jpg")
            if not os.path.exists(cam_path):
                cam_path = os.path.join(BASE_DIR, "memory", "camera_view.jpg")
            if os.path.exists(cam_path):
                with open(cam_path, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.wfile.write(b"")
        else:
            super().do_GET()

    def do_POST(self):
        content_len = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_len).decode("utf-8")

        if self.path == "/api/command":
            data = json.loads(post_data) if post_data else {}
            cmd = data.get("command", "")
            res_text, should_compact = execute_command_string(cmd)
            mood = get_current_emotion()["badge"]

            response = {
                "response": res_text,
                "mood": mood,
                "compact_mode": should_compact,
                "telemetry": get_telemetry_json(),
                "camera_b64": get_last_camera_b64()
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))

        elif self.path == "/api/voice":
            rec_text = listen_from_microphone(timeout=4)
            should_compact = False
            if rec_text:
                res_text, should_compact = execute_command_string(rec_text)
            else:
                res_text = "No speech detected. Please speak clearly or type your command."
            
            mood = get_current_emotion()["badge"]
            response = {
                "recognized": rec_text,
                "response": res_text,
                "mood": mood,
                "compact_mode": should_compact,
                "telemetry": get_telemetry_json(),
                "camera_b64": get_last_camera_b64()
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

def start_ui_server():
    server = None
    target_port = PORT
    for candidate_port in [PORT, 5001, 5002]:
        try:
            server = ReusableTCPServer(("0.0.0.0", candidate_port), CyberHUDHandler)
            target_port = candidate_port
            break
        except OSError:
            continue

    if not server:
        server = ReusableTCPServer(("0.0.0.0", PORT), CyberHUDHandler)
        target_port = PORT

    mobile_info = get_mobile_connect_info(target_port)
    print("\n=======================================================")
    print(f" [ BUDDY CYBER HUD LOCAL: http://127.0.0.1:{target_port} ]")
    print(f" [ 📱 MULTI-DEVICE WI-FI CONTROL LINK: {mobile_info['url']} ]")
    print("=======================================================\n")

    open_standalone_app_window(f"http://127.0.0.1:{target_port}")
    server.serve_forever()

if __name__ == "__main__":
    start_ui_server()
