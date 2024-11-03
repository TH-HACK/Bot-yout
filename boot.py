import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from pytube import YouTube
from telegram import InputFile

# دالة لتحميل الفيديو
def download_video(url):
    try:
        yt = YouTube(url)
        video_stream = yt.streams.get_highest_resolution()
        video_file = video_stream.download(output_path="downloads/")
        return video_file
    except Exception as e:
        return str(e)

# الدالة للتعامل مع الأمر /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("مرحباً! أرسل لي رابط الفيديو من يوتيوب وسأقوم بتحميله لك.")

# الدالة لتحميل الفيديو من الرابط المرسل
def handle_message(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    if "youtube.com/watch" in url or "youtu.be/" in url:
        update.message.reply_text("جاري تحميل الفيديو...")
        video_file = download_video(url)
        
        if isinstance(video_file, str):
            # إذا كان هناك خطأ
            update.message.reply_text(f"حدث خطأ: {video_file}")
        else:
            # إرسال الفيديو
            with open(video_file, 'rb') as video:
                update.message.reply_video(video)
            # حذف الفيديو بعد إرساله
            os.remove(video_file)
    else:
        update.message.reply_text("يرجى إرسال رابط صحيح من يوتيوب.")

# الدالة الرئيسية
def main() -> None:
    # إعداد البوت
    updater = Updater("7901940137:AAGQfDnI_P-LN5U_BtJGCPmAaZNXJp80jdM", use_context=True)
    
    # إضافة المعالجات
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    
    # بدء البوت
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    # إنشاء مجلد للتخزين
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
        
    main()
