# main.py

import os
import re
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from constants import (
    BOT_TOKEN, 
    BUTTON_GET_KEY, 
    BUTTON_MENU, 
    BUTTON_MY_KEYS, 
    BUTTON_PROFILE, 
    KEY_NAME, 
    DATABASE, 
    BUTTON_REGISTRATION,
    BUTTON_INFO
)
from database import init_db
from handlers import (
    start, 
    reg, 
    contact_handler, 
    get_key, 
    key_name_handler, 
    profile, 
    my_keys, 
    show_menu,
    show_info
)

def main():
    # При полном новом запуске удаляем базу данных, если она существует
    if os.path.exists(DATABASE):
        os.remove(DATABASE)
    init_db()
    
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Добавляем обработчики команд
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("reg", reg))
    dp.add_handler(CommandHandler("get_key", get_key))
    dp.add_handler(CommandHandler("profile", profile))
    dp.add_handler(CommandHandler("my_keys", my_keys))
    dp.add_handler(CommandHandler("menu", show_menu))
    dp.add_handler(CommandHandler("info", show_info))
    # Обработка контакта
    dp.add_handler(MessageHandler(Filters.contact, contact_handler))
    
    # Обработка нажатий кнопок через текстовые сообщения
    dp.add_handler(MessageHandler(Filters.regex(re.compile(BUTTON_REGISTRATION, re.IGNORECASE)), reg))
    dp.add_handler(MessageHandler(Filters.regex(re.compile(BUTTON_PROFILE, re.IGNORECASE)), profile))
    dp.add_handler(MessageHandler(Filters.regex(re.compile(BUTTON_MY_KEYS, re.IGNORECASE)), my_keys))
    dp.add_handler(MessageHandler(Filters.regex(re.compile(BUTTON_MENU, re.IGNORECASE)), show_menu))
    dp.add_handler(MessageHandler(Filters.regex(re.compile(BUTTON_INFO, re.IGNORECASE)), show_info))
    
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("get_key", get_key),
            MessageHandler(Filters.regex(re.compile(BUTTON_GET_KEY, re.IGNORECASE)), get_key)
        ],
        states={
            KEY_NAME: [MessageHandler(Filters.text & ~Filters.command, key_name_handler)]
        },
        fallbacks=[]
    )
    dp.add_handler(conv_handler)
    
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, show_menu))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
