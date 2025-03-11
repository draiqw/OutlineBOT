# handlers.py
import re
from datetime import datetime, timedelta
import re
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, CallbackContext
from keys import create_outline_key

from database import (
    get_user, 
    add_user, 
    update_user_key,
    update_subscription
)

from constants import (
    BUTTON_GET_KEY, 
    BUTTON_GIVE_CONTACT, 
    BUTTON_INFO, 
    BUTTON_MENU, 
    BUTTON_MY_KEYS, 
    BUTTON_PROFILE, 
    BUTTON_REGISTRATION, 
    CONTACT_INVALID, 
    CONTACT_SUCCESS, 
    GET_KEY_ALREADY_EXISTS, 
    GET_KEY_PROMPT,
    INFO_DESCRIPTION, 
    KEY_NAME, 
    KEY_SUCCESS, 
    MENU_MESSAGE,
    MY_KEYS_NONE, 
    PROFILE_INFO, 
    PROFILE_NOT_REGISTERED, 
    REG_ALREADY_REGISTERED, 
    REG_PROMPT, 
    START_MESSAGE,
    SUBSCRIBE_NOT_REGISTERED,
    SUBSCRIBE_SUCCESS
)


def format_date(date_str: str) -> str:
    try:
        dt = datetime.fromisoformat(date_str)
        return dt.strftime("%d.%m.%Y %H:%M")
    except Exception:
        return date_str


def get_menu_keyboard(buttons=[]):
    return ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True)


def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    update.message.reply_text(
        START_MESSAGE,
        parse_mode="HTML",
        reply_markup=get_menu_keyboard(
            [
                [BUTTON_REGISTRATION, BUTTON_MENU, BUTTON_INFO]
            ] 
        )
    )


