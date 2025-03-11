# handlers.py

import re
from datetime import datetime, timedelta
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler, CallbackContext
from database import get_user, add_user, update_user_key, update_subscription
from keys import create_outline_key
from constants import KEY_NAME, INFO_DESCRIPTION

def get_menu_keyboard(user_id=None):
    """
    Формирует постоянную клавиатуру для взаимодействия.
    Добавлены эмодзи и стилизация.
    """
    if user_id is not None and get_user(user_id):
        buttons = [
            ["👤 Посмотреть профиль", "🚀 Получить ключ"],
            ["🔑 Мои ключи", "📋 Меню"]
        ]
    else:
        buttons = [
            ["🔥 Регистрация", "🚀 Получить ключ", "📋 Меню"]
        ]
    return ReplyKeyboardMarkup(buttons, one_time_keyboard=False, resize_keyboard=True)

def format_date(date_str: str) -> str:
    """Форматирует дату из ISO в формат 'ДД.MM.ГГГГ ЧЧ:ММ'."""
    try:
        dt = datetime.fromisoformat(date_str)
        return dt.strftime("%d.%m.%Y %H:%M")
    except Exception:
        return date_str

def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    update.message.reply_text(
        "<b>Привет!</b>\n\n"
        "Доступные команды:\n"
        "<b>/reg</b> - регистрация (<i>в подарок неделя пробной подписки</i>)\n"
        "<b>/get_key</b> - получить Outline ключ\n"
        "<b>/profile</b> - посмотреть профиль\n"
        "<b>/my_keys</b> - посмотреть свои ключи\n"
        "<b>/subscribe</b> - оплатить подписку (100 руб/мес, оплата условная)\n"
        "<b>/info</b> - информация и гайды\n\n"
        "Или воспользуйтесь кнопками в меню ниже.",
        parse_mode="HTML",
        reply_markup=get_menu_keyboard(user_id)
    )

