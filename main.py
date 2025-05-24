import gspread
import pandas as pd
import datetime
import yagmail
import os
from google.oauth2.service_account import Credentials
from zoneinfo import ZoneInfo
import time
import logging
import random

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
SLEEP_TIME = 3600
IST = ZoneInfo("Asia/Kolkata")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

# Ensure the environment variables are set
if not EMAIL_USER or not EMAIL_PASS:
    logging.error("Missing email credentials in environment variables")
    raise ValueError("Missing email credentials in environment variables")
if not os.path.exists("service_account.json"):
    logging.error(
        "Service account file not found. Please provide 'service_account.json'."
    )
    raise FileNotFoundError(
        "Service account file not found. Please provide 'service_account.json'."
    )


def calculate_years(date_str: str) -> int:
    date = datetime.datetime.strptime(date_str, "%d-%m-%Y")
    today = datetime.datetime.now(IST)
    return format_number_with_suffix(today.year - date.year)


def format_number_with_suffix(n: int) -> str:
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


now = datetime.datetime.now(IST)
target = now.replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(
    days=1
)
sleep_time = (target - now).total_seconds()
logging.info(f"Sleep time is {int(sleep_time)} seconds until 12:00 AM...")
if sleep_time <= 3600:
    time.sleep(sleep_time)


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

creds = Credentials.from_service_account_file("service_account.json", scopes=SCOPES)
client = gspread.authorize(creds)
sheet = client.open("Events").sheet1

data = sheet.get_all_records()
df = pd.DataFrame(data)
today = datetime.datetime.now(IST).strftime("%m-%d")
# Message bodies
bodies = [
    """Hi {name},

Wishing you a fantastic birthday filled with joy, laughter, and celebration! 🎂🎈
May this year bring you new adventures and cherished memories.
""",
    """Hey {name},

Happy Birthday! 🎉✨
Hope your day is as amazing as you are. Stay awesome and keep smiling! 😊🎁
""",
    """Hi {name},

Cheers to you on your birthday! 🥂🎂
May this special day be the beginning of an amazing year ahead! 🎁🌈
""",
    """Hello {name},

Wishing you smiles, laughter, and tons of love on your birthday! 😊💖
Enjoy every moment of your special day! 🎉🎂
""",
    """Hey {name},

Hope your birthday is as sweet and bright as you are! 🍰🌟
Have a wonderful celebration! 🎈🎁
""",
    """Hi {name},

Happy Birthday to you! 🎊🎂
May your day be filled with happiness, your year with purpose, and your heart with love. ❤️
""",
    """Hi {name},

Wishing you a magical birthday and a year full of sparkles and dreams come true! ✨🎉
Have an amazing one! 🎂🎁
""",
    """Hi {name},

On your special day, may laughter and love surround you. ❤️🎉
Wishing you the happiest birthday and a brilliant year ahead! 🎂✨
""",
    """Hi {name},

Wishing you joy that lasts the whole year, not just your birthday! 🎈🥳
Have an awesome celebration and a fabulous year ahead! 🎁🍰
""",
]

for _, row in df.iterrows():
    event_date = datetime.datetime.strptime(row["date"], "%d-%m-%Y").strftime("%m-%d")
    age_str = row["date"]

    if event_date == today:
        name = row["name"]
        email = row["email"]
        subject = f"Happy {calculate_years(age_str)} Birthday, {name}! 🎉"
        body = random.choice(bodies).format(name=name)
        logging.info(f"Sending email to {name} ({email})...")

        try:
            yag = yagmail.SMTP(user=EMAIL_USER, password=EMAIL_PASS)
            yag.send(to=email, subject=subject, contents=body)
            logging.info(f"Email sent to {name} ({email})")
        except Exception as e:
            logging.error(f"Failed to send to {name}: {e}")
            raise
logging.info("Script completed successfully.")
