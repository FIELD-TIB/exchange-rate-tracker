# This file holds the application-wide settings used by the exchange-rate tracker.
# Keeping configuration in one place makes the project easier to maintain and adjust.

import os
from zoneinfo import ZoneInfo

# East Africa time is the most relevant timezone for Kenyan and Tanzanian rates.
APP_TIMEZONE = ZoneInfo("Africa/Nairobi")

# The requirement says to poll every 10 minutes, so this value is fixed here.
FETCH_INTERVAL_MINUTES = 10

# We only collect rates during the business window requested by the user.
WINDOW_START_HOUR = 6
WINDOW_END_HOUR = 18

# This free public service is enough for a cost-free exchange-rate lookup.
# It returns currency conversion data without requiring an API key.
FRANKFURTER_URL = "https://api.frankfurter.app/latest"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "exchange_rates.db")
