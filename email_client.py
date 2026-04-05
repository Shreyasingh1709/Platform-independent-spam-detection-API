

import os
from dotenv import load_dotenv
load_dotenv()
import requests
from imapclient import IMAPClient
import pyzmail
import database

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/predict")
IMAP_SERVER = os.getenv("IMAP_SERVER", "imap.gmail.com")
SOURCE = os.getenv("SOURCE", "email")

def fetch_and_detect():
    with IMAPClient(IMAP_SERVER) as server:
        server.login(EMAIL, PASSWORD)
        server.select_folder('INBOX', readonly=True)
        # Fetch all unseen emails first
        unseen = server.search(['UNSEEN'])
        # If not enough unseen, also fetch last 100 emails
        messages = list(set(unseen + server.search(['NOT', 'DELETED'])))[-100:]
        for uid, message_data in server.fetch(messages, ['BODY[]']).items():
            # Check if UID already exists
            if database.uid_exists(str(uid)):
                print(f"[DEBUG] Skipping UID {uid} (already in database)")
                continue
            msg = pyzmail.PyzMessage.factory(message_data[b'BODY[]'])
            subject = msg.get_subject()
            if msg.text_part:
                body = msg.text_part.get_payload().decode(msg.text_part.charset or 'utf-8', errors='ignore')
            elif msg.html_part:
                body = msg.html_part.get_payload().decode(msg.html_part.charset or 'utf-8', errors='ignore')
            else:
                body = ""
            text = subject + " " + body
            print(f"[DEBUG] Fetched email UID: {uid}, Subject: {subject}")
            response = requests.post(API_URL, json={
                "message": text,
                "uid": str(uid),
                "source": SOURCE
            })
            if response.ok:
                result_json = response.json()
                prediction = result_json.get("prediction", "?")
                confidence = result_json.get("confidence", None)
                if prediction == "?":
                    print(f"[ERROR] API response missing or invalid prediction for UID {uid}: {result_json}")
                # Save to database with UID
                database.insert_data(str(uid), text, prediction, confidence)
                print(f"[DEBUG] Inserted UID {uid} into database with prediction: {prediction}")
            else:
                prediction = "API error"
                confidence = None
                print(f"[DEBUG] API error for UID {uid}")
            print(f"Subject: {subject}\nPrediction: {prediction}\nConfidence: {confidence}\n{'-'*40}")

if __name__ == "__main__":
    fetch_and_detect()
