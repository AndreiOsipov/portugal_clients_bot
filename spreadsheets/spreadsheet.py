import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload


from bot_paths.paths import GOOGLE_API_TOKEN_PATH, GOOGLE_API_CREDS_PATH

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    ]


SPREADSHEET_ID = "1xKMQaXdXKX7urG-m3BQqGlzC1FfjqFBEe4KmwGxLsSU"
LIST_ID = 0

class GoogleAPILogin:
    def get_auth_creds(self):
        """возвращает разрешения на использование гугл-таблиц и гугл-диска"""
        creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file(GOOGLE_API_TOKEN_PATH, SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(GOOGLE_API_CREDS_PATH, SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(GOOGLE_API_TOKEN_PATH, 'w') as token:
                token.write(creds.to_json())
        return creds

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
