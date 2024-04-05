from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ContextTypes,
)

from conv_enums import UserDataKeys,BotsDataKeys, GeneralCallBackData
from spreadsheets.spreadsheet import QueriesGoogleSheets

class BaseEndpoint:    
    def __init__(self, conversation_state: int, text: str, buttons: list[list[InlineKeyboardButton]], enter_callbacks_data: list[str] = None) -> None:
        self.conversation_state = conversation_state
        self.text = text
        self.buttons = buttons
        self.enter_callbacks_data = enter_callbacks_data


    def check_callback_data(self, callback_data: str):
        return self.enter_callbacks_data and callback_data in self.enter_callbacks_data


    def previous_bots_responce_text_different(self, context: ContextTypes.DEFAULT_TYPE):
        return context.user_data[BotsDataKeys.last_bots_message_text] != self.text


    def change_state(self, context: ContextTypes.DEFAULT_TYPE) -> int:
        context.user_data[BotsDataKeys.last_bots_message_text] = self.text
        return self.conversation_state


    async def handle_trigger_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=context.user_data[BotsDataKeys.last_bots_message_id],
            text=self.text, 
            reply_markup=InlineKeyboardMarkup(self.buttons))
    
 
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await update.callback_query.edit_message_text(
            text=self.text, 
            reply_markup=InlineKeyboardMarkup(self.buttons))
        return self.change_state(context)
    
 
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        if self.previous_bots_responce_text_different(context):
            await self.handle_trigger_message(update, context)        
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
        return self.change_state(context)
    

class RecipientEndPoint(BaseEndpoint):
    def __init__(
            self,
            conversation_state: int, 
            text: str, 
            buttons: list[list[InlineKeyboardButton]],
            enter_callbacks_data: list[str] = None,
            user_callback_key: str = None,
            user_message_key: str = None,
        ) -> None:
        
        super().__init__(conversation_state, text, buttons, enter_callbacks_data)
        self.user_callback_key = user_callback_key
        self.user_message_key = user_message_key
    
    def is_write_callback(self, update: Update):
        return update.callback_query != GeneralCallBackData.back_to_previous_handler.value
    
    async def handle_trigger_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data[self.user_message_key] = update.message.text
        await super().handle_trigger_message(update, context)

    def context_set_callback_data(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data[self.user_callback_key] = update.callback_query.data

    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:    
        if self.is_write_callback(update):
            self.context_set_callback_data(update, context)
        return await super().handle_callback(update, context)
            

class ConversationEndEndPoint(RecipientEndPoint):
    
    async def handle_trigger_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data[self.user_message_key] = update.message.text
        message_text = self.text 
        # + [
        #     "\n".join(data_key.value + ": "+ context.user_data[data_key.value]) 
        #     for data_key in UserDataKeys 
        #     if data_key.value in context.user_data.keys()
        #  ][0]
        await context.bot.edit_message_text(
            chat_id=update.effective_chat.id,
            message_id=context.user_data[BotsDataKeys.last_bots_message_id],
            text=message_text,
            reply_markup=InlineKeyboardMarkup(self.buttons))


class MainMenuEndPoint(BaseEndpoint):
    def __init__(
            self,
            google_sheet:QueriesGoogleSheets,
            conversation_state: int,
            text: str,
            buttons: list[list[InlineKeyboardButton]],
            enter_callbacks_data: list[str] = None) -> None:
        super().__init__(conversation_state, text, buttons, enter_callbacks_data)
        self.google_sheet = google_sheet

  
    def write_user_data_to_google_sheet(self, context: ContextTypes.DEFAULT_TYPE):
        self.google_sheet.write_data([
            context.user_data[data_key.value]
            if data_key.value in context.user_data.keys()
            else "---"
            for data_key in UserDataKeys 
            ])


    def is_write_callback(self, update: Update):
        return update.callback_query.data == GeneralCallBackData.main_menu_save.value


    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        last_message_id = context.user_data.get(BotsDataKeys.last_bots_message_id)
        if last_message_id:
            if self.previous_bots_responce_text_different(context):
                await self.handle_trigger_message(update, context)
        else:
            message = await update.message.reply_text(self.text, reply_markup=InlineKeyboardMarkup(self.buttons))
            context.user_data[BotsDataKeys.last_bots_message_id] = message.message_id
            context.user_data[UserDataKeys.username.value] = update.message.from_user.username

        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
        return self.change_state(context)


    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        if self.is_write_callback(update):
            self.write_user_data_to_google_sheet(context)
        return await super().handle_callback(update, context)
    