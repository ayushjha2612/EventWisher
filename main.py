import gspread
import pandas as pd
import datetime
import yagmail
import os
from google.oauth2.service_account import Credentials
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")
def calculate_age(birth_date_str: str) -> int:
    birth_date = datetime.datetime.strptime(birth_date_str, "%d-%m-%Y")
    today = datetime.datetime.now(IST)
    return format_number_with_suffix(today.year - birth_date.year)


def format_number_with_suffix(n: int) -> str:
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


# --- Optional: sleep until midnight ---
now = datetime.datetime.now(IST)
target = now.replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
# target = now.replace(hour=21, minute=29, second=00, microsecond=0)

sleep_time = (target - now).total_seconds()
print(f"Sleeping for {int(sleep_time)} seconds until 12:00 AM...")
# time.sleep(sleep_time)

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

creds = Credentials.from_service_account_file("service_account.json", scopes=SCOPES)
client = gspread.authorize(creds)
sheet = client.open("Events").sheet1

data = sheet.get_all_records()
df = pd.DataFrame(data)
print(df)

today = datetime.datetime.now(IST).strftime("%m-%d")

for _, row in df.iterrows():
    birthday = datetime.datetime.strptime(row["date"], "%d-%m-%Y").strftime("%m-%d")
    age_str = row["date"]

    if birthday == today:
        name = row["name"]
        email = row["email"]
        subject = f"Happy {calculate_age(age_str)} Birthday, {name}! 🎉"
        body = f"""
        Hi {name},

        Wishing you a fantastic birthday filled with joy, laughter, and celebration! 🎂🎈
        May this year bring you new adventures and cherished memories.
        """
        print(f"Sending email to {name} ({email})...")
        if not EMAIL_USER or not EMAIL_PASS:
            raise ValueError("Missing email credentials in environment variables")

        try:
            yag = yagmail.SMTP(user=EMAIL_USER, password=EMAIL_PASS)
            yag.send(to=email, subject=subject, contents=body)
            print(f"Email sent to {name} ({email})")
        except Exception as e:
            print(f"Failed to send to {name}: {e}")
