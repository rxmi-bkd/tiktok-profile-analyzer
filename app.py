import json

from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

accounts = {}

# Account field constants
TOTAL_SLIDESHOW_VIEWS = "total_slideshow_views"
SLIDESHOW_COUNT = "slideshow_count"
SEEN_ITEMS = "seen_items"
LAST_UPDATED = "last_updated"

# Item field constants
ITEM_LIST = "itemList"
AUTHOR = "author"
UNIQUE_ID = "uniqueId"
CREATE_TIME = "createTime"
ITEM_ID = "id"
STATS = "stats"
PLAY_COUNT = "playCount"
IMAGE_POST = "imagePost"


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
        if data[TOTAL_SLIDESHOW_VIEWS] >= min_views:
            response[account_id] = {
                TOTAL_SLIDESHOW_VIEWS: data[TOTAL_SLIDESHOW_VIEWS],
                SLIDESHOW_COUNT: data[SLIDESHOW_COUNT],
                LAST_UPDATED: data[LAST_UPDATED]
            }

    return response


def get_items():
    payload = request.get_json()
    return payload.get(ITEM_LIST, [])


def get_author_unique_id(item):
    try:
        return item.get(AUTHOR, {}).get(UNIQUE_ID, None)
    except:
        return None


def get_created_time(item):
    try:
        return item.get(CREATE_TIME, None)
    except:
        return None


def get_id(item):
    try:
        return item.get(ITEM_ID, None)
    except:
        return None


def get_views(item):
    try:
        stats = item.get(STATS, {})
        views = stats.get(PLAY_COUNT, 0)
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
        return item.get(IMAGE_POST, False)
    except:
        return False


def update_accounts(item):
    views = get_views(item)

    author_unique_id = get_author_unique_id(item)

    if author_unique_id not in accounts:
        accounts[author_unique_id] = {
            TOTAL_SLIDESHOW_VIEWS: 0,
            SLIDESHOW_COUNT: 0,
            SEEN_ITEMS: set(),
            LAST_UPDATED: datetime.now().isoformat()
        }

    item_id = get_id(item)

    if item_id not in accounts[author_unique_id][SEEN_ITEMS]:
        accounts[author_unique_id][TOTAL_SLIDESHOW_VIEWS] += views
        accounts[author_unique_id][SLIDESHOW_COUNT] += 1
        accounts[author_unique_id][SEEN_ITEMS].add(item_id)

    accounts[author_unique_id][LAST_UPDATED] = datetime.now().isoformat()
