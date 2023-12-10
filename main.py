import telebot
from telebot import types
from datetime import datetime

bot = telebot.TeleBot("TOKEN")

@bot.message_handler(commands=["start", "help"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Добавить заметку"))
    markup.add(types.KeyboardButton("Мои заметки"))

    if message.text.lower() == "/help":
        bot.send_message(message.chat.id, "Доступные команды:\n/start - начать работу с ботом\n/help - список команд")
    else:
        bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text.lower() == "добавить заметку")
def add_note_start(message):
    msg = bot.send_message(message.chat.id, "Введите вашу заметку:")
    bot.register_next_step_handler(msg, add_note_process)

def add_note_process(message):
    user_id = message.chat.id
    note = message.text
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        with open(f"{user_id}_diary.txt", "a", encoding="utf-8") as file:
            file.write(f"{date}: {note}\n")
        bot.send_message(user_id, "Заметка успешно добавлена!")

        # Возвращаем пользователя к начальной клавиатуре
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("Добавить заметку"))
        markup.add(types.KeyboardButton("Мои заметки"))
        bot.send_message(user_id, "Выберите действие", reply_markup=markup)

    except Exception as e:
        bot.send_message(user_id, f"Произошла ошибка: {str(e)}")

@bot.message_handler(func=lambda message: message.text.lower() == "мои заметки")
def view_notes(message):
    user_id = message.chat.id

    try:
        with open(f"{user_id}_diary.txt", "r", encoding="utf-8") as file:
            notes = file.read()

        if notes:
            bot.send_message(user_id, f"Ваши заметки:\n{notes}")
        else:
            bot.send_message(user_id, "У вас пока нет заметок.")

    except Exception as e:
        bot.send_message(user_id, f"Произошла ошибка: {str(e)}")

if __name__ == "__main__":
    bot.polling(none_stop=True)
