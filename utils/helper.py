import logging
from constants import EMAIL_USER, EMAIL_PASS, IST, SLEEP_TIME_LIMIT, SCOPES
import os
import datetime
import time
from google.oauth2.service_account import Credentials
import gspread
import pandas as pd


def validate_env():
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


def sleep_till_midnight():
    now = datetime.datetime.now(IST)
    target = now.replace(
        hour=0, minute=0, second=0, microsecond=0
    ) + datetime.timedelta(days=1)
    sleep_time = (target - now).total_seconds() - 1
    if sleep_time <= SLEEP_TIME_LIMIT:
        logging.info(f"Sleeping for {int(sleep_time)} seconds until 12:00 AM...")
        time.sleep(sleep_time)


def get_events_sheet_df():
    creds = Credentials.from_service_account_file("service_account.json", scopes=SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open("Events").sheet1

    data = sheet.get_all_records()
    return pd.DataFrame(data)
