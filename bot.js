const TelegramBot = require('node-telegram-bot-api');
const fs = require('fs');
const https = require('https');

// استبدل YOUR_BOT_TOKEN بالتوكن الخاص بك
const token = process.env.BOT_TOKEN;
const bot = new TelegramBot(token, { polling: true });

// الترحيب عند بدء المحادثة
bot.onText(/\/start/, (msg) => {
    bot.sendMessage(msg.chat.id, "مرحباً! أرسل لي رابط الصورة من Pinterest وسأقوم بتحميلها لك.");
});

// معالجة الرسائل
bot.on('message', (msg) => {
    const chatId = msg.chat.id;
    const url = msg.text.trim();

    // تحقق إذا كانت الرابط من Pinterest
    if (url.includes("pinterest.com")) {
        bot.sendMessage(chatId, "جاري تحميل الصورة...");

        // حاول تحميل الصورة من الرابط
        const imageUrl = url; // يمكنك تحسين هذا الجزء للحصول على رابط مباشر للصورة إذا كان لديك طريقة معينة

        const filePath = `downloads/${Date.now()}.jpg`;

        const file = fs.createWriteStream(filePath);
        https.get(imageUrl, (response) => {
            response.pipe(file);
            file.on('finish', () => {
                file.close(() => {
                    bot.sendPhoto(chatId, filePath, {}, { caption: "ها هي الصورة التي طلبتها!" })
                        .then(() => {
                            fs.unlinkSync(filePath); // حذف الملف بعد إرساله
                        })
                        .catch((error) => {
                            console.error(error);
                            bot.sendMessage(chatId, "حدث خطأ أثناء إرسال الصورة.");
                        });
                });
            });
        }).on('error', (error) => {
            console.error(error);
            bot.sendMessage(chatId, "حدث خطأ أثناء تحميل الصورة. تأكد من أن الرابط صحيح.");
        });
    } else {
        bot.sendMessage(chatId, "يرجى إرسال رابط صحيح من Pinterest.");
    }
});
