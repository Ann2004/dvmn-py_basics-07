import ptbot
import os
from dotenv import load_dotenv
import random
from pytimeparse import parse


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def notify_progress(secs_left, author_id, message_id, total, bot):   
    bot.update_message(
        author_id,
        message_id,
        f"Осталось {secs_left} секунд \n{render_progressbar(total, total - secs_left)}"
    )


def notify(author_id, bot):
    bot.send_message(author_id, "Время вышло")


def reply(chat_id, message, bot):
    message_id = bot.send_message(chat_id, "Запускаю таймер...")
    bot.create_countdown(
        parse(message), 
        notify_progress, 
        author_id=chat_id, 
        message_id=message_id, 
        total=parse(message),
        bot=bot
    )
    bot.create_timer(
        parse(message),
        notify,
        author_id=chat_id,
        bot=bot
    )


def main():
    load_dotenv()
    TG_TOKEN = os.getenv("TG_TOKEN")

    bot = ptbot.Bot(TG_TOKEN)
    bot.reply_on_message(reply, bot=bot)
    bot.run_bot()


if __name__ == "__main__":
    main()