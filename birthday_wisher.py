import gspread
import pandas as pd
import datetime
import yagmail
import os
import time
from google.oauth2.service_account import Credentials

# --- Optional: sleep until midnight ---
now = datetime.datetime.now()
target = now.replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
sleep_time = (target - now).total_seconds()
print(f"Sleeping for {int(sleep_time)} seconds until 12:00 AM...")
time.sleep(sleep_time)

# --- Load environment variables ---
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

# --- Connect to Google Sheets ---
scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
creds = Credentials.from_service_account_file("service_account.json", scopes=scopes)
client = gspread.authorize(creds)

sheet = client.open("Birthday Sheet").sheet1
data = sheet.get_all_records()
df = pd.DataFrame(data)

# --- Check for today's birthdays ---
today = datetime.datetime.now().strftime("%m-%d")

for _, row in df.iterrows():
    birthday = datetime.datetime.strptime(row['Birthday'], "%Y-%m-%d").strftime("%m-%d")
    if birthday == today:
        name = row['Name']
        email = row['Email']
        subject = f"Happy Birthday, {name}! 🎉"
        body = f"""
        Hi {name},

        Wishing you a fantastic birthday filled with joy, laughter, and celebration! 🎂🎈

        Best regards,
        Ayush
        """
        try:
            yag = yagmail.SMTP(EMAIL_USER, EMAIL_PASS)
            yag.send(to=email, subject=subject, contents=body)
            print(f"✅ Email sent to {name} ({email})")
        except Exception as e:
            print(f"❌ Failed to send to {name}: {e}")
