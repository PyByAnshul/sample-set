from flask import Flask, request, jsonify, render_template
from smlib.twitter import post_twit
from smlib.instagram import post_scrapper
from smlib.ollama import caption_creater
from globals import db
import threading


app = Flask(__name__)

# Home route 
@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")

# Starts post scraping in a background thread
@app.route("/start_fetch_post", methods=["GET"])
def start_fetch_post():
    thread = threading.Thread(target=post_scrapper.main)
    thread.start()
    return "Post fetch started in the background."

# Generates a caption summary for a given post
@app.route("/get_caption", methods=["POST"])
def get_caption():
    data = request.json
    post_id = data.get("post_id")

    if not post_id:
        return jsonify({"status": "error", "message": "Post ID is required."}), 400

    try:
        summary = caption_creater.main(post_id)
        return jsonify(summary)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Fetches post data from the database
@app.route("/get-post-data", methods=["GET"])
def get_post_data():
    try:
        data = list(db.post.find({}, {'_id': 0}))  
        return jsonify(data)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Posts a tweet with a given caption
@app.route("/post-tweet", methods=["POST"])
def post_tweet():
    data = request.json
    caption = data.get("caption")

    if not caption:
        return jsonify({"status": "error", "message": "Caption is required."}), 400

    try:
        post_twit.main(caption)
        return jsonify({"status": "success", "message": "Tweet posted successfully."}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Starts the Flask app
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
