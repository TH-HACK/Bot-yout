import os
import telebot
from telebot import types
import yt_dlp
import time
from urllib.parse import urlparse, parse_qs, urlunparse

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

USERS_FILE = 'users.txt'
STATS_FILE = 'stats.txt'
VIDEO_DIR = 'video'
ADMIN_ID = 1457  # ايدي حسابك

if not os.path.exists(USERS_FILE):
    open(USERS_FILE, 'w').close()

if not os.path.exists(STATS_FILE):
    with open(STATS_FILE, 'w') as f:
        f.write("تيك توك 0\nيوتيوب 0\nإنستغرام 0\nفيسبوك 0\nتويتر 0\n")

if not os.path.exists(VIDEO_DIR):
    os.makedirs(VIDEO_DIR)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    save_user(message.from_user.id, message.from_user.username, message.from_user.first_name)

    btn_tiktok = types.InlineKeyboardButton("تيك توك", callback_data="tiktok")
    btn_instagram = types.InlineKeyboardButton("إنستغرام", callback_data="instagram")
    btn_youtube = types.InlineKeyboardButton("يوتيوب", callback_data="youtube")
    btn_facebook = types.InlineKeyboardButton("فيسبوك", callback_data="facebook")
    btn_twitter = types.InlineKeyboardButton("تويتر", callback_data="twitter")
    btn_developer = types.InlineKeyboardButton("المطور", url="https://t.me/z1_xa")
    btn_ggg = types.InlineKeyboardButton("قناة المطور", url="https://t.me/yqyqy66")

    markup.add(btn_tiktok)
    markup.add(btn_instagram, btn_youtube)
    markup.add(btn_facebook, btn_twitter)
    markup.add(btn_developer)
    markup.add(btn_ggg)

    bot.send_photo(
        chat_id=message.chat.id,
        photo="https://postimg.cc/rD2QgXDw/64f45a3f",  # رابط الصورة
        caption=f"""*👋┇أهلاً بك عزيزي

مع هذا البوت يمكنك تحميل المحتوى من عدة مواقع

في بوت التحميل من مواقع التواصل، 
يمكنك الآن تحميل فيديوهات صوتية من منصات مثل «« تيك توك، ✨إنستجرام✨، يوتيوب، ✨فيسبوك، ✨✨ وتويتر X»».*""",
        parse_mode="Markdown",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data in ["tiktok", "instagram", "youtube", "facebook", "twitter"])
def handle_platform_selection(call):
    platform = call.data
    bot.send_message(call.message.chat.id, f"""```مرحباً بك في قسم تنزيل من {platform}```

*- يمكنك تحميل مقاطع الفيديو العامة من تطبيق {platform} (بدون علامة مائية)

- فقط ارسل رابط المقطع الان*""", 
        parse_mode="Markdown" 
    )
    bot.register_next_step_handler(call.message, download_content, platform)

def clean_url(url):
    """إزالة المعلمات الإضافية من الرابط"""
    parsed_url = urlparse(url)
    clean_url = parsed_url._replace(query='').geturl()
    
    if 'twitter.com' in clean_url or 'x.com' in clean_url:
        if not clean_url.endswith('/'):
            clean_url += '/'
    
    return clean_url

def download_content(message, platform):
    url = message.text
    clean_video_url = clean_url(url)
    if platform == "tiktok" and 'tiktok.com' in clean_video_url:
        ask_format(message)
    elif platform == "instagram" and 'instagram.com' in clean_video_url:
        ask_format(message)
    elif platform == "youtube" and ('youtube.com' in clean_video_url or 'youtu.be' in clean_video_url):
        ask_format(message)
    elif platform == "facebook" and 'facebook.com' in clean_video_url:
        ask_format(message)
    elif platform == "twitter" and ('twitter.com' in clean_video_url or 'x.com' in clean_video_url):
        ask_format(message)
    else:
        bot.send_message(message.chat.id, f"يرجى إرسال رابط صحيح من {platform}.")
        bot.register_next_step_handler(message, download_content, platform)

