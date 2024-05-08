import telebot
from telebot import types
import time

# Bot tokenini buraya yapıştır
TOKEN = '6994880373:AAGDldLjJObYDOsis9iDVuv5BwOKCJZ39hw'
bot = telebot.TeleBot(TOKEN)

# Spam kontrolü için bir sözlük
spam_control = {}

# Güvenlik kodları
def ban_user(chat_id, user_id):
    bot.kick_chat_member(chat_id, user_id)

def kick_user(chat_id, user_id):
    bot.kick_chat_member(chat_id, user_id)
    bot.unban_chat_member(chat_id, user_id)

# Merhaba mesajı ve ana menü
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, """Merhaba Ben Eko Mod,
    Sunucuların güvenliğini sağlamak amacıyla üretildim.""")
    main_menu(message)

# Ana menüyü gönderen fonksiyon
def main_menu(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
    itembtn1 = telebot.types.KeyboardButton('➕ Grup/Kanal\'a Ekle')
    itembtn2 = telebot.types.KeyboardButton('📙 Komutlar')
    itembtn3 = telebot.types.KeyboardButton('⚜️ Sahip')
    markup.add(itembtn1, itembtn2, itembtn3)
    bot.send_message(message.chat.id, "Menü", reply_markup=markup)

# Grup/Kanal ekleme butonuna basıldığında
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text == '➕ Grup/Kanal\'a Ekle':
        bot.send_message(message.chat.id, "Botu hangi gruba veya kanala eklemek istiyorsunuz? Lütfen linkini paylaşın.")
        bot.register_next_step_handler(message, add_to_group)
        
    elif message.text == '📙 Komutlar':
        bot.send_message(message.chat.id, """Botun Komutları:
        /ban - Bir kullanıcıyı yasaklar
        /kick - Bir kullanıcıyı atar
        /help - Yardım menüsünü gösterir""")

    elif message.text == '⚜️ Sahip':
        bot.send_message(message.chat.id, "Sahip", reply_markup=telebot.types.ReplyKeyboardRemove())

# Spam kontrolü
@bot.message_handler(func=lambda message: True)
def spam_control(message):
    user_id = message.from_user.id
    if user_id not in spam_control:
        spam_control[user_id] = {'message_count': 1, 'last_message_time': time.time()}
    else:
        current_time = time.time()
        time_difference = current_time - spam_control[user_id]['last_message_time']
        if time_difference < 10:  # Örnek olarak 10 saniye içinde 3'ten fazla mesaj atarsa
            spam_control[user_id]['message_count'] += 1
            if spam_control[user_id]['message_count'] > 3:
                # Spam yapan kullanıcıyı sustur ve uyarı mesajını gönder
                bot.restrict_chat_member(message.chat.id, user_id, until_date=time.time() + 180)  # 3 dakika susturma
                bot.reply_to(message, "Spam yapmayı kes! Son uyarı!")
        else:
            spam_control[user_id] = {'message_count': 1, 'last_message_time': current_time}

# Botu istenilen gruba veya kanala ekleyen fonksiyon
def add_to_group(message):
    try:
        chat_link = message.text
        chat_id = chat_link.split('/')[-1]  # Grup veya kanal ID'sini al
        bot.send_message(chat_id, "Bot bu gruba veya kanala eklendi.")
    except Exception as e:
        bot.send_message(message.chat.id, "Bir hata oluştu. Lütfen tekrar deneyin.")

# Güvenlik mesajını belirli aralıklarla gönderen fonksiyon
def send_security_message():
    while True:
        # Botun bulunduğu tüm grup ve kanallara mesaj gönder
        for chat in bot.get_chat_member(message.chat.id, user_id).chat_ids:
            bot.send_message(chat.id, "Bu sunucunun güvenliği Eko Mod ile sağlanmaktadır.",
                             reply_markup=generate_owner_button())
        time.sleep(3600)  # 1 saatte bir mesaj gönder

# Sahip butonu için özel buton oluşturan fonksiyon
def generate_owner_button():
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text="⚜️ Sahip", url="https://t.me/t3rickg"))
    return markup

# Güvenlik mesajlarını gönderen fonksiyonu başlat
send_security_message()

bot.polling()
