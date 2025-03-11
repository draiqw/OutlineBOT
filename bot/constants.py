# constants.py

BUTTON_REGISTRATION = "🔥 Регистрация"
BUTTON_GET_KEY = "🚀 Получить ключ"
BUTTON_PROFILE = "👤 Профиль"
BUTTON_MY_KEYS = "🔑 Мои ключи"
BUTTON_MENU = "📋 Меню"
BUTTON_INFO = "📖 Информация"
BUTTON_GIVE_CONTACT = "📲 Поделиться контактом"
BUTTON_SUBSCRIBE = "💳 Подписка"

START_MESSAGE = (
    "<b>Привет!</b>\n\n"
    "Доступные команды:\n"
    "<b>/reg</b> - регистрация (в подарок неделя пробной подписки)\n"
    "<b>/get_key</b> - получить Outline ключ\n"
    "<b>/profile</b> - посмотреть профиль\n"
    "<b>/my_keys</b> - посмотреть свои ключи\n"
    "<b>/subscribe</b> - оплатить подписку (100 руб/мес, оплата условная)\n"
    "<b>/info</b> - информация и гайды\n\n"
    "Или воспользуйтесь кнопками в меню ниже."
)
GET_KEY_ALREADY_EXISTS = "🔑 <b> У вас уже есть ключ </b> (доступен только один ключ на пользователя):\n"

REG_ALREADY_REGISTERED = "⚠️ Пользователь уже зарегистрирован."
REG_PROMPT = (
    "Супер! Давай зарегистрируемся.\n"
    "Нажми кнопку, чтобы поделиться контактом.\n"
    "В подарок – <b>неделя пробной подписки</b>!"
)

CONTACT_INVALID = "⚠️ Пожалуйста, поделитесь своим контактом."
CONTACT_SUCCESS = (
    "🎉 Регистрация прошла успешно!\n"
    "В подарок вам неделя пробной подписки, действующая до: <b>{expiry}</b>.\n"
    "Для получения Outline ключа используйте \n <b>/get_key</b> или кнопку <b>{button_get_key}</b>."
)

GET_KEY_NOT_REGISTERED = "⚠️ Сначала зарегистрируйтесь командой <b>/reg</b> и поделитесь контактом."
GET_KEY_ALREADY_EXISTS = "🔑 <b> У вас уже есть ключ </b> (доступен только один ключ на пользователя):\n"

GET_KEY_PROMPT = "🚀 <b>Пожалуйста, введите имя для ключа:</b>"

KEY_SUCCESS = "🔑 Ваш Outline ключ:\n```\n{key}\n```"

PROFILE_NOT_REGISTERED = "⚠️ Вы не зарегистрированы. Используйте команду <b>/reg</b> для регистрации."
PROFILE_INFO = "👤 <b>Ваш профиль:</b>\n<b>ID:</b> {id}\n<b>Телефон:</b> {phone}\n<b>Подписка действует до:</b> {expiry}"

MY_KEYS_NONE = "⚠️ У вас ещё нет ключа. Используйте команду <b>/get_key</b> или кнопку <b>{button_get_key}</b>."

SUBSCRIBE_NOT_REGISTERED = "⚠️ Вы не зарегистрированы. Используйте <b>/reg</b> для регистрации."
SUBSCRIBE_SUCCESS = (
    "💳 <b>Пока оплата условная</b>, но подписка продлена на 30 дней!\n"
    "Подписка действует до: <b>{expiry}</b>."
)

INFO_DESCRIPTION = (
    "<b>Информация и гайды:</b>\n\n"
    "📖 <a href='https://example.com/guide'>Гайд по установке</a>\n"
    "❓ <a href='https://example.com/faq'>FAQ</a>\n"
    "💬 <a href='https://example.com/support'>Поддержка</a>"
)

MENU_MESSAGE = (
    "📋 <b>Меню:</b>\n"
    "/reg - регистрация\n"
    "/get_key - получить Outline ключ\n"
    "/profile - посмотреть профиль\n"
    "/my_keys - посмотреть свои ключи\n"
    "/subscribe - оплатить подписку\n"
    "/info - информация и гайды"
)

BOT_TOKEN = "7587969714:AAFJZDXig9ZcYUJ4GUDu-Lbqy0h43cvw9mI"
BASE_API_URL = "https://88.218.171.165:50406/j1JwWvOIScy1f9VjY_dgvg"
DATABASE = "users.db"
KEY_NAME = 1

SUBSCRIBE_END = "⚠️ Ваша подписка закончилась. Обновите её командой <b>/subscribe</b>."

