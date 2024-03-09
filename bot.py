#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

import logging
import os
import enum
from typing import Any, Dict, Tuple
from bot_paths.paths import BOT_TOKEN
import json

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from spreadsheets.spreadsheet import QueriesGoogleSheets



class UserDataKeys(enum.Enum):
    last_bots_message_id = "last_bots_message_id"
    username = "username"
    full_name = "full_name"
    gender = "gender"
    phone_number = "phone_number"
    email = "email"
    last_message_text = "last_message_text"


class CallBackData(enum.Enum):
    main_menu = "main_menu"
    main_menu_save = "main_menu_save"
    about = "about"
    full_name = "full_name"
    man = "man"
    wooman = "wooman"
    gender = "gender"
    phone_number = "phone_number"
    email = "email"

MAIN_MENU, FULL_NAME, GENDER, PHONE_NUMBER, EMAIL, CONV_END, ABOUT = range(7)


async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = "Здравствуйте, этот бот поможет оставить вам заявку на получение НИФ Португалии!"
    buttons = [[
        InlineKeyboardButton(text="Ввести или обновмить данные о себе", callback_data=CallBackData.full_name.value),
        InlineKeyboardButton(text="О нас", callback_data=CallBackData.about.value)
        ]]
    
    if update.callback_query:
        if update.callback_query.data == CallBackData.main_menu_save.value:
            QueriesGoogleSheets().write_data([
            context.user_data[UserDataKeys.username],
            context.user_data[UserDataKeys.full_name],
            context.user_data[UserDataKeys.gender],
            context.user_data[UserDataKeys.phone_number],
            context.user_data[UserDataKeys.email]
        ])
            
        await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(buttons))    
    
    else:
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
        last_message_id = context.user_data.get(UserDataKeys.last_bots_message_id)
        
        if last_message_id:    
            if context.user_data[UserDataKeys.last_message_text] != text:
                await context.bot.edit_message_text(
                    chat_id=update.effective_chat.id,
                    message_id=last_message_id,
                    text=text,
                    reply_markup=InlineKeyboardMarkup(buttons)
                )

        else:
            message = await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(buttons))
            context.user_data[UserDataKeys.last_bots_message_id] = message.message_id
            context.user_data[UserDataKeys.username] = update.message.from_user.username

    context.user_data[UserDataKeys.last_message_text] = text
    return MAIN_MENU


async def enter_client_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [[
        InlineKeyboardButton(text="назад", callback_data=CallBackData.main_menu.value)
    ]]
    text = "Введите полное ФИО"
    await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(buttons))

    context.user_data[UserDataKeys.last_message_text] = text
    return FULL_NAME


async def enter_client_gender(update: Update, context: ContextTypes.DEFAULT_TYPE):
    inline_buttons = [[
        InlineKeyboardButton(text="назад", callback_data=CallBackData.full_name.value),
        InlineKeyboardButton(text="Муж.", callback_data=CallBackData.man.value),
        InlineKeyboardButton(text="Жен.", callback_data=CallBackData.wooman.value),
    ]]
    text = "Выберете ваш пол"
    if update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(inline_buttons))
    
    else:
        users_message_id = update.message.message_id
        context.user_data[UserDataKeys.full_name] = update.message.text
        
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=users_message_id)
        if context.user_data[UserDataKeys.last_message_text] != text:
            await context.bot.edit_message_text(
                chat_id=update.effective_chat.id,
                message_id=context.user_data[UserDataKeys.last_bots_message_id],
                text=text,
                reply_markup=InlineKeyboardMarkup(inline_buttons)
            )
    
    context.user_data[UserDataKeys.last_message_text] = text
    return GENDER


async def enter_client_phone_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    inline_buttons = [[
        InlineKeyboardButton(text="назад", callback_data=CallBackData.gender.value)
    ]]
    
    text = "Введите контактный номер телефона"
    if update.callback_query:
        if update.callback_query.data != "назад":
            context.user_data[UserDataKeys.gender] = update.callback_query.data
        await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(inline_buttons))
    else:
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
    context.user_data[UserDataKeys.last_message_text] = text
    return PHONE_NUMBER


