import gspread
from google.oauth2.service_account import Credentials

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

try:
    creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
    client = gspread.authorize(creds)
    
    print("--- Robot Vision Test ---")
    print("I have access to these files:")
    for s in client.openall():
        print(f"- '{s.title}'")
except Exception as e:
    print(f"Connection failed: {e}")
