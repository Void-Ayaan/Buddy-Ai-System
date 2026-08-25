from core.pipeline import process_query_pipeline, PIPELINE_ACTION, PIPELINE_QUESTION
from core.self_upgrader import self_upgrade
from core.emotions import detect_emotion_from_input, get_current_emotion, format_emotional_response
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
from tools.camera_tools import capture_vision
from tools.health_tools import run_health_check
from tools.speed_tools import check_website_status
from tools.battery_tools import get_battery_details
from tools.dictionary_tools import get_word_definition
from tools.converter_tools import convert_units
from tools.process_tools import get_system_uptime, get_top_processes
from tools.calc_tools import evaluate_math
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
from tools.file_tools import (
    organize_folder,
    move_file,
    copy_file,
    delete_file,
    find_file
)
from tools.media_tools import (
    volume_up,
    volume_down,
    toggle_mute,
    play_pause,
    next_track,
    previous_track
)
from tools.screen_tools import take_screenshot
from tools.web_search_tools import search_google, search_youtube, search_wikipedia
from tools.reminder_tools import parse_timer_command
from memory.memory_manager import parse_and_save_memory, load_memory
from memory.cache_manager import get_cached_response, save_cached_response
from core.llm import ask_ai
from voice.tts import speak
from voice.greetings import get_random_greeting
from voice.animation import ThinkingAnimation
from voice.listener import listen_from_microphone
from voice.banner import print_tech_banner

# Display large creative tech ASCII logo banner
print_tech_banner()

greeting = get_random_greeting()
speak(greeting)

while True:
    try:
        user_input = input("You (press Enter to speak, or type): ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye, Boss!")
        break

    # If user presses Enter without typing, trigger Voice Microphone Input!
    if not user_input or user_input.lower() in ["mic", "speak", "voice"]:
        user_input = listen_from_microphone(timeout=4)
        if not user_input:
            continue

    # Dynamically update Buddy's emotional mood based on user input
    mood = detect_emotion_from_input(user_input)

    pipeline_type, action, payload = process_query_pipeline(user_input)

    # PIPELINE 1: FAST ACTION / TASK PROTOCOL (INSTANT <10ms EXECUTION - ZERO LLM LATENCY)
    if pipeline_type == PIPELINE_ACTION:
        if action == "disk_storage":
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
            with ThinkingAnimation("Buddy is coding self-upgrade..."):
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
                    response = f"Your name is {name}, and you are my {role}."
                elif name:
                    response = f"Your name is {name}."
                else:
                    facts = ", ".join([f"{k} is {v}" for k, v in data.items()])
                    response = f"Here is what I remember: {facts}."
            else:
                response = "I don't have any facts stored about you yet. Please tell me your name!"
            result = response

        format_emotional_response(result)
        speak(result)

    # PIPELINE 2: GENERAL KNOWLEDGE & MODEL CONVERSATION
    else:
        cached_response = get_cached_response(user_input)
        if cached_response:
            print("[ ⚡ Instant Cache Hit ]")
            format_emotional_response(cached_response)
            speak(cached_response)
        else:
            with ThinkingAnimation("Buddy is thinking..."):
                response = ask_ai(user_input)

            save_cached_response(user_input, response)
            format_emotional_response(response)
            speak(response)
