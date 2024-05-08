import telebot
from pytube import YouTube
from tiktokapi import TikTokApi
import instaloader

# Telegram botunuzun token'ını buraya ekleyin
TOKEN = '7005558840:AAFFQZ0V5rkSYbuqoG4adafJAS0liUrKnw0'

bot = telebot.TeleBot(TOKEN)
tiktok_api = TikTokApi()
insta_loader = instaloader.Instaloader()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "💫 Merhaba! Ben Eko Download, Instagram, YouTube, TikTok platformlarından video indirme yardımcı olmak için üretildim.\nAşağıdaki butonları kullanarak istediğiniz platformdan video indirebilirsiniz.")

    # Butonları oluştur
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    tiktok_button = types.KeyboardButton("📙 TikTok")
    instagram_button = types.KeyboardButton("📗 Instagram")
    youtube_button = types.KeyboardButton("📕 YouTube")
    owner_button = types.KeyboardButton("⚜️ Sahip")
    keyboard.add(tiktok_button, instagram_button, youtube_button, owner_button)

    bot.send_message(message.chat.id, "Hangi platformdan video indirmek istersiniz?", reply_markup=keyboard)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "📙 TikTok":
        bot.reply_to(message, "TikTok platformundan video indirmek için lütfen TikTok video linkini gönderin.")
    elif message.text == "📗 Instagram":
        bot.reply_to(message, "Instagram platformundan video indirmek için lütfen Instagram video linkini gönderin.")
    elif message.text == "📕 YouTube":
        bot.reply_to(message, "YouTube platformundan video indirmek için lütfen YouTube video linkini gönderin.")
    elif message.text == "⚜️ Sahip":
        bot.send_message(message.chat.id, "Botun sahibi: @t3rickg")

@bot.message_handler(content_types=['text'])
def download_video(message):
    try:
        if message.text.startswith("https://www.tiktok.com/") or message.text.startswith("https://vm.tiktok.com/"):
            video_id = message.text.split('/')[-1]
            tiktok_video = tiktok_api.get_video_by_id(video_id)
            with open(f"{video_id}.mp4", "wb") as out:
                out.write(tiktok_video)
            bot.reply_to(message, "TikTok video başarıyla indirildi!")
        elif "instagram.com" in message.text:
            insta_loader.download_post(message.text, target='.')
            bot.reply_to(message, "Instagram video başarıyla indirildi!")
        elif "youtube.com" in message.text:
            yt = YouTube(message.text)
            stream = yt.streams.get_highest_resolution()
            stream.download()
            bot.reply_to(message, "YouTube video başarıyla indirildi!")
        else:
            bot.reply_to(message, "Geçersiz link. Lütfen desteklenen bir platformdan video linki gönderin.")
    except Exception as e:
        bot.reply_to(message, "Video indirilirken bir hata oluştu: " + str(e))

bot.polling()
