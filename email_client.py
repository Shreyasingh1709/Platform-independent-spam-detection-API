
import os
from dotenv import load_dotenv
load_dotenv()
import requests
from imapclient import IMAPClient
import pyzmail

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/predict")
IMAP_SERVER = os.getenv("IMAP_SERVER", "imap.gmail.com")
SOURCE = os.getenv("SOURCE", "email")

def fetch_and_detect():
    with IMAPClient(IMAP_SERVER) as server:
        server.login(EMAIL, PASSWORD)
        server.select_folder('INBOX', readonly=True)
        messages = server.search(['NOT', 'DELETED'])
        for uid, message_data in server.fetch(messages[-10:], ['BODY[]']).items():
            msg = pyzmail.PyzMessage.factory(message_data[b'BODY[]'])
            subject = msg.get_subject()
            if msg.text_part:
                body = msg.text_part.get_payload().decode(msg.text_part.charset or 'utf-8', errors='ignore')
            elif msg.html_part:
                body = msg.html_part.get_payload().decode(msg.html_part.charset or 'utf-8', errors='ignore')
            else:
                body = ""
            text = subject + " " + body
            response = requests.post(API_URL, json={
                "text": text,
                "source": SOURCE
            })
            result = response.json()["prediction"] if response.ok else "API error"
            print(f"Subject: {subject}\nPrediction: {result}\n{'-'*40}")

if __name__ == "__main__":
    fetch_and_detect()
