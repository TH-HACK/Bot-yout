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

# استقبال رابط الفيديو
@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text.strip()
    
    # إزالة المعلمات الإضافية إذا كانت موجودة
    url = re.sub(r'(\?|&).+', '', url)

    if not url.startswith("http"):
        bot.reply_to(message, "عذرًا، تأكد من أن الرابط يبدأ بـ http:// أو https://")
        return

    try:
        qualities, audio_tag = get_streams(url)
        
        # إعداد لوحة الأزرار
        markup = InlineKeyboardMarkup()
        for itag, res in qualities.items():
            markup.add(InlineKeyboardButton(f"جودة {res}", callback_data=f"video:{itag}:{url}"))
        if audio_tag:
            markup.add(InlineKeyboardButton("تحميل كملف صوتي", callback_data=f"audio:{audio_tag}:{url}"))

        bot.reply_to(message, "اختر الجودة التي تريدها أو اختر تحميل كملف صوتي:", reply_markup=markup)
    except Exception as e:
        print(e)  # طباعة الخطأ لتشخيص المشكلة
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

bot.polling()