def ask_format(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    btn_video = types.KeyboardButton("فيديو")
    btn_audio = types.KeyboardButton("صوت")
    markup.add(btn_video, btn_audio)
    bot.send_message(message.chat.id, "هل ترغب في تحميل الفيديو أو الصوت؟", reply_markup=markup)
    bot.register_next_step_handler(message, process_format_choice)

def process_format_choice(message):
    format_choice = message.text
    if format_choice == "فيديو":
        bot.send_message(message.chat.id, "⏳ جاري تحميل الفيديو...")
        download_video(message.text, message.chat.id)
    elif format_choice == "صوت":
        bot.send_message(message.chat.id, "⏳ جاري تحميل الصوت...")
        download_audio(message.text, message.chat.id)
    else:
        bot.send_message(message.chat.id, "يرجى اختيار فيديو أو صوت فقط.")
        bot.register_next_step_handler(message, process_format_choice)

def download_video(url, chat_id, remove_watermark=False, is_youtube=False):
    try:
        user_id = str(chat_id)
        video_path = os.path.join(VIDEO_DIR, f"{user_id}.mp4")

        ydl_opts = {
            'format': 'best',
            'outtmpl': video_path,
            'noplaylist': True,
            'socket_timeout': 99999,
            'retries': 3,
            'retry_wait': 5,
            'postprocessors': [],
        }

        if remove_watermark:
            ydl_opts['postprocessors'].append({
                'key': 'FFmpegVideoRemuxer',
                'preferedformat': 'mp4'
            })

        if is_youtube:
            cookies_file = 'cookies.txt'
            if os.path.exists(cookies_file):
                ydl_opts['cookiefile'] = cookies_file
            else:
                bot.send_message(chat_id, "🚨 لم يتم العثور على ملف الكوكيز. تأكد من وجوده في المسار المحدد.")

        bot.send_message(chat_id, "⏳ جاري تحميل الفيديو، يرجى الانتظار...")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)

            video_size = info_dict.get('filesize', 0)
            video_duration = info_dict.get('duration', 0)

            video_size_mib = video_size / (1024 * 1024) if video_size else 0
            video_duration_min = video_duration // 60
            video_duration_sec = video_duration % 60
            duration_str = f"{video_duration_min}:{video_duration_sec}"

            message_text = (f"🕡 {duration_str} - 💾 {video_size_mib:.2f} MIB")

        with open(video_path, "rb") as video:
            bot.send_video(chat_id, video, caption=message_text)

        os.remove(video_path)

    except Exception as e:
        bot.send_message(chat_id, f"🚨 حدث خطأ أثناء تحميل الفيديو: {e}")

def download_audio(url, chat_id):
    try:
        user_id = str(chat_id)
        audio_path = os.path.join(VIDEO_DIR, f"{user_id}.mp3")

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': audio_path,
            'noplaylist': True,
            'socket_timeout': 99999,
            'retries': 3,
            'retry_wait': 5,
            'postprocessors': [{
                'key': 'FFmpegAudioConvertor',
                'preferredformat': 'mp3',
            }],
        }

        bot.send_message(chat_id, "⏳ جاري تحميل الصوت، يرجى الانتظار...")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)

            audio_size = info_dict.get('filesize', 0)
            audio_size_mib = audio_size / (1024 * 1024) if audio_size else 0

            message_text = f"💾 {audio_size_mib:.2f} MIB"

        with open(audio_path, "rb") as audio:
            bot.send_audio(chat_id, audio, caption=message_text)

        os.remove(audio_path)

    except Exception as e:
        bot.send_message(chat_id, f"🚨 حدث خطأ أثناء تحميل الصوت: {e}")

def save_user(user_id, username, full_name):
    user_id = str(user_id)
    new_user = False
    with open(USERS_FILE, 'r') as f:
        users = f.read().splitlines()
    if user_id not in users:
        new_user = True
        with open(USERS_FILE, 'a') as f:
            f.write(user_id + '\n')

    if new_user:
        with open(USERS_FILE, 'r') as f:
            total_users = len(f.read().splitlines())

        bot.send_message(
            ADMIN_ID,
