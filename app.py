from flask import Flask, request
import requests
import logging
import os

app = Flask(__name__)

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

POST_URL = "https://api.pushover.net/1/messages.json"
USER_KEY = os.environ["PUSHOVER_USER_KEY"]
TOKEN = os.environ["PUSHOVER_TOKEN"]

@app.route('/', methods=['POST'])
def webhook():
    content_type = request.headers.get('Content-Type')
    if (content_type != 'application/json'):
        return {"status": "Error"}, 400

    body = request.json
    if body["status"] != "firing":
        return {"status": "NOOP"}

    app.logger.info(body)
    requests.post(POST_URL, json={
        "token": TOKEN,
        "user": USER_KEY,
        "message": str(body["groupLabels"]),
        "priority": 0,
        "title": body["groupKey"],
        "ttl": 3600
    })

    return {"status": "OK"}

@app.route('/healthz')
def health():
    return "OK"

if __name__ == "__main__":
    app.run()
