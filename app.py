import json
from flask import Flask, render_template, request, redirect, url_for, jsonify
import random
import os

app = Flask(__name__)
SETTINGS_FILE = "settings.json"

# Load settings from JSON or use defaults
if os.path.exists(SETTINGS_FILE):
    with open(SETTINGS_FILE, "r") as f:
        data = json.load(f)
        entries = data.get("entries", ["A major", "E major", "B major"])
        page_title = data.get("page_title", "Practice")
        refresh_interval = data.get("refresh_interval", 30)
        countdown_date = data.get("countdown_date", "2026-04-16T00:00:00")
else:
    entries = ["A major", "E major", "B major"]
    page_title = "Practice"
    refresh_interval = 30
    countdown_date = "2026-04-16T00:00:00"

# Helper to save settings
def save_settings():
    data = {
        "entries": entries,
        "page_title": page_title,
        "refresh_interval": refresh_interval,
        "countdown_date": countdown_date
    }
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route('/')
def index():
    return render_template(
        'index.html',
        page_title=page_title,
        entries=entries,
        refresh_interval=refresh_interval,
        countdown_date=countdown_date
    )

@app.route("/refresh")
def index_refresh():
    return render_template(
        "index.refresh.html",
        page_title=page_title,
        entries=entries,
        refresh_interval=refresh_interval,
        countdown_date=countdown_date
    )

@app.route('/random_entry', methods=['GET'])
def random_entry():
    entry = random.choice(entries)
    return jsonify(entry=entry)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    global entries, page_title, refresh_interval, countdown_date
    if request.method == 'POST':
        # Update entries
        new_entries = request.form.get('entries')
        if new_entries:
            entries = [e.strip() for e in new_entries.split(",")]

        # Update page title
        new_title = request.form.get('page_title')
        if new_title:
            page_title = new_title

        # Update refresh interval
        new_interval = request.form.get('refresh_interval')
        if new_interval and new_interval.isdigit():
            refresh_interval = int(new_interval)

        # Update countdown date
        new_countdown = request.form.get('countdown_date')
        if new_countdown:
            countdown_date = new_countdown

        # Save settings to JSON
        save_settings()

        return redirect(url_for('admin'))

    return render_template(
        'admin.html',
        entries=entries,
        page_title=page_title,
        refresh_interval=refresh_interval,
        countdown_date=countdown_date
    )

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5001,
 #       ssl_context=(
 #           "/home/xxxxxxxxx/certs/fullchain.pem",
 #           "/home/xxxxxxxxx/certs/privkey.pem"
 #       )
    )
