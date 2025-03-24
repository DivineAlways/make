from flask import Flask, request, jsonify
import time, hmac, hashlib

app = Flask(__name__)

@app.route('/sign', methods=['POST'])
def sign():
    data = request.json
    method = data.get('method', 'GET').upper()
    path = data.get('path', '/trade/order')
    body = data.get('body', '')
    api_key = data.get('apiKey')
    api_secret = data.get('apiSecret')
    passphrase = data.get('passphrase')

    timestamp = str(int(time.time()))
    message = timestamp + method + path + body
    signature = hmac.new(
        api_secret.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    return jsonify({
        "ACCESS-KEY": api_key,
        "ACCESS-SIGN": signature,
        "ACCESS-TIMESTAMP": timestamp,
        "ACCESS-PASSPHRASE": passphrase,
        "Content-Type": "application/json"
    })

if __name__ == "__main__":
    # On Render/Replit, the PORT is usually provided as an env var.
    # For local testing, default to 8080.
    import os
    port = int(os.environ.get('PORT', 8080))
    app.run(host="0.0.0.0", port=port)
