# This project stores exchange-rate snapshots in a local SQLite database.
# It polls a free public exchange-rate API and displays the latest values on a simple dashboard.

## What this app does
- Retrieves the KES/TZS exchange rate from a free public provider.
- Runs the fetch every 10 minutes while the app is active.
- Only collects data between 06:00 and 18:00 in Africa/Nairobi time.
- Saves each rate to a local SQLite database.
- Exposes a small API and a front-end dashboard.

## Free-tier setup
This app uses:
- Flask for the web API and frontend
- SQLite for local storage
- Frankfurter API as a free exchange-rate data source

## Run it locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then open: http://localhost:5000

## API endpoints
- `GET /api/rates/latest` - returns the newest rate
- `GET /api/rates/history?limit=24` - returns recent rate history
- `GET /api/health` - basic app health check

## Notes
- The app only fetches within the configured trading window: 06:00 to 18:00.
- The scheduler begins when the app starts, so the first fetch happens immediately.
- Data is stored locally, so there is no external database dependency.
