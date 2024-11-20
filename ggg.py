import os
import telebot,base64
from telebot import types
#import yt_dlp
import time
from urllib.parse import urlparse, parse_qs, urlunparse

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

USERS_FILE = 'users.txt'
STATS_FILE = 'stats.txt'
VIDEO_DIR = 'video'
ADMIN_ID = 5164991393 #ايدي حسابك+++تطوير @YQYQY6----@z1_xa

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
        photo=base64.b64decode("aHR0cHM6Ly9wb3N0aW1nLmNjLzBLQ2p2U1BO").decode('utf-8'),
        caption=base64.b64decode(f"8J+Ri+KUh9ij2YfZhNin2Ysg2KjZgyDYudiy2YrYstmF2Lkg2YfYsNinINin2YTYqNmI2Kog2YrZhdmD2YbZgyDYqtit2YXZitmEINin2YTZhdit2KrZiNmJINmF2YYg2LnYr9ipINmF2YjYp9mC2LnZgdmKINio2YjYqiDYp9mE2KrYrdmF2YrZhCDZhdmGINmF2YjYp9mC2Lkg2KfZhNiq2YjYp9i12YTYjCDZitmF2YPZhtmDINin2YTYotmGINiq2K3ZhdmK2YQg2YHZitiv2YrZiNmH2KfYqiDYtdmI2KrZitipINmF2YYg2YXZhti12KfYqiDZhdir2YQgwqvCqyDYqtmK2YMg2KrZiNmD2Iwg4pyo2KXZhtiz2KrYrNix2KfZheKcqNiMINmK2YjYqtmK2YjYqNiMIOKcqNmB2YrYs9io2YjZg9iMIOKcqOKcqCDZiNiq2YjZitiq2LEgWMK7wrsuINiq2LfZiNmK2LEgQHlxeXF5Ng===").decode('utf-8'), 
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
        download_video(clean_video_url, message.chat.id, remove_watermark=True)
        update_stats(platform)  
    elif platform == "instagram" and 'instagram.com' in clean_video_url:
        download_video(clean_video_url, message.chat.id)
        update_stats(platform)
    elif platform == "youtube" and ('youtube.com' in clean_video_url or 'youtu.be' in clean_video_url):
        download_video(clean_video_url, message.chat.id, is_youtube=True)
        update_stats(platform)
    elif platform == "facebook" and 'facebook.com' in clean_video_url:
        download_video(clean_video_url, message.chat.id)
        update_stats(platform)
    elif platform == "twitter" and ('twitter.com' in clean_video_url or 'x.com' in clean_video_url):
        download_video(clean_video_url, message.chat.id)
        update_stats(platform)
    else:
        bot.send_message(message.chat.id, f"يرجى إرسال رابط صحيح من {platform}.")
        bot.register_next_step_handler(message, download_content, platform)
        bot.register_next_step_handler(message, download_content, platform)

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

if not os.path.exists(STATS_FILE):
    with open(STATS_FILE, 'w') as f:
        f.write("تيك توك 0\nيوتيوب 0\nإنستغرام 0\nفيسبوك 0\nتويتر 0\n")

if not os.path.exists(VIDEO_DIR):
    os.makedirs(VIDEO_DIR)


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
            f"""• دخل شخص جديد إلى البوت الخاص بك 👾

- معلومات المستخدم الجديد:

- اسمه: {full_name or 'غير متوفر'}
- معرفه: @{username if username else 'غير متوفر'}
- ايديه: {user_id}

• اجمالي الاعضاء: {total_users}"""
        )


def update_stats(platform):
    platform_mapping = {
        "tiktok": "تيك توك",
        "youtube": "يوتيوب",
        "instagram": "إنستغرام",
        "facebook": "فيسبوك",
        "twitter": "تويتر",
    }
    platform_name = platform_mapping.get(platform.lower())
    
    if not platform_name:
        print(f"❌ لم يتم العثور على المنصة: {platform}")
        return

    try:
        with open(STATS_FILE, 'r') as f:
            stats = f.read().splitlines()

        new_stats = []
        found = False
        for line in stats:
            if line.startswith(platform_name):
                platform_label, count = line.rsplit(' ', 1)
                new_stats.append(f"{platform_label} {int(count) + 1}")
                found = True
            else:
                new_stats.append(line)

        if not found:
            new_stats.append(f"{platform_name} 1")  

        with open(STATS_FILE, 'w') as f:
            f.write('\n'.join(new_stats) + '\n')
        
        print(f"✅ تم تحديث الإحصائيات لمنصة {platform_name}.")

    except Exception as e:
        print(f"❌ خطأ أثناء تحديث الإحصائيات: {e}")


def get_stats():
    with open(STATS_FILE, 'r') as f:
        stats = f.read()
    
    with open(USERS_FILE, 'r') as f:
        users_count = len(f.read().splitlines())

    stats_message = f"\n\n📊 الإحصائيات:\n\n عدد الفيديوهات المحملة لكل منصة\n\n \n\n{stats}\n\n👥 عدد مستخدمي البوت: {users_count}"
    return stats_message

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, "🚫 هذا الأمر مخصص للمسؤول فقط.")
        return

    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_broadcast = types.InlineKeyboardButton("إذاعة", callback_data="broadcast")
    btn_broadcast_pin = types.InlineKeyboardButton("إذاعة بالتثبيت", callback_data="broadcast_pin")
    btn_stats = types.InlineKeyboardButton("الإحصائيات", callback_data="stats")
    markup.add(btn_broadcast, btn_broadcast_pin, btn_stats)
    bot.send_message(message.chat.id, "🔧 لوحة التحكم:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ["broadcast", "broadcast_pin", "stats"])
def handle_admin_actions(call):
    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "🚫 ليس لديك إذن.")
        return

    if call.data == "broadcast":
        msg = bot.send_message(call.message.chat.id, "✉️ أرسل الرسالة التي تريد إذاعتها:")
        bot.register_next_step_handler(msg, broadcast_message)

    elif call.data == "broadcast_pin":
        msg = bot.send_message(call.message.chat.id, "📌 أرسل الرسالة التي تريد إذاعتها مع التثبيت:")
        bot.register_next_step_handler(msg, broadcast_message, pin=True)

    elif call.data == "stats":
        stats = get_stats()
        bot.send_message(call.message.chat.id, stats)

def broadcast_message(message, pin=False):
    with open(USERS_FILE, 'r') as f:
        all_users = f.read().splitlines()

    for user_id in all_users:
        try:
            sent_message = bot.send_message(user_id, message.text)
            if pin:
                bot.pin_chat_message(user_id, sent_message.message_id)
        except Exception as e:
            print(f"🚨 خطأ أثناء الإرسال إلى {user_id}: {e}")


    update_stats(platform)

print('🚀 البوت يعمل الآن!')
bot.infinity_polling()
