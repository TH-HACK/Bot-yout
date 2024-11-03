import telebot
from pytube import YouTube
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import re

API_TOKEN = '7901940137:AAGQfDnI_P-LN5U_BtJGCPmAaZNXJp80jdM'
bot = telebot.TeleBot(API_TOKEN)

# دالة لإظهار الجودات المتاحة
def get_streams(url):
    yt = YouTube(url)
    video_streams = yt.streams.filter(progressive=True, file_extension="mp4")
    audio_stream = yt.streams.filter(only_audio=True).first()
    qualities = {stream.itag: stream.resolution for stream in video_streams}
    audio_tag = audio_stream.itag if audio_stream else None
    return qualities, audio_tag

# دالة لتحويل الروابط المختصرة إلى الروابط الكاملة
def convert_youtube_url(url):
    if "youtu.be" in url:
        return url.replace("youtu.be", "youtube.com/watch?v=")
    return url

# رسالة الإبلاغ عن تحديث الروبوت
def send_startup_message(chat_id):
    bot.send_message(chat_id, "تم تحديث الروبوت وتفعيله!")

# استقبال رابط الفيديو
@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text.strip()
    print(f"Received URL: {url}")  # طباعة الرابط المستلم

    # تحويل الرابط إذا كان مختصرًا
    url = convert_youtube_url(url)

    # إزالة المعلمات الإضافية إذا كانت موجودة
    url = re.sub(r'(\?|&).+', '', url)

    if not url.startswith("http"):
        bot.reply_to(message, "عذرًا، تأكد من أن الرابط يبدأ بـ http:// أو https://")
        return

    try:
        qualities, audio_tag = get_streams(url)
        if not qualities:
            bot.reply_to(message, "عذرًا، لم أتمكن من العثور على أي جودات للفيديو.")
            return
        
        # إعداد لوحة الأزرار
        markup = InlineKeyboardMarkup()
        for itag, res in qualities.items():
            markup.add(InlineKeyboardButton(f"جودة {res}", callback_data=f"video:{itag}:{url}"))
        if audio_tag:
            markup.add(InlineKeyboardButton("تحميل كملف صوتي", callback_data=f"audio:{audio_tag}:{url}"))

        bot.reply_to(message, "اختر الجودة التي تريدها أو اختر تحميل كملف صوتي:", reply_markup=markup)
    except Exception as e:
        print(f"Error: {e}")  # طباعة الخطأ لتشخيص المشكلة
        bot.reply_to(message, "عذرًا، حدث خطأ. تأكد من أن الرابط صالح وأنه فيديو يوتيوب.")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        data = call.data.split(':')
        if data[0] == 'video':
            itag, url = data[1], data[2]
            stream = YouTube(url).streams.get_by_itag(itag)
            stream.download()
            bot.answer_callback_query(call.id, "تم تحميل الفيديو!")
        elif data[0] == 'audio':
            itag, url = data[1], data[2]
            stream = YouTube(url).streams.get_by_itag(itag)
            stream.download()
            bot.answer_callback_query(call.id, "تم تحميل الصوت!")
    except Exception as e:
        bot.answer_callback_query(call.id, "عذرًا، حدث خطأ أثناء التحميل.")

# معرف الدردشة الذي سترسل إليه رسالة التحديث
CHAT_ID = '5164991393'  # استبدل هذا بمعرف الدردشة الخاص بك

# إرسال رسالة عند بدء التشغيل
send_startup_message(CHAT_ID)

bot.polling()