async def enter_client_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    inline_buttons = [[
        InlineKeyboardButton(text="назад", callback_data=CallBackData.phone_number.value)
    ]]
    text = "Введите контактный email"
    if update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(inline_buttons))
    
    else:
        if context.user_data[UserDataKeys.last_message_text] != text:
            context.user_data[UserDataKeys.phone_number] = update.message.text
            await context.bot.edit_message_text(
                chat_id=update.effective_chat.id, 
                message_id=context.user_data[UserDataKeys.last_bots_message_id], 
                text=text, 
                reply_markup=InlineKeyboardMarkup(inline_buttons)
                )
            
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
    return EMAIL


async def end_of_conv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f'''
Спасибо что оставили заявку, для изменения нажмите <<назад>>,
чтобы сохранить данные нажмите <<главное меню>>, после чего вам напишет наш специалист
собранная информация:
'''
    inline_buttons = [[
        InlineKeyboardButton("назад", callback_data=CallBackData.email.value),
        InlineKeyboardButton("главное меню", callback_data=CallBackData.main_menu_save.value)
        ]
    ]
    
    if context.user_data[UserDataKeys.last_message_text] != text:
        context.user_data[UserDataKeys.email] = update.message.text

        text_cont = f'''
Телеграмм ник:  {context.user_data[UserDataKeys.username]}
ФИО: {context.user_data[UserDataKeys.full_name]}
Пол: {context.user_data[UserDataKeys.gender]}
Номер телефона: {context.user_data[UserDataKeys.phone_number]}
email: {context.user_data[UserDataKeys.email]}
        '''
        full_text = text+"\n"+text_cont
        context.user_data[UserDataKeys.last_message_text] = full_text
        
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=context.user_data[UserDataKeys.last_bots_message_id],
            text=full_text,
            reply_markup=InlineKeyboardMarkup(inline_buttons)
        )

    await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
    return CONV_END
        

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    inline_buttons = [[
        InlineKeyboardButton("назад", callback_data=CallBackData.main_menu.value),
    ]]
    text = "вы можете узнать о нас больше на нашем сайте: https://getnif.com/wp-admin/"
    context.user_data[UserDataKeys.last_message_text] = text
    await update.callback_query.edit_message_text(text=text, reply_markup=InlineKeyboardMarkup(inline_buttons))
    return ABOUT


def main():
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', main_menu)],
        states = {
            MAIN_MENU: [
                CallbackQueryHandler(enter_client_name, CallBackData.full_name.value),
                CallbackQueryHandler(about, CallBackData.about.value)
                ],

            FULL_NAME: [
                CallbackQueryHandler(main_menu, CallBackData.main_menu.value),
                MessageHandler(filters.Text(), enter_client_gender)
                ],
            GENDER: [
                CallbackQueryHandler(enter_client_name, CallBackData.full_name.value),
                CallbackQueryHandler(enter_client_phone_number, CallBackData.man.value),
                CallbackQueryHandler(enter_client_phone_number, CallBackData.wooman.value),
                MessageHandler(filters.TEXT, enter_client_gender)
                ],
            PHONE_NUMBER: [
                CallbackQueryHandler(enter_client_gender, CallBackData.gender.value),
                MessageHandler(filters.Regex("[1-9][0-9]{10}"), enter_client_email),
                MessageHandler(filters.TEXT, enter_client_phone_number)
                ],
            EMAIL: [
                CallbackQueryHandler(enter_client_phone_number, CallBackData.phone_number.value),
                # MessageHandler(filters.Regex(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"), end_of_conv),
                MessageHandler(filters.Text(), end_of_conv)
                ],
            CONV_END: [
                CallbackQueryHandler(enter_client_email, CallBackData.email.value),
                CallbackQueryHandler(main_menu, CallBackData.main_menu_save.value),
            ],
            ABOUT: [CallbackQueryHandler(main_menu, CallBackData.main_menu.value)],
        },
        fallbacks=[MessageHandler(filters.Text(), main_menu)]
    )

    with open(BOT_TOKEN) as file:
        bot_token = json.load(file)["telegram_token"]

    application = Application.builder().token(bot_token).build()
    application.add_handler(conv_handler)
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()