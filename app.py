from flask import Flask, request
import requests

app = Flask(__name__)

POST_URL = "https://api.pushover.net/1/messages.json"

@app.route('/1/messages.json', methods=['POST'])
def bomb():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        body = request.json
        requests.post(POST_URL, json={
            "token": body["token"],
            "user": body["user"],
            "message": body["message"],
            "priority": body["priority"],
            "sound": body["sound"],
            "title": body["title"],
            "ttl": 3600
        })
        return {"status": "OK"}
    return {"status": "Error"}, 400

@app.route('/healthz')
def health():
    return "OK"

if __name__ == "__main__":
    app.run()
