import os
import glob
from telegram.ext import Updater, CommandHandler


FILES_FOLDER = "files"


def get_available_files():
    files = glob.glob(os.path.join(FILES_FOLDER, "*"))
    clean = []
    for f in files:
        base = os.path.basename(f)
        clean.append(os.path.splitext(base)[0])
    return clean


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="Привет! Используй /d <страна> или /list")


def list_command(bot, update):
    available = get_available_files()

    if not available:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Нет доступных диапазонов.")
        return

    msg = "Вот доступные диапазоны:\n"
    for i, name in enumerate(available, start=1):
        msg += f"{i}. {name}\n"

    bot.send_message(chat_id=update.message.chat_id, text=msg)


def d_command(bot, update, args):
    if len(args) == 0:
        bot.send_message(chat_id=update.message.chat_id,
                         text="Используйте команду так: /d CountryName")
        return

    country = args[0]

    patterns = [
        f"{country}.*",
        f"{country.lower()}.*",
        f"{country.upper()}.*",
        f"{country.capitalize()}.*"
    ]

    found = []
    for p in patterns:
        found = glob.glob(os.path.join(FILES_FOLDER, p))
        if found:
            break

    if not found:
        bot.send_message(chat_id=update.message.chat_id,
                         text=f'Файл для "{country}" не найден.')
        return

    file_path = found[0]

    with open(file_path, "rb") as f:
        bot.send_document(chat_id=update.message.chat_id,
                          document=f,
                          filename=os.path.basename(file_path),
                          caption=f'Вот ваши диапазоны "{country}", с любовью от @devstocker ❤️')


def main():
    TOKEN = "8578117375:AAFuWpSGLqYctjEt53mS7OFZMxtwkwkHED0"

    # В старых версиях требуется update_queue
    updater = Updater(token=TOKEN, update_queue=None)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("list", list_command))
    dp.add_handler(CommandHandler("d", d_command, pass_args=True))

    print("Бот запущен!")
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()