import random
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Telegram bot token
TOKEN = '7075891544:AAH19Mp2D-Nkofq4ifwoChnm1T69b0JyrPs'

# Başlangıç komutu
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sayı tahmin oyununa hoş geldiniz! Bir sayı tahmin edin.")

# Sayı tahmin oyunu
def guess_number(update, context):
    user_number = int(update.message.text)
    bot_number = random.randint(1, 100)
    
    if user_number == bot_number:
        message = "Tebrikler! Doğru tahmin ettiniz."
    elif user_number < bot_number:
        message = "Daha büyük bir sayı girin."
    else:
        message = "Daha küçük bir sayı girin."
    
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

# Yardım komutu
def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Bu bot bir sayı tahmin oyunu sunar. Oyunu başlatmak için /start komutunu kullanın.")

# Tanımlayıcı ve özel mesaj işleyicilerini ayarlama
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, guess_number))
    dp.add_handler(CommandHandler("help", help))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
