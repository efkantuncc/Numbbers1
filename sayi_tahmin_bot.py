import telebot
from telebot import types
import random  

# Telegram bot tokenını buraya girin
TOKEN = '7172697421:AAGbjLQ7-WVWz_xVg-d0sL3EWxfg4FSlZos'
bot = telebot.TeleBot(TOKEN)

# Oyun için gerekli değişkenler
minimum = 1
maximum = 100
secret_number = random.randint(minimum, maximum)
guesses = 0

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    # Fotoğrafı gönder
    photo_url = "https://i.hizliresim.com/633fzxo.png"
    bot.send_photo(message.chat.id, photo_url)
    
    # Buton oluştur
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🤠 Sahip", url="t.me/t3rickg"))
    
    # Başlangıç mesajını gönder
    bot.reply_to(message, "Merhaba! Benimle sayı tahmin oyununa başlamak için /s komutunu kullanabilirsin.", reply_markup=markup)

@bot.message_handler(commands=['s'])
def handle_guess(message):
    global guesses
    try:
        guesses += 1
        guess = int(message.text.split()[1])
        if guess < minimum or guess > maximum:
            bot.reply_to(message, "Lütfen {}. ve {}. arasında bir sayı giriniz.".format(minimum, maximum))
        elif guess < secret_number:
            bot.reply_to(message, "Daha büyük bir sayı girin.")
        elif guess > secret_number:
            bot.reply_to(message, "Daha küçük bir sayı girin.")
        else:
            bot.reply_to(message, "Tebrikler! Doğru tahmin ettiniz. {} denemede buldunuz.".format(guesses))
            # Oyunu sıfırla
            reset_game()
    except:
        bot.reply_to(message, "Lütfen geçerli bir sayı girin.")

def reset_game():
    global secret_number, guesses
    secret_number = random.randint(minimum, maximum)
    guesses = 0

if __name__ == "__main__":
    bot.polling()
