import json

from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

accounts = {}


@app.get("/")
def get():
    response = get_accounts(min_views=100000)
    return jsonify(response)


@app.post("/")
def post():
    items = get_items()

    for item in items:

        if not is_valid_item(item):
            continue

        if is_older_than_30_days(item):
            continue

        if is_slide_show(item):
            update_accounts(item)

    return None, 200


@app.post("/save")
def save():
    response = get_accounts()

    with open("accounts.json", "w") as f:
        json.dump(response, f, indent=2)

    return None, 200


def get_accounts(min_views=0):
    response = {}

    for account_id, data in accounts.items():
        if data["total_slideshow_views"] >= min_views:
            response[account_id] = {
                "total_slideshow_views": data["total_slideshow_views"],
                "slideshow_count": data["slideshow_count"],
                "last_updated": data["last_updated"]
            }

    return response


def get_items():
    payload = request.get_json()
    return payload.get("itemList", [])


def get_author_unique_id(item):
    try:
        return item.get("author", {}).get("uniqueId", None)
    except:
        return None


def get_created_time(item):
    try:
        return item.get("createTime", None)
    except:
        return None


def get_id(item):
    try:
        return item.get("id", None)
    except:
        return None


def get_views(item):
    try:
        stats = item.get("stats", {})
        views = stats.get("playCount", 0)
        return views
    except:
        return 0


def is_valid_item(item):
    author_unique_id = get_author_unique_id(item)
    create_time = get_created_time(item)
    item_id = get_id(item)

    if author_unique_id is None or create_time is None or item_id is None:
        return False

    return True


def is_older_than_30_days(item):
    create_time = get_created_time(item)
    create_datetime = datetime.fromtimestamp(create_time)
    return datetime.now() - create_datetime > timedelta(days=30)


def is_slide_show(item):
    try:
        return item.get("imagePost", False)
    except:
        return False


def update_accounts(item):
    views = get_views(item)

    author_unique_id = get_author_unique_id(item)

    if author_unique_id not in accounts:
        accounts[author_unique_id] = {
            "total_slideshow_views": 0,
            "slideshow_count": 0,
            "seen_items": set(),
            "last_updated": datetime.now().isoformat()
        }

    item_id = get_id(item)

    if item_id not in accounts[author_unique_id]["seen_items"]:
        accounts[author_unique_id]["total_slideshow_views"] += views
        accounts[author_unique_id]["slideshow_count"] += 1
        accounts[author_unique_id]["seen_items"].add(item_id)

    accounts[author_unique_id]["last_updated"] = datetime.now().isoformat()
