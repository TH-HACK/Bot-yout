//𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳
//• لا تنسى ذكر حقوق المطور توم
//• المطور ↦ @T_0_M0 ↤
//• قناة المطور ↦ @izeoe ↤
//𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳
<?php
ob_start();
error_reporting(0);
define("API_KEY", '7901940137:AAGQfDnI_P-LN5U_BtJGCPmAaZNXJp80jdM');
function bot($method, $datas = []) {
    $url = "https://api.telegram.org/bot" . API_KEY . "/$method";
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $datas);
    $res = curl_exec($ch);
    if (curl_error($ch)) {
        var_dump(curl_error($ch));
    }
    return json_decode($res);
}
// 𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳


// هنا تكدر تضيف لوحة ادمن اذا تحب


// 𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳
$input = file_get_contents("php://input");
$update = json_decode($input, TRUE);
$chatId = $update['message']['chat']['id'];
$text = $update['message']['text'];

if ($text == '/start') {
bot('sendMessage', [
'chat_id' => $chatId,
'text' => '*• اهلا بك عزيزي في بوت الذكاء الاصطناعي
• أنا GPT AI ، تم تدريبه باستخدام تقنية الذكاء الاصطناعي 
• لتوفير الإجابات والمحادثات للمستخدمين 
• في مختلف المواضيع والمجالات

• اكدر اساعدك بشيء ؟ *',
'parse_mode' => "Markdown",
'disable_web_page_preview' => true,
'reply_markup' => json_encode([
'inline_keyboard' => [
[['text' => "• مطور البوت •", 'url' => "https://t.me/T_0_M0"],
['text' => "• قناة البوت •", 'url' => "https://t.me/izeoe"]]
]
])
]);
return;
}
//𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳
//• لا تنسى ذكر حقوق المطور توم
//• المطور ↦ @T_0_M0 ↤
//• قناة المطور ↦ @izeoe ↤
//𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳
sendApiResponse($chatId, $text);
function sendApiResponse($chatId, $message) {
    $apiUrl = "https://advancewithaiapi.cropk.com/Gpt/generate"; 
    $payload = json_encode(["prompt" => $message, "contentType" => "gptAlternative"]);
    
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $apiUrl);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Content-Type: application/json'
    ]);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);
    
    $apiResponse = curl_exec($ch);
    curl_close($ch);
    $result = json_decode($apiResponse, true);
    $generatedText = isset($result['generatedText']) ? $result['generatedText'] : 'لم أتمكن من الحصول على رد.';
$waitingMessage =bot('SendMessage', [
'chat_id' => $chatId,
'text' => "انتظر من فضلك ⏱️",
]);
//• لا تنسى ذكر حقوق المطور توم
//• المطور ↦ @T_0_M0 ↤
//• قناة المطور ↦ @izeoe ↤
$message_id = $waitingMessage->result->message_id;
bot('editMessageText', [
'chat_id' => $chatId,
'message_id' => $message_id,
'text' => $generatedText,
'parse_mode' => "markdown"
]);
}
?>
//𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳
//• لا تنسى ذكر حقوق المطور توم
//• المطور ↦ @T_0_M0 ↤
//• قناة المطور ↦ @izeoe ↤
//𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳𓏳
