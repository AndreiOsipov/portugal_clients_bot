import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


from bot_paths.paths import GOOGLE_API_CREDS_PATH

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    ]


SPREADSHEET_ID = "1xKMQaXdXKX7urG-m3BQqGlzC1FfjqFBEe4KmwGxLsSU"
LIST_ID = 0

class GoogleAPILogin:
    def get_auth_creds(self):
        return Credentials.from_service_account_file(GOOGLE_API_CREDS_PATH)

class QueriesGoogleSheets:
    def __init__(self) -> None:
        self.creds = GoogleAPILogin().get_auth_creds()
        self.service = build('sheets', 'v4', credentials=self.creds)
        self._spreadsheet_id = SPREADSHEET_ID
        
    def write_data(self, data:list[str]):
        range_name = 'clients'  # Имя листа
        value_input_option = 'RAW'
        value_range_body = {
            'majorDimension': 'ROWS',
            'values': [data]
        }

        self.service.spreadsheets().values().append(
            spreadsheetId=self._spreadsheet_id,
            range=range_name,
            valueInputOption=value_input_option,
            body=value_range_body
        ).execute()
