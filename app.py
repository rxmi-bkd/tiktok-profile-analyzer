from flask import Flask, request, jsonify

app = Flask(__name__)

POST = ["POST"]


@app.route("/", methods=POST)
def process_tiktok_videos():
    videos = request.get_json()
    print(videos)
    ...
    return jsonify({})
