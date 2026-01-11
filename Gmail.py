
from tokenrizer import GoogleToken
from googleapiclient.discovery import build


class Gmail:
    def __init__(self, TOKEN_FILE):
        self.SCOPES = ["https://mail.google.com/"]
        self.TOKEN_FILE = TOKEN_FILE
        self.creds = GoogleToken(TOKEN_FILE, self.SCOPES)
        self.service = build("gmail","v1",credentials=self.creds)
    def __getattribute__(self, name):
        atr = super().__getattribute__(name)
        if name not in ["__init__","__getattribute__","refresh_token"] and callable(atr):
            def new_func(*args, **kwargs):
                print("Gmail ; ",name)
                return atr(*args, **kwargs)
            return new_func
        return atr
    def refresh_token(self):
        self.creds = GoogleToken(self.TOKEN_FILE, self.SCOPES)
    def list_messages(self, query="is:unread", max_results=100):
        results = self.service.users().messages().list(
            userId="me", q=query, maxResults=max_results
        ).execute()
        messages=[{'id':i['id'],'subject' : self.get_formated_massage(i['id'])['Subject']} for i in results.get('messages', ['id'])]
        return messages
    def get_message(self, msg_id, format='metadata'):
        message = self.service.users().messages().get(
            userId='me', id=msg_id, format=format
        ).execute()
        return message
    def get_formated_massage(self, msg_id):
        txt = self.get_message(msg_id, format='metadata')
        headers = {i['name']: i['value'] for i in txt['payload']['headers']}
        return {
            'id': txt['id'],
            'threadId': txt['threadId'],
            'Subject': headers["Subject"],
            'Snippet': txt['snippet'],
            'From': headers["From"],
            'To': headers["To"],
            'Date': headers["Date"],
        }
    def send_to(self, To, Subject, Body):
        from email.message import EmailMessage
        import base64
        msg = EmailMessage()
        msg.set_content(Body)
        msg['Subject'] = Subject
        msg['From'] = "me"
        msg['To'] = To
        encodedMsg = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        raw = {'raw': encodedMsg}
        self.service.users().messages().send(userId="me", body=raw).execute()
        print("Email sent to", To)