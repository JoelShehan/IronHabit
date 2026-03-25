import json
import os
from datetime import datetime

DATA_FILE = "data/gym_data.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return {"history": {}, "streak": 0, "last_date": None}

    try:
        with open(DATA_FILE, "r") as f:
            content = f.read().strip()
            if not content:
                raise ValueError("Empty file")
            return json.loads(content)
    except:
        return {"history": {}, "streak": 0, "last_date": None}


def save_data(data):
    json.dump(data, open(DATA_FILE, "w"), indent=4)


def mark_went(image_path):
    data = load_data()
    today = datetime.now().date().isoformat()

    data["history"][today] = {
        "status": "went",
        "image": image_path
    }

    # streak logic
    if data["last_date"]:
        last = datetime.fromisoformat(data["last_date"]).date()
        if (datetime.now().date() - last).days == 1:
            data["streak"] += 1
        else:
            data["streak"] = 1
    else:
        data["streak"] = 1

    data["last_date"] = today
    save_data(data)


def mark_missed():
    data = load_data()
    today = datetime.now().date().isoformat()

    data["history"][today] = {"status": "missed"}
    data["streak"] = 0

    save_data(data)