def reg(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if get_user(user_id):
        update.message.reply_text("⚠️ <b>Пользователь уже зарегистрирован.</b>", parse_mode="HTML", reply_markup=get_menu_keyboard(user_id))
        return
    keyboard = [[KeyboardButton("📲 Поделиться контактом", request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=False, resize_keyboard=True)
    update.message.reply_text(
        "Супер! Давай зарегистрируемся.\nНажми кнопку, чтобы поделиться контактом.\nВ подарок – <b>неделя пробной подписки</b>!",
        parse_mode="HTML",
        reply_markup=reply_markup
    )

def contact_handler(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    contact = update.message.contact
    if contact:
        if contact.user_id != user_id:
            update.message.reply_text("⚠️ Пожалуйста, поделитесь своим контактом.", reply_markup=get_menu_keyboard(user_id))
            return
        if get_user(user_id):
            update.message.reply_text("⚠️ <b>Пользователь уже зарегистрирован.</b>", parse_mode="HTML", reply_markup=get_menu_keyboard(user_id))
        else:
            add_user(user_id, contact.phone_number)
            trial_expiry = (datetime.now() + timedelta(days=7)).isoformat(timespec='seconds')
            formatted_expiry = format_date(trial_expiry)
            update.message.reply_text(
                "🎉 <b>Регистрация прошла успешно!</b>\nВ подарок вам неделя пробной подписки, действующая до: <b>" + formatted_expiry + "</b>.\n"
                "Для получения Outline ключа используйте <b>/get_key</b> или кнопку <b>🚀 Получить ключ</b>.",
                parse_mode="HTML",
                reply_markup=get_menu_keyboard(user_id)
            )

def get_key(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user = get_user(user_id)
    if not user:
        update.message.reply_text(
            "⚠️ Сначала зарегистрируйтесь командой <b>/reg</b> и поделитесь контактом.",
            parse_mode="HTML",
            reply_markup=get_menu_keyboard(user_id)
        )
        return ConversationHandler.END
    if user[2]:
        update.message.reply_text(
            f"🔑 <b>У вас уже есть ключ</b> (доступен только один ключ на пользователя):\n<code>{user[2]}</code>",
            parse_mode="HTML",
            reply_markup=get_menu_keyboard(user_id)
        )
        return ConversationHandler.END
    context.user_data["awaiting_key_name"] = True
    update.message.reply_text("🚀 <b>Пожалуйста, введите имя для ключа:</b>", parse_mode="HTML", reply_markup=ReplyKeyboardRemove())
    return KEY_NAME

def key_name_handler(update: Update, context: CallbackContext):
    context.user_data["awaiting_key_name"] = False
    user_id = update.effective_user.id
    key_name = update.message.text.strip()
    if key_name.lower() in ["регистрация", "получить ключ", "меню", "посмотреть профиль", "посмотреть свои ключи"]:
        update.message.reply_text("⚠️ <b>Пожалуйста, введите корректное имя для ключа:</b>", parse_mode="HTML", reply_markup=ReplyKeyboardRemove())
        context.user_data["awaiting_key_name"] = True
        return KEY_NAME
    # Имитируем задержку (typing)
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    key = create_outline_key(key_name)
    update_user_key(user_id, key)
    update.message.reply_text(
        f"🔑 <b>Ваш Outline ключ:</b>\n<code>{key}</code>",
        parse_mode="HTML",
        reply_markup=get_menu_keyboard(user_id)
    )
    return ConversationHandler.END

def profile(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user = get_user(user_id)
    if not user:
        update.message.reply_text("⚠️ Вы не зарегистрированы. Используйте команду <b>/reg</b> для регистрации.", parse_mode="HTML")
    else:
        formatted_expiry = format_date(user[3]) if user[3] else "не установлено"
        update.message.reply_text(
            f"👤 <b>Ваш профиль:</b>\n<b>ID:</b> {user[0]}\n<b>Телефон:</b> {user[1]}\n<b>Подписка действует до:</b> {formatted_expiry}",
            parse_mode="HTML",
            reply_markup=get_menu_keyboard(user_id)
        )

def my_keys(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user = get_user(user_id)
    if not user:
        update.message.reply_text("⚠️ Вы не зарегистрированы. Используйте команду <b>/reg</b> для регистрации.", parse_mode="HTML", reply_markup=get_menu_keyboard(user_id))
    elif user[2]:
        update.message.reply_text(
            f"🔑 <b>Ваш Outline ключ:</b>\n<code>{user[2]}</code>",
            parse_mode="HTML",
            reply_markup=get_menu_keyboard(user_id)
        )
    else:
        update.message.reply_text("⚠️ У вас ещё нет ключа. Используйте команду <b>/get_key</b> или кнопку <b>🚀 Получить ключ</b>.", parse_mode="HTML", reply_markup=get_menu_keyboard(user_id))

def subscribe(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user = get_user(user_id)
    if not user:
        update.message.reply_text("⚠️ Вы не зарегистрированы. Используйте <b>/reg</b> для регистрации.", parse_mode="HTML", reply_markup=get_menu_keyboard(user_id))
        return
    new_expiry = (datetime.now() + timedelta(days=30)).isoformat(timespec='seconds')
    update_subscription(user_id, new_expiry)
    formatted_expiry = format_date(new_expiry)
    update.message.reply_text(
        "💳 <b>Пока оплата условная</b>, но подписка продлена на 30 дней!\nПодписка действует до: <b>" + formatted_expiry + "</b>.",
        parse_mode="HTML",
        reply_markup=get_menu_keyboard(user_id)
    )

def info(update: Update, context: CallbackContext):
    update.message.reply_text(INFO_DESCRIPTION, parse_mode="HTML", disable_web_page_preview=True, reply_markup=ReplyKeyboardRemove())

def show_menu(update: Update, context: CallbackContext):
    menu_text = (
        "📋 <b>Меню:</b>\n"
        "/reg - регистрация\n"
        "/get_key - получить Outline ключ\n"
        "/profile - посмотреть профиль\n"
        "/my_keys - посмотреть свои ключи\n"
        "/subscribe - оплатить подписку\n"
        "/info - информация и гайды"
    )
    update.message.reply_text(menu_text, parse_mode="HTML", reply_markup=ReplyKeyboardRemove())

def global_text_handler(update: Update, context: CallbackContext):
    # Если бот ожидает ввода имени ключа, не обрабатываем сообщение
    if context.user_data.get("awaiting_key_name"):
        return
    show_menu(update, context)
