import datetime
import logging
import random
from utils.helper import calculate_years, sleep_till_midnight
from constants import EMAIL_USER, EMAIL_PASS, IST, BODIES
import yagmail
import pandas as pd


def event_wisher(df: pd.DataFrame, target_day: str):
    for _, row in df.iterrows():
        event_date = datetime.datetime.strptime(row["date"], "%d-%m-%Y").strftime(
            "%m-%d"
        )
        age_str = row["date"]

        if event_date == target_day:
            name = row["name"]
            email = row["email"]
            subject = f"Happy {calculate_years(age_str)} Birthday, {name}! 🎉"
            body = random.choice(BODIES).format(name=name)
            sleep_till_midnight()
            logging.info(f"Sending email to {name} ({email})...")
            try:
                yag = yagmail.SMTP(user=EMAIL_USER, password=EMAIL_PASS)
                yag.send(to=email, subject=subject, contents=body)
                logging.info(f"Email sent to {name} ({email})")
            except Exception as e:
                logging.error(f"Failed to send to {name}: {e}")
                raise
