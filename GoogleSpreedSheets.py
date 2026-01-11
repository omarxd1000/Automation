import os.path
import pickle
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from tokenrizer import GoogleToken

class GoogleSpreedsheets:
    def __init__(self, TOKEN_FILE= 'google_spreadsheets_token.pickle'):
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
                       'https://www.googleapis.com/auth/drive.metadata.readonly',]
        self.TOKEN_FILE = TOKEN_FILE
        self.AppName = "GoogleSpreedsheets"
        self.creds = GoogleToken(TOKEN_FILE, self.SCOPES)
        self.service = build('sheets', 'v4', credentials=self.creds)
        self.drive_service = build('drive', 'v3', credentials=self.creds)
    def __getattribute__(self, name):
        atr = super().__getattribute__(name)
        if name not in ["__init__","__getattribute__","refresh_token"] and callable(atr):
            def new_func(*args, **kwargs):
                print("GoogleSpreedsheets ;",name)
                return atr(*args, **kwargs)
            return new_func
        return atr
    def refresh_token(self):
        self.creds = GoogleToken(self.TOKEN_FILE, self.SCOPES)
    def list(self):
        query = "mimeType = 'application/vnd.google-apps.spreadsheet'"
        results = self.drive_service.files().list(
            q=query,
            pageSize=1000,
            fields="nextPageToken, files(id, name)"
        ).execute()
        items = results.get('files')
        return items
    def read(self, SPREADSHEET_ID, RANGE_NAME):
        sheet = self.service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=RANGE_NAME).execute()
        values = result.get('values', [])
        return values
    def write(self, SPREADSHEET_ID, RANGE_NAME, values, valueInputOption='RAW'):
        body = {
            'values': values
        }
        result = self.service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME,
            valueInputOption=valueInputOption,  # Use 'USER_ENTERED' if you want formulas to parse
            body=body
        ).execute()
        return result
