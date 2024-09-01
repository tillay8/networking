import os, time, sys, signal
from datetime import datetime
from dateutil.relativedelta import relativedelta
from threading import Thread

lines_shown = 30
gmt_offset = 6
restrict = False
color_code = '\033[0;32m'
prefix = ""

if len(sys.argv) > 1:
    arg = sys.argv[1]
    if arg == 't':
        prefix = "User1: "
        color_code = '\033[0;31m'
    elif arg == 's':
        prefix = "User2: "
        color_code = '\033[0;34m'
    else:
        prefix = f"{arg}: "
    
    if len(sys.argv) > 2:
        color_code = f'\033[0;{sys.argv[2]}m'

def convert_to_time():
    utc_now = time.gmtime()
    hour = (utc_now.tm_hour - gmt_offset) % 24
    return time.strftime("%H:%M:%S", utc_now[:3] + (hour,) + utc_now[4:])

def ping(user_input):
    parts = user_input.split()
    highlighted_message = []
    highlight_code = '\033[0;46m'
    
    for part in parts:
        if part.startswith("@"):
            highlighted_message.append(f"{highlight_code}{part}{color_code}")
        else:
            highlighted_message.append(part)
    
    return ' '.join(highlighted_message)

def is_restricted(user_input):
    restricted_words = ["sigma", "skibidi", "rizz"]
    for word in restricted_words:
        if word in user_input.lower():
            return True
    return False

def log_message(user_input):
    if not restrict and not is_restricted(user_input):
        RESET = '\033[0m'
        highlighted_input = ping(user_input)
        with open(os.path.expanduser('~/messages.txt'), 'a') as f:
            f.write(f"{color_code}{prefix}{highlighted_input}{RESET}\n")
    else:
        print("dont say that")

def monitor_file_changes():
    file_path = os.path.expanduser('~/messages.txt')
    last_mod_time = os.path.getmtime(file_path)
    while True:
        current_mod_time = os.path.getmtime(file_path)
        if current_mod_time != last_mod_time:
            last_mod_time = current_mod_time
            refresh()

def refresh():
    os.system('clear')
    with open(os.path.expanduser('~/messages.txt'), 'r') as f:
        lines = f.readlines()
        print(''.join(lines[-lines_shown:]), end='')

def cleanup(signal_received, frame):
    with open(os.path.expanduser('~/messages.txt'), 'a') as f:
        f.write(f"[{prefix[:-2]} left the chat at {convert_to_time()}]\n")
    sys.exit(0)

def livefeed():
    with open(os.path.expanduser('~/messages.txt'), 'a') as f:
        f.write(f"[{prefix[:-2]} entered the chat at {convert_to_time()}]\n")
    Thread(target=monitor_file_changes, daemon=True).start()
    refresh()
    
    while True:
        user_input = input()
        if user_input:
            if user_input == ":skull:":
                log_message("💀")
            elif user_input == "/shrug":
                log_message("¯\_(ツ)_/¯")
            elif user_input == "clear":
                if input("are you sure? y/n: ") == "y":
                    os.system("echo > ~/messages.txt")
                    with open(os.path.expanduser('~/messages.txt'), 'a') as f:
                        f.write(f"[{prefix[:-2]} cleared chat at {convert_to_time()}]\n")
                else:
                    refresh()
            else:
                log_message(user_input)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, cleanup)
    livefeed()

