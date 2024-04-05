from bot_paths.paths import BOT_TOKEN
import json

from telegram import InlineKeyboardButton, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from spreadsheets.spreadsheet import QueriesGoogleSheets
from conv_enums import (
    UserDataKeys, 
    GeneralCallBackData, 
    PurposeCallBackData,
    CountryCabackData,
    MainMenuCallbackData,
    GenderCallbackData,
    DocumentTypeCallbackData,
    AgeCallbackData,
)
from telegram import InlineKeyboardButton, Update

from dialog_endpoints import (
    BaseEndpoint, 
    RecipientEndPoint,
    MainMenuEndPoint, 
    ConversationEndEndPoint,
    
)


(
    MAIN_MENU, 
    ABOUT,
    FATHER_FULL_NAME,
    MOTHER_FULL_NAME,
    ADULT,
    PURPOSE, 
    FIRST_NAME, 
    LAST_NAME, 
    PHONE_NUMBER,
    EMAIL, 
    NATIONALITY, 
    BIRTHDAY, 
    BIRTHDAY,
    GENDER,
    COUNTRY_BIRTH,
    DOCUMENT_TYPE,
    DOCUMENT_NUMBER,
    COUNTRY_ISSUER,
    VALIDITY_DOCUMENT,
    RESIDENCE_ADDRESS,
    CURRENT_COUNTRY,
    POSTAL_CODE,
    CONV_END,
) = range(23)

