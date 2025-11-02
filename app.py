from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

def notify_telegram(chat_id: str, text: str) -> bool:
    if not BOT_TOKEN or not chat_id:
        return False
    try:
        r = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id": chat_id, "text": text},
            timeout=8,
        )
        print("Telegram API:", r.status_code, r.text, flush=True)
        return r.ok
    except Exception as e:
        print("Telegram error:", e, flush=True)
        return False

@app.route("/webhook/tribute", methods=["GET", "POST"])
def tribute():
    if request.method == "GET":
        return "OK", 200

    payload = request.get_json(silent=True) or {}
    print("Webhook /tribute payload:", payload, flush=True)

    # Достаём telegram_id и продукт
    purchase = payload.get("purchase") or {}
    metadata = purchase.get("metadata") or {}
    telegram_id = metadata.get("telegram_id") or metadata.get("tg_id")

    product = (
        purchase.get("product_id")
        or purchase.get("product")
        or (payload.get("product") or {}).get("id")
        or (payload.get("product") or {}).get("handle")
        or (payload.get("product") or {}).get("name")
    )

    if telegram_id:
        notify_telegram(
            str(telegram_id),
            f"Оплата получена. Доступ активирован. Продукт: {product or 'unknown'}",
        )
    else:
        print("telegram_id не найден в payload.metadata — передавай telegram_id в metadata при покупке", flush=True)

    return jsonify(status="ok"), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)