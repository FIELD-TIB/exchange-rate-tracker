# This module starts the periodic background job that calls the fetch logic.
# It is separated from the request handlers so the app remains easy to maintain.

import logging

from apscheduler.schedulers.background import BackgroundScheduler

from config import APP_TIMEZONE, FETCH_INTERVAL_MINUTES, WINDOW_END_HOUR, WINDOW_START_HOUR
from db import ensure_db
from services.rate_service import fetch_and_store_rate

logger = logging.getLogger(__name__)


def start_background_jobs() -> None:
    """Start the scheduler that runs the exchange-rate fetch loop."""
    ensure_db()

    # Run a first fetch immediately when the app starts. This satisfies the
    # requirement that the app begins collecting data as soon as it is launched.
    fetch_and_store_rate()

    scheduler = BackgroundScheduler(timezone=str(APP_TIMEZONE))
    scheduler.add_job(
        fetch_and_store_rate,
        "interval",
        minutes=FETCH_INTERVAL_MINUTES,
        id="kes_tzs_rate_collection",
    )

    scheduler.start()
    logger.info(
        "Exchange-rate scheduler started. Polling every %s minutes between %s:00 and %s:00 local time.",
        FETCH_INTERVAL_MINUTES,
        WINDOW_START_HOUR,
        WINDOW_END_HOUR,
    )