def main():
    back_button_keyboard = [[InlineKeyboardButton(text="назад", callback_data=GeneralCallBackData.back_to_previous_handler.value)]]
    
    adult_keyboard = [
        back_button_keyboard[0],
        [
            InlineKeyboardButton(text="больше 18", callback_data=AgeCallbackData.adult.value),
            InlineKeyboardButton(text="меньше 18",callback_data=AgeCallbackData.minor.value)
        ]
    ]
    countries_keyboard = [
        back_button_keyboard[0],
        [
            InlineKeyboardButton(text="Россия", callback_data=CountryCabackData.rus.value),
            InlineKeyboardButton(text="Казахстан", callback_data=CountryCabackData.kaz.value),
            InlineKeyboardButton(text="Беларусь", callback_data=CountryCabackData.blr.value)
        ]
    ]
    menu_keybpard = [[
        InlineKeyboardButton(text="Ввести или обновмить данные о себе", callback_data=MainMenuCallbackData.questionnaire_start.value),
        InlineKeyboardButton(text="О нас", callback_data=MainMenuCallbackData.about.value)
        ]
    ]

    purpose_keyboard = [back_button_keyboard[0],
        [
            InlineKeyboardButton(text="Жить в Португалии",callback_data=PurposeCallBackData.live_in_portugal.value),
            InlineKeyboardButton(text="Бизнес в Португалии",callback_data=PurposeCallBackData.undertaking__in_portugal.value),
        ],
        [
            InlineKeyboardButton(text="Купить недвижимость в Португалии",callback_data=PurposeCallBackData.buy_property_in_portugal.value),
            InlineKeyboardButton(text="открыть счет в банке",callback_data=PurposeCallBackData.open_bank_account_in_portugal.value),
        ],
        [
            InlineKeyboardButton(text="Виза",callback_data=PurposeCallBackData.visa.value),
            InlineKeyboardButton(text="Другое",callback_data=PurposeCallBackData.other.value),
        ]
    ]

    gender_keyboard = [
        back_button_keyboard[0],
        [
            InlineKeyboardButton(text="Муж.", callback_data=GenderCallbackData.man.value),
            InlineKeyboardButton(text="Жен.", callback_data=GenderCallbackData.woman.value),
        ]
    ]

    document_type_keyboard = [
            back_button_keyboard[0],
            [InlineKeyboardButton(text="Паспорт",callback_data=DocumentTypeCallbackData.passport.value)],
            [InlineKeyboardButton(text="BI",callback_data=DocumentTypeCallbackData.bi.value)],
            [InlineKeyboardButton(text="Citizin Card",callback_data=DocumentTypeCallbackData.citizen_card.value)]
        ]

    conversation_end_keyboard = [
        back_button_keyboard[0],
        [
            InlineKeyboardButton("главное меню", callback_data=GeneralCallBackData.main_menu_save.value)
        ]
    ]
    
    
    main_menu_endpoint = MainMenuEndPoint(
        google_sheet=QueriesGoogleSheets(),
        text="Здравствуйте, этот бот поможет оставить вам заявку на получение НИФ Португалии!",
        buttons=menu_keybpard,
        conversation_state=MAIN_MENU,
        enter_callbacks_data=[GeneralCallBackData.main_menu_save.value]
    )


    about_endpoint = BaseEndpoint(
        text="вы можете узнать о нас больше на нашем сайте: https://getnif.com/wp-admin/",
        buttons=back_button_keyboard,
        conversation_state=ABOUT,
        enter_callbacks_data=[MainMenuCallbackData.about.value]
    )

    enter_adult_endpoint = BaseEndpoint(
        text="Вам больше 18 лет?",
        buttons=adult_keyboard,
        conversation_state=ADULT,
        enter_callbacks_data=[MainMenuCallbackData.questionnaire_start.value]
    )

    
   
    enter_father_full_name_endpoint = RecipientEndPoint(
        text="Введите ФИО вашего отца",
        buttons=back_button_keyboard,
        conversation_state=FATHER_FULL_NAME,
        enter_callbacks_data=[AgeCallbackData.minor.value],
        user_callback_key=UserDataKeys.age.value
    )


    end_mother_full_name_endpoint = RecipientEndPoint(
        text="ВВедите ФИО вашей матери",
        buttons=back_button_keyboard,
        conversation_state=MOTHER_FULL_NAME,
        user_message_key=UserDataKeys.father_full_name.value
    )
    
    enter_purpose_endpoint = RecipientEndPoint(
        conversation_state=PURPOSE,
        text="выберете цель приобретения налогового номера",
        buttons=purpose_keyboard,
        enter_callbacks_data=[AgeCallbackData.adult.value],
        user_callback_key=UserDataKeys.age.value,
        user_message_key=UserDataKeys.mother_full_name.value
    )
    
    enter_first_name_endpoint = RecipientEndPoint(
        text="Введите Имя",
        buttons=back_button_keyboard,
        conversation_state=FIRST_NAME,
        enter_callbacks_data=[data.value for data in PurposeCallBackData],
        user_callback_key=UserDataKeys.purpose.value,
    )
    enter_last_name_endpoint = RecipientEndPoint(
        text="Введите фамилию",
        buttons= back_button_keyboard,
        conversation_state=LAST_NAME,
        user_message_key=UserDataKeys.first_name.value,
    )
    enter_phone_number_endpoint = RecipientEndPoint(
        text="введите ваш номер телефона",
        buttons=back_button_keyboard,
        conversation_state=PHONE_NUMBER,
        user_message_key=UserDataKeys.last_name.value,
    )
    enter_email_endpoint = RecipientEndPoint(
        text="Введите ваш email",
        buttons=back_button_keyboard,
        conversation_state=EMAIL,
        user_message_key=UserDataKeys.phone_number.value,
    )
    enter_nationality_endpoint = RecipientEndPoint(
        text="выбирете гражданство",
        buttons=countries_keyboard,
        conversation_state=NATIONALITY,
        user_message_key=UserDataKeys.email.value,
    )
    enter_birthday_endpoint = RecipientEndPoint(
        text = "введите дату рождения в формате DD.MM.YYYY, например 12.10.2000",
        buttons=back_button_keyboard,
        conversation_state=BIRTHDAY,
        enter_callbacks_data=[nationality.value for nationality in CountryCabackData],
        user_callback_key=UserDataKeys.nationality.value,
    )

    enter_gender_endpoint = RecipientEndPoint(
        text = "Выберете ваш пол",
        buttons=gender_keyboard,
        conversation_state=GENDER,
        user_message_key=UserDataKeys.birthday.value,
    )

    enter_country_birth_endpoint = RecipientEndPoint(
        text="Выберете страну рождения",
        buttons=countries_keyboard,
        conversation_state=COUNTRY_BIRTH,
        enter_callbacks_data=[gender.value for gender in GenderCallbackData],
        user_callback_key=UserDataKeys.gender.value, 
    )

    enter_document_type_endpoint = RecipientEndPoint(
        text = "Выберете тип документа",
        buttons = document_type_keyboard,
        conversation_state=DOCUMENT_TYPE,
        enter_callbacks_data=[country.value for country in CountryCabackData],
        user_callback_key=UserDataKeys.country_birth.value,
    )

    enter_document_number_endpoint = RecipientEndPoint(
        text = "Введите номер документа",
        buttons = back_button_keyboard,
        conversation_state=DOCUMENT_NUMBER,
        enter_callbacks_data=[doc_type.value for doc_type in  DocumentTypeCallbackData],
        user_callback_key=UserDataKeys.document_type.value,
    )

    enter_country_issuer_endpoint = RecipientEndPoint(
        text = "Выберете страну, выдавшую документ",
        buttons = countries_keyboard,
        conversation_state=COUNTRY_ISSUER,
        user_message_key=UserDataKeys.document_number.value,
    )

    enter_validity_document_endpoint = RecipientEndPoint(
        text = "введите дату истечения документа DD.MM.YYYY, например 12.10.2025",
        buttons=back_button_keyboard,
        conversation_state=VALIDITY_DOCUMENT,
        enter_callbacks_data=[country_issuer.value for country_issuer in CountryCabackData],
        user_callback_key=UserDataKeys.country_issuer.value,
    )

    enter_residence_address_endpoint = RecipientEndPoint(
        text="введите ваш полный адрес места жительства",
        buttons=back_button_keyboard,
        conversation_state=RESIDENCE_ADDRESS,
        user_message_key=UserDataKeys.validity_date.value,
    )

    enter_current_country_endpoint = RecipientEndPoint(
        text="введите текущую страну проживания",
        buttons=countries_keyboard,
        conversation_state=CURRENT_COUNTRY,
        user_message_key=UserDataKeys.residence_addres.value,
    )

    enter_postal_code_endpoint = RecipientEndPoint(
        text = "введите ваш почтовый индекс",
        buttons=back_button_keyboard,
        conversation_state=POSTAL_CODE,
        enter_callbacks_data=[country.value for country in CountryCabackData],
        user_callback_key=UserDataKeys.current_country.value,
    )
    
    end_of_conversation_endpoint = ConversationEndEndPoint(
        text="Спасибо, что оставили заявку!",
        buttons=conversation_end_keyboard,
        conversation_state=CONV_END,
        user_message_key=UserDataKeys.postal_code.value,
    )

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', main_menu_endpoint.handle_message)],
     
        states = {
            MAIN_MENU: [
                CallbackQueryHandler(enter_adult_endpoint.handle_callback, enter_adult_endpoint.check_callback_data),
                CallbackQueryHandler(about_endpoint.handle_callback, about_endpoint.check_callback_data),
                MessageHandler(filters.Text(), main_menu_endpoint.handle_message)
                ],
            ABOUT: [
                CallbackQueryHandler(main_menu_endpoint.handle_callback, GeneralCallBackData.back_to_previous_handler.value),
                MessageHandler(filters.Text(), about_endpoint.handle_message)
                ],
            ADULT: [
                CallbackQueryHandler(main_menu_endpoint.handle_callback, GeneralCallBackData.back_to_previous_handler.value),
                CallbackQueryHandler(enter_father_full_name_endpoint.handle_callback, enter_father_full_name_endpoint.check_callback_data),
                CallbackQueryHandler(enter_purpose_endpoint.handle_callback, enter_purpose_endpoint.check_callback_data),
                MessageHandler(filters.Text(), enter_adult_endpoint.handle_message)
            ],
            FATHER_FULL_NAME: [
                CallbackQueryHandler(enter_adult_endpoint.handle_callback, GeneralCallBackData.back_to_previous_handler.value),
                MessageHandler(filters.Text(), end_mother_full_name_endpoint.handle_message)
            ],
            MOTHER_FULL_NAME: [
                CallbackQueryHandler(enter_father_full_name_endpoint.handle_callback, GeneralCallBackData.back_to_previous_handler.value),
                MessageHandler(filters.Text(), enter_purpose_endpoint.handle_message)
            ],

            PURPOSE:[
                CallbackQueryHandler(enter_adult_endpoint.handle_callback, GeneralCallBackData.back_to_previous_handler.value),
                CallbackQueryHandler(enter_first_name_endpoint.handle_callback, enter_first_name_endpoint.check_callback_data),
                MessageHandler(filters.Text(), enter_purpose_endpoint.handle_message)
            ],
            FIRST_NAME:[
                CallbackQueryHandler(enter_purpose_endpoint.handle_callback, GeneralCallBackData.back_to_previous_handler.value),
                MessageHandler(filters.Text(), enter_last_name_endpoint.handle_message)
            ],
            LAST_NAME:[
                CallbackQueryHandler(enter_first_name_endpoint.handle_callback, GeneralCallBackData.back_to_previous_handler.value),
                MessageHandler(filters.Text(), enter_phone_number_endpoint.handle_message)
            ],
            PHONE_NUMBER: [
                CallbackQueryHandler(enter_last_name_endpoint.handle_callback, GeneralCallBackData.back_to_previous_handler.value),
                MessageHandler(filters.Regex("[1-9][0-9]{10}"), enter_email_endpoint.handle_message),
                MessageHandler(filters.Text(), enter_phone_number_endpoint.handle_message)
            ],
            EMAIL : [
                CallbackQueryHandler(enter_phone_number_endpoint.handle_callback, GeneralCallBackData.back_to_previous_handler.value),
                MessageHandler(filters.Text(), enter_nationality_endpoint.handle_message)
            ],
            NATIONALITY: [
                CallbackQueryHandler(enter_email_endpoint.handle_callback, GeneralCallBackData.back_to_previous_handler.value),
                CallbackQueryHandler(enter_birthday_endpoint.handle_callback, enter_birthday_endpoint.check_callback_data),
                MessageHandler(filters.Text(), enter_nationality_endpoint.handle_message)
            ],
            BIRTHDAY: [
                CallbackQueryHandler(enter_nationality_endpoint.handle_callback, GeneralCallBackData.back_to_previous_handler.value),
                MessageHandler(filters.Regex("[1-9][0-9].[0-9][0-9].[1-9][0-9][0-9][0-9]"), enter_gender_endpoint.handle_message),
                MessageHandler(filters.Text(), enter_birthday_endpoint.handle_message)
            ],
            GENDER: [
                CallbackQueryHandler(enter_birthday_endpoint.handle_callback, GeneralCallBackData.back_to_previous_handler.value),
                CallbackQueryHandler(enter_country_birth_endpoint.handle_callback, enter_country_birth_endpoint.check_callback_data),
                MessageHandler(filters.Text(), enter_gender_endpoint.handle_message)
            ],
            COUNTRY_BIRTH: [
                CallbackQueryHandler(enter_gender_endpoint.handle_callback, GeneralCallBackData.back_to_previous_handler.value),
                CallbackQueryHandler(enter_document_type_endpoint.handle_callback, enter_document_type_endpoint.check_callback_data),
                MessageHandler(filters.Text(), enter_country_birth_endpoint.handle_message)
            ],
            DOCUMENT_TYPE: [
                CallbackQueryHandler(enter_country_birth_endpoint.handle_callback, GeneralCallBackData.back_to_previous_handler.value),
                CallbackQueryHandler(enter_document_number_endpoint.handle_callback, enter_document_number_endpoint.check_callback_data),
                MessageHandler(filters.Text(), enter_document_type_endpoint.handle_message)
            ],
            DOCUMENT_NUMBER: [
                CallbackQueryHandler(enter_document_type_endpoint.handle_callback, GeneralCallBackData.back_to_previous_handler.value),
                MessageHandler(filters.Regex("\d+"), enter_country_issuer_endpoint.handle_message),
                MessageHandler(filters.Text(), enter_document_number_endpoint.handle_message)

            ],
            COUNTRY_ISSUER: [
                CallbackQueryHandler(enter_document_number_endpoint.handle_callback, GeneralCallBackData.back_to_previous_handler.value),
                CallbackQueryHandler(enter_validity_document_endpoint.handle_callback, enter_validity_document_endpoint.check_callback_data),
                MessageHandler(filters.Text(), enter_country_issuer_endpoint.handle_message)
            ],
            VALIDITY_DOCUMENT: [
                CallbackQueryHandler(enter_country_issuer_endpoint.handle_callback, GeneralCallBackData.back_to_previous_handler.value),
                MessageHandler(filters.Regex("[1-9][0-9].[0-9][0-9].[1-9][0-9][0-9][0-9]"), enter_residence_address_endpoint.handle_message),
                MessageHandler(filters.Text(), enter_validity_document_endpoint.handle_message)

            ],
            RESIDENCE_ADDRESS: [
                CallbackQueryHandler(enter_validity_document_endpoint.handle_callback, GeneralCallBackData.back_to_previous_handler.value),
                MessageHandler(filters.Text(), enter_current_country_endpoint.handle_message)                
            ],
            CURRENT_COUNTRY: [
                CallbackQueryHandler(enter_residence_address_endpoint.handle_callback, GeneralCallBackData.back_to_previous_handler.value),
                CallbackQueryHandler(enter_postal_code_endpoint.handle_callback, enter_postal_code_endpoint.check_callback_data),
                MessageHandler(filters.Text(), enter_current_country_endpoint.handle_message)
            ],
            POSTAL_CODE: [
                CallbackQueryHandler(enter_current_country_endpoint.handle_callback, GeneralCallBackData.back_to_previous_handler.value),
                MessageHandler(filters.Regex("\d+"), end_of_conversation_endpoint.handle_message),
                  MessageHandler(filters.Text(), enter_postal_code_endpoint.handle_message)
            ],
            CONV_END: [
                CallbackQueryHandler(enter_postal_code_endpoint.handle_callback, GeneralCallBackData.back_to_previous_handler.value),
                CallbackQueryHandler(main_menu_endpoint.handle_callback, main_menu_endpoint.check_callback_data),
                MessageHandler(filters.Text(), end_of_conversation_endpoint.handle_message)
            ]
        },
        fallbacks=[MessageHandler(filters.Text(), main_menu_endpoint.handle_message)]
    )

    with open(BOT_TOKEN) as file:
        bot_token = json.load(file)["telegram_token"]

    application = Application.builder().token(bot_token).build()
    application.add_handler(conv_handler)
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()