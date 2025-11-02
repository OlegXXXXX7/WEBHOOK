from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/webhook/tribute", methods=["GET", "POST"])
def tribute():
    if request.method == "GET":
        return "OK", 200
    payload = request.get_json(silent=True) or {}
    print("Webhook /tribute payload:", payload, flush=True)
    return jsonify(status="ok"), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)