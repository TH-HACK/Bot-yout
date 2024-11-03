const TelegramBot = require('node-telegram-bot-api');
const ytdl = require('ytdl-core');
const fs = require('fs');

// استبدل YOUR_BOT_TOKEN بالتوكن الخاص بك
const token = process.env.BOT_TOKEN;
const bot = new TelegramBot(token, { polling: true });

// الترحيب عند بدء المحادثة
bot.onText(/\/start/, (msg) => {
    bot.sendMessage(msg.chat.id, "مرحباً! أرسل لي رابط الفيديو من يوتيوب وسأقوم بتحميله لك.");
});

// معالجة الرسائل
bot.on('message', (msg) => {
    const chatId = msg.chat.id;
    const url = msg.text.trim();

    if (ytdl.validateURL(url)) {
        bot.sendMessage(chatId, "جاري تحميل الفيديو...");

        const stream = ytdl(url, { quality: 'highestvideo' });
        const filePath = `downloads/${Date.now()}.mp4`;

        stream.pipe(fs.createWriteStream(filePath));

        stream.on('end', () => {
            bot.sendVideo(chatId, filePath, {}, { filename: filePath })
                .then(() => {
                    fs.unlinkSync(filePath); // حذف الملف بعد إرساله
                });
        });

        stream.on('error', (error) => {
            console.error(error);
            bot.sendMessage(chatId, "حدث خطأ أثناء تحميل الفيديو. تأكد من أن الرابط صحيح.");
        });
    } else {
        bot.sendMessage(chatId, "يرجى إرسال رابط صحيح من يوتيوب.");
    }
});
