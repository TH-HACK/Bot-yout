import telebot
from pytube import YouTube
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

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
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "أرسل لي رابط فيديو اليوتيوب لتحميله.")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text
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
        bot.reply_to(message, "عذرًا، حدث خطأ. تأكد من أن الرابط صالح.")

# معالجة اختيار الجودة
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        data = call.data.split(':')
        media_type, itag, url = data[0], int(data[1]), data[2]
        yt = YouTube(url)
        
        if media_type == "video":
            video = yt.streams.get_by_itag(itag)
            video.download()
            with open(video.default_filename, 'rb') as video_file:
                bot.send_video(call.message.chat.id, video_file)
        
        elif media_type == "audio":
            audio = yt.streams.get_by_itag(itag)
            audio.download(filename='audio.mp4')
            with open('audio.mp4', 'rb') as audio_file:
                bot.send_audio(call.message.chat.id, audio_file)
                
    except Exception as e:
        bot.send_message(call.message.chat.id, "عذرًا، حدث خطأ أثناء التحميل.")

# تشغيل البوت
bot.polling()
