from flask import Flask, jsonify, render_template, request

from config import APP_TIMEZONE, FETCH_INTERVAL_MINUTES
from db import ensure_db, get_history, get_latest_rate
from scheduler import start_background_jobs

# Create the Flask app instance. This is the main web server that will serve
# both the dashboard page and the JSON API endpoints used by the frontend.
app = Flask(__name__)

# Start the background scheduler as soon as the app loads. This ensures the app
# begins fetching exchange-rate data immediately on startup, then continues to poll
# every 10 minutes while the server is running.
start_background_jobs()


@app.route("/")
def index():
    """Serve the dashboard page for the KES/TZS exchange-rate tracker."""
    return render_template("index.html")


@app.route("/api/rates/latest")
def api_latest_rate():
    """Return the newest saved KES/TZS exchange rate as JSON."""
    record = get_latest_rate()
    if record is None:
        return jsonify({"error": "No exchange rate has been saved yet."}), 404

    return jsonify(
        {
            "base": record["base"],
            "target": record["target"],
            "rate": record["rate"],
            "fetched_at": record["fetched_at"],
            "timezone": str(APP_TIMEZONE),
        }
    )


@app.route("/api/rates/history")
def api_history():
    """Return recent exchange-rate snapshots stored in the local database."""
    try:
        limit = int(request.args.get("limit", 24))
    except ValueError:
        # If the user passes a non-numeric value, fall back to a sensible default.
        limit = 24

    # Keep the request bounded so the API stays predictable and lightweight.
    limit = max(1, min(limit, 200))
    history = get_history(limit)
    return jsonify({"count": len(history), "history": history})


@app.route("/api/health")
def health_check():
    """A simple health endpoint for quick readiness checks."""
    ensure_db()
    latest = get_latest_rate()
    return jsonify(
        {
            "status": "ok",
            "interval_minutes": FETCH_INTERVAL_MINUTES,
            "latest_rate": latest["rate"] if latest else None,
        }
    )


if __name__ == "__main__":
    # Run the app in local development mode. This is suitable for testing on a
    # machine and is simple to debug without extra web-server setup.
    app.run(host="0.0.0.0", port=5000, debug=False)