def reg(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if get_user(user_id):
        update.message.reply_text(
            REG_ALREADY_REGISTERED, 
            reply_markup=get_menu_keyboard(
                [
                    [BUTTON_PROFILE, BUTTON_MENU, BUTTON_MY_KEYS]
                ]
            )
        )
        return
    
    reply_markup = get_menu_keyboard(
        [
            [KeyboardButton(
                BUTTON_GIVE_CONTACT, 
                request_contact=True
            )]
        ]
    )
    update.message.reply_text(
        REG_PROMPT,
        parse_mode="HTML",
        reply_markup=reply_markup
    )


def contact_handler(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    contact = update.message.contact
    if contact:
        if contact.user_id != user_id:
            update.message.reply_text(
                CONTACT_INVALID, 
                reply_markup = get_menu_keyboard(
                    [
                        [KeyboardButton(
                            BUTTON_GIVE_CONTACT, 
                            request_contact=True
                        )]
                    ]
                )
            )
            return
        if get_user(user_id):
            update.message.reply_text(
                REG_ALREADY_REGISTERED, 
                reply_markup=get_menu_keyboard(
                    [
                        [BUTTON_PROFILE, BUTTON_MENU, BUTTON_MY_KEYS]
                    ] 
                )
            )
        else:
            trial_expiry = (datetime.now() + timedelta(days=7)).isoformat(timespec='seconds')
            formatted_expiry = format_date(trial_expiry)

            add_user(user_id, contact.phone_number, trial_expiry)

            update.message.reply_text(
                CONTACT_SUCCESS.format(
                    expiry=formatted_expiry, 
                    button_get_key=BUTTON_GET_KEY
                ),
                parse_mode="HTML",
                reply_markup=get_menu_keyboard(
                    [
                        [BUTTON_PROFILE, BUTTON_MENU, BUTTON_GET_KEY]
                    ]
                )
            )


def get_key(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user = get_user(user_id)

    if not user:
        update.message.reply_text(
            PROFILE_NOT_REGISTERED,
            parse_mode="HTML",
            reply_markup=get_menu_keyboard(
                [
                    [BUTTON_REGISTRATION, BUTTON_MENU]
                ]
            )
        )
        return ConversationHandler.END
    
    if user[2]:
        update.message.reply_text(
            GET_KEY_ALREADY_EXISTS,
            parse_mode="HTML",
            reply_markup=get_menu_keyboard(
                [
                    [BUTTON_PROFILE, BUTTON_MENU, BUTTON_MY_KEYS]
                ]
            )
        )
        return ConversationHandler.END
    
    update.message.reply_text(
        GET_KEY_PROMPT, 
        parse_mode="HTML"
    )
    
    return KEY_NAME


def key_name_handler(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    key_name = update.message.text.strip()

    key = create_outline_key(key_name)

    update_user_key(user_id, key)

    update.message.reply_text(
        KEY_SUCCESS.format(key=key),
        parse_mode="Markdown",
        reply_markup=get_menu_keyboard(
            [
                [BUTTON_PROFILE, BUTTON_MENU, BUTTON_INFO]
            ]
        )
    )
    return ConversationHandler.END


def profile(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user = get_user(user_id)
    if not user:
        update.message.reply_text(
            PROFILE_NOT_REGISTERED,
            parse_mode="HTML",
            reply_markup=get_menu_keyboard(
                [
                    [BUTTON_REGISTRATION]
                ]
            )
        )
    else:
        update.message.reply_text(
            PROFILE_INFO.format(
                id = user_id,
                phone = user[1],
                expiry = format_date(user[3])
            ),
            parse_mode="HTML",
            reply_markup=get_menu_keyboard(
                [
                    [BUTTON_MY_KEYS, BUTTON_MENU, BUTTON_INFO ]
                ]
            )
        )


def my_keys(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user = get_user(user_id)

    if not user:
        update.message.reply_text(
            PROFILE_NOT_REGISTERED, 
            parse_mode="HTML",
            reply_markup=get_menu_keyboard(
                [
                    [BUTTON_REGISTRATION],
                    [BUTTON_MENU, BUTTON_INFO]
                ]
            )
        )
    elif user[2]:
        update.message.reply_text(
            KEY_SUCCESS.format(key=user[2]),
            parse_mode="Markdown",
            reply_markup=get_menu_keyboard(
                [
                    [BUTTON_PROFILE, BUTTON_MENU, BUTTON_INFO]
                ]
            )
        )
    else:
        update.message.reply_text(
            MY_KEYS_NONE.format(button_get_key=BUTTON_GET_KEY), 
            parse_mode="HTML",
            reply_markup=get_menu_keyboard(
                [
                    [BUTTON_GET_KEY],
                    [BUTTON_PROFILE, BUTTON_MENU, BUTTON_INFO]
                ]
            )
        )


def show_menu(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    update.message.reply_text(
        MENU_MESSAGE,
        parse_mode="HTML",
        reply_markup=get_menu_keyboard(
            [
                [BUTTON_PROFILE, BUTTON_MENU, BUTTON_INFO],
                [BUTTON_GET_KEY, BUTTON_MY_KEYS, BUTTON_REGISTRATION]
            ]
        )
    )


def show_info(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    update.message.reply_text(
        INFO_DESCRIPTION,
        parse_mode="HTML",
        reply_markup=get_menu_keyboard(
            [
                [BUTTON_PROFILE, BUTTON_MENU, BUTTON_INFO]
            ]
        )
    )


def subscribe(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user = get_user(user_id)

    if not user:
        update.message.reply_text(
            PROFILE_NOT_REGISTERED, 
            parse_mode="HTML", 
            reply_markup=get_menu_keyboard(
                [
                    [BUTTON_REGISTRATION],
                    [BUTTON_MENU, BUTTON_INFO]
                ]
            )
        )
        return
    
    new_expiry = (datetime.now() + timedelta(days=30)).isoformat(timespec='seconds')
    update_subscription(user_id, new_expiry)
    formatted_expiry = format_date(new_expiry)
    update.message.reply_text(
        SUBSCRIBE_SUCCESS.format(expiry=formatted_expiry),
        parse_mode="HTML",
        reply_markup=get_menu_keyboard(
            [
                [BUTTON_PROFILE, BUTTON_MENU, BUTTON_INFO]
            ]
        )
    )