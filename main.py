from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CallbackContext, CommandHandler
import random

generator_words = ""
num_of_fails = 7
game_start = False
guessed = ""

random.seed(version=2)

def get_random_word():
    random_words = ["Геолог", "Бальзам", "Бревно", "Жердь", "Борец", "Самовар", "Карабин", "Подлокотник", "Барак", "Мотор"]
    random_number = random.randint(1, 10)
    for i, j in enumerate(random_words):
        random_words[i] = j.upper()
    return list(random_words[random_number - 1])

def change_word(letter):
    global guessed
    global generator_words
    for i, j in enumerate(generator_words):
        if j == letter:
            guessed[i] = j

def start(update, context):
    global game_start
    global generator_words
    global guessed
    global num_of_fails
    generator_words = get_random_word()
    guessed = len(generator_words) * ["_"]
    num_of_fails = 7
    game_start = True
    update.message.reply_text("Игра началась!\n Загаданное слово:" + "".join(guessed))


def restart(update, context):
    global game_start
    global generator_words
    global guessed
    global num_of_fails
    generator_words = get_random_word()
    guessed = len(generator_words) * ["_"]
    num_of_fails = 7
    update.message.reply_text("Новая игра началась!\n Загаданное слово:" + "".join(guessed))


def echo(update, context):
    global game_start
    global generator_words
    global guessed
    global num_of_fails
    if game_start:
        command = update.message.text
        if command == "/restart":
            generator_words = get_random_word()
            guessed = len(generator_words) * ["_"]
            num_of_fails = 7
            update.message.reply_text("Новая игра началась!\n Загаданное слово:" + "".join(guessed) + "\nКоличество букв в слове:" + str(len(generator_words)))
        else:
            letter = command[0].upper()
            if letter != '_':
                if letter in guessed:
                    update.message.reply_text("Данная буква уже отгадана, попробуйте другую")
                else:
                    if letter in generator_words:
                        change_word(letter)
                        update.message.reply_text("Вы угадали букву!\n Загаданное слово:"+"".join(guessed))
                        if generator_words == guessed:
                            update.message.reply_text("Вы выиграли!")
                            game_start = False
                    else:
                        num_of_fails -= 1
                        out = "Отгаданное слово:" + "".join(guessed) + "\n" + "Количество попыток:" + str(num_of_fails)
                        if num_of_fails == 0:
                            out += "\nВы проиграли."
                            game_start = False
                        update.message.reply_text("Данной буквы нет в загаданном слове\n" + out)
            else:
                update.message.reply_text("Это не буква.")
    else:
        command = update.message.text
        if command != "/start":
            update.message.reply_text("Хотите сыграть? Дла запуска игры напишите команду /start")
        else:
            generator_words = get_random_word()
            guessed = len(generator_words) * ["_"]
            num_of_fails = 7
            game_start = True
            update.message.reply_text("Игра началась!\n Загаданное слово:" + "".join(guessed) + "\nКоличество букв в слове:" + str(len(generator_words)))


def main():
    updater = Updater("5243519049:AAEWBMDT8nE2qy2vZYVy3eXDZ_Pc2UyKwGU", use_context = True)
    dp = updater.dispatcher
    text_handler = MessageHandler(Filters.text, echo)

    dp.add_handler(text_handler)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("restart", restart))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()