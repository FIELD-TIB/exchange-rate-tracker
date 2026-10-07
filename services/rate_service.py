# This file is responsible for fetching the live exchange rate and saving it.
# The logic is intentionally small and clean so the project stays easy to follow.

import logging
from datetime import datetime

import requests

from config import APP_TIMEZONE, EXCHANGE_RATE_API_URL, WINDOW_END_HOUR, WINDOW_START_HOUR
from db import ensure_db, save_rate

logger = logging.getLogger(__name__)


def fetch_kes_tzs_rate() -> float:
    """Fetch the latest KES/TZS conversion rate using a free public API."""
    response = requests.get(EXCHANGE_RATE_API_URL, timeout=10)
    response.raise_for_status()

    payload = response.json()
    if payload.get("result") != "success":
        raise ValueError("Open Exchange Rates API did not return success.")

    rates = payload.get("rates", {})
    if "TZS" not in rates:
        raise ValueError("KES/TZS rate not available from the API.")

    rate = float(rates["TZS"])
    return rate


def fetch_and_store_rate() -> None:
    """Only store a new rate if the current time falls within the requested window."""
    ensure_db()

    now = datetime.now(APP_TIMEZONE)

    # The requirement says the app should collect data only from 06:00 to 18:00.
    # If outside that window, we skip this fetch and do not save anything.
    if not (WINDOW_START_HOUR <= now.hour < WINDOW_END_HOUR):
        logger.info("Skipping rate fetch outside the 06:00-18:00 window.")
        return

    try:
        rate = fetch_kes_tzs_rate()
        fetched_at = now.isoformat()
        save_rate("KES", "TZS", rate, fetched_at)
        logger.info("Saved KES/TZS rate at %s: %s", fetched_at, rate)
    except Exception as exc:  # pragma: no cover - used for runtime logging only.
        logger.warning("Failed to fetch KES/TZS rate: %s", exc)
