from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

accounts = {}


@app.get("/")
def get_accounts():
    result = {}

    for account_id, data in accounts.items():
        result[account_id] = {
            "total_slideshow_views": data["total_slideshow_views"],
            "slideshow_count": data["slideshow_count"],
            "last_updated": data["last_updated"]
        }

    return jsonify(result)


@app.post("/")
def process_tiktok_response():
    items = get_items()
    now = datetime.now()

    for item in items:
        author_unique_id = get_author_unique_id(item)
        create_time = get_created_time(item)
        item_id = get_id(item)

        if author_unique_id is None or create_time is None or item_id is None:
            continue

        create_datetime = datetime.fromtimestamp(create_time)

        if create_datetime < now - timedelta(days=30):
            continue

        if is_slide_show(item):
            views = get_views(item)

            if author_unique_id not in accounts:
                accounts[author_unique_id] = {
                    "total_slideshow_views": 0,
                    "slideshow_count": 0,
                    "seen_items": set(),
                    "last_updated": now.isoformat()
                }

            if item_id not in accounts[author_unique_id]["seen_items"]:
                accounts[author_unique_id]["total_slideshow_views"] += views
                accounts[author_unique_id]["slideshow_count"] += 1
                accounts[author_unique_id]["seen_items"].add(item_id)

            accounts[author_unique_id]["last_updated"] = now.isoformat()

    return "ok", 200


def get_items():
    payload = request.get_json()
    return payload.get("itemList", [])


def get_id(item):
    try:
        return item.get("id", None)
    except:
        return None


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


def is_slide_show(item):
    try:
        return item.get("imagePost", False)
    except:
        return False


def get_views(item):
    try:
        stats = item.get("stats", {})
        views = stats.get("playCount", 0)
        return views
    except:
        return 0
