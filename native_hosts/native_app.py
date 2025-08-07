import sys
import json
import struct
import subprocess
import platform
import os
import shutil

def read_message():
    raw_length = sys.stdin.buffer.read(4)
    if not raw_length:
        return None
    message_length = struct.unpack('=I', raw_length)[0]
    message = sys.stdin.buffer.read(message_length).decode('utf-8')
    return json.loads(message)

def send_message(message):
    encoded = json.dumps(message).encode('utf-8')
    sys.stdout.buffer.write(struct.pack('=I', len(encoded)))
    sys.stdout.buffer.write(encoded)
    sys.stdout.buffer.flush()

def get_installed_browsers():
    system = platform.system()
    available = []

    known_browsers = {
        "firefox": {
            "windows": "C:\\Program Files\\Mozilla Firefox\\firefox.exe",
            "mac": "/Applications/Firefox.app",
            "linux": "firefox"
        },
        "brave": {
            "windows": "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe",
            "mac": "/Applications/Brave Browser.app",
            "linux": "brave"
        },
        "edge": {
            "windows": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
            "mac": "/Applications/Microsoft Edge.app",
            "linux": "microsoft-edge"
        }
    }

    for browser, paths in known_browsers.items():
        if system == "Windows":
            if os.path.exists(paths["windows"]):
                available.append(browser)
        elif system == "Darwin":
            if os.path.exists(paths["mac"]):
                available.append(browser)
        elif system == "Linux":
            if shutil.which(paths["linux"]):
                available.append(browser)

    return available

def open_url_in_browser(browser, url):
    system = platform.system()

    try:
        if system == "Windows":
            paths = {
                "firefox": "C:\\Program Files\\Mozilla Firefox\\firefox.exe",
                "brave": "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe",
                "edge": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
            }
            exe = paths.get(browser)
            if exe and os.path.exists(exe):
                subprocess.Popen([exe, url])
            else:
                raise Exception("Browser not found.")
        elif system == "Darwin":
            subprocess.Popen(["open", "-a", browser.capitalize(), url])
        elif system == "Linux":
            subprocess.Popen([browser, url])
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    msg = read_message()
    if not msg:
        send_message({"status": "error", "message": "No input received"})
    elif msg["action"] == "get_browsers":
        send_message({"status": "ok", "browsers": get_installed_browsers()})
    elif msg["action"] == "open_url":
        send_message(open_url_in_browser(msg["browser"], msg["url"]))
