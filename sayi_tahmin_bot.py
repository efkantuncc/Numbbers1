import telebot
import random

# Telegram bot tokenını buraya girin
TOKEN = '7075891544:AAEvxq61Tu97HGoOZkzoZtJztmXlzivqPw4'
bot = telebot.TeleBot(TOKEN)

# Oyun için gerekli değişkenler
minimum = 1
maximum = 100
secret_number = random.randint(minimum, maximum)
guesses = 0

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Merhaba! Benimle sayı tahmin oyununa başlamak için /guess komutunu kullanabilirsin.")

@bot.message_handler(commands=['guess'])
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
