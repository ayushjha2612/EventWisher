import logging
from utils.helper import validate_env, sleep_till_midnight, get_events_sheet_df
from modules.event_wisher import event_wisher

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

if __name__ == "__main__":
    validate_env()
    sleep_till_midnight()
    df = get_events_sheet_df()
    logging.info("Starting to process events...")
    event_wisher(df)
    logging.info("Script completed successfully.")
