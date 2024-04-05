import enum


class BotsDataKeys(enum.Enum):
    last_bots_message_id = "last_bots_message_id"
    last_bots_message_text = "last_bots_message_text"


class UserDataKeys(enum.Enum):    
    username = "username"
    age = "age"
    father_full_name = "father_full_name"
    mother_full_name = "mother_full_name"
    purpose = "purpose"
    first_name = "first_name"
    last_name = "last_name"
    phone_number = "phone_number"
    email = "email"
    nationality = "nationality"
    birthday = "birthday"
    gender = "gender"
    country_birth = "country_birth"
    document_type = "document_type"
    document_number = "document_number"
    country_issuer = "country_issuer"
    validity_date = "validity_date"
    residence_addres = "residence_addres"
    current_country = "current_country"
    postal_code = "postal_code"


class AgeCallbackData(enum.Enum):
    adult = "adult"
    minor = "minor"

class MainMenuCallbackData(enum.Enum):
    about = "about"
    questionnaire_start = "questionnaire_start"


class PurposeCallBackData(enum.Enum):
    main_menu = "main_menu"
    live_in_portugal = "live_in_portugal"
    undertaking__in_portugal = "undertaking__in_portugal"
    buy_property_in_portugal = "buy_property_in_portugal"
    open_bank_account_in_portugal = "open_bank_account_in_portugal"
    visa = "visa"
    other = "orher"


class CountryCabackData(enum.Enum):
    bact_to_enter_last_name = "bact_to_enter_last_name"
    rus = "RUS"
    kaz = "KAZ"
    blr = "BLR"


class GenderCallbackData(enum.Enum):
    man = "man"
    woman = "woman"


class DocumentTypeCallbackData(enum.Enum):
    passport = "passport"
    bi = "bi"
    citizen_card = "citizen_card"


class GeneralCallBackData(enum.Enum):
    back_to_previous_handler = "back_to_previous_handler"
    main_menu_save = "main_menu_save"
    

