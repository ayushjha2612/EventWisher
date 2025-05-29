import logging
from utils.helper import validate_env, get_events_sheet_df, get_day
from modules.event_wisher import event_wisher

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

if __name__ == "__main__":
    validate_env()
    df = get_events_sheet_df()
    logging.info("Starting to process events...")
    target_day = get_day()
    event_wisher(df, target_day)
    logging.info("Script completed successfully.")
