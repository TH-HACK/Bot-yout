import os
from telegram import Update, InputFile
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
        return str(e)

# دالة للترحيب عند بدء المحادثة
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("مرحباً! أرسل لي رابط الفيديو من يوتيوب وسأقوم بتحميله لك.")

# دالة لتحميل الفيديو عند إرسال الرابط
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = update.message.text.strip()  # إزالة المسافات الزائدة
    if "youtube.com/watch" in url or "youtu.be/" in url:
        await update.message.reply_text("جاري تحميل الفيديو...")
        video_file = download_video(url)
        
        if isinstance(video_file, str):
            # إذا كان هناك خطأ
            await update.message.reply_text(f"حدث خطأ: {video_file}")
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
    # استبدل YOUR_BOT_TOKEN بالتوكن الخاص بك
    application = Application.builder().token("7901940137:AAGQfDnI_P-LN5U_BtJGCPmAaZNXJp80jdM").build()
    
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
