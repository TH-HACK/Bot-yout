import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from pytube import YouTube

# دالة لتحميل الفيديو
def download_video(url):
    try:
        yt = YouTube(url)
        video_stream = yt.streams.get_highest_resolution()
        video_file = video_stream.download(output_path="downloads/")
        return video_file
    except Exception as e:
        print(f"Error in download_video: {e}")
        return None

# دالة الترحيب عند بدء المحادثة
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("مرحباً! أرسل لي رابط الفيديو من يوتيوب وسأقوم بتحميله لك.")

# دالة لمعالجة الرابط المرسل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = update.message.text.strip()
    if "youtube.com/watch" in url or "youtu.be/" in url:
        await update.message.reply_text("جاري تحميل الفيديو...")
        video_file = download_video(url)
        
        if video_file is None:
            # إذا كان هناك خطأ أثناء التحميل
            await update.message.reply_text("حدث خطأ أثناء تحميل الفيديو. تأكد من أن الرابط صحيح.")
        else:
            # إرسال الفيديو
            with open(video_file, 'rb') as video:
                await update.message.reply_video(video)
            # حذف الفيديو بعد إرساله
            os.remove(video_file)
    else:
        await update.message.reply_text("يرجى إرسال رابط صحيح من يوتيوب.")

# الدالة الرئيسية لتشغيل البوت
def main() -> None:
    # توكن البوت (قم باستخدام متغير بيئة آمن في التطبيقات الفعلية)
    TOKEN = os.getenv("BOT_TOKEN")

    # التحقق من وجود التوكن
    if not TOKEN:
        raise ValueError("TOKEN غير موجود في متغيرات البيئة")

    application = Application.builder().token(TOKEN).build()
    
    # إضافة المعالجات
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # بدء البوت
    application.run_polling()

if __name__ == '__main__':
    # إنشاء مجلد للتخزين
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
        
    main()
