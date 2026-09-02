from flask import Flask, request, jsonify

app = Flask(__name__)

POST = ["POST"]


@app.route("/", methods=POST)
def process_tiktok_videos():
    total_views = 0
    payload = request.get_json()
    items = payload.get("itemList", [])

    for item in items:
        stats = item.get("stats", {})
        views = stats.get("playCount", 0)
        total_views += views

    response = { "total_views": total_views }
    print(response)
    return jsonify(response)
