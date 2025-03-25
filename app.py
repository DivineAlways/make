from flask import Flask, request, jsonify
import time
import hmac
import hashlib

app = Flask(__name__)

@app.route('/sign', methods=['POST'])
def sign():
    # Read values from form data instead of JSON
    method = (request.form.get('method') or 'GET').upper()
    path = request.form.get('path') or '/trade/order'
    body = request.form.get('body') or ''
    api_key = request.form.get('apiKey')
    api_secret = request.form.get('apiSecret')
    passphrase = request.form.get('passphrase')

    # Generate current Unix timestamp (seconds)
    timestamp = str(int(time.time()))

    # Construct message: timestamp + method + path + body
    message = timestamp + method + path + body

    # HMAC SHA256 signature (hex)
    signature = hmac.new(
        api_secret.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    # Return the BloFin headers as JSON
    return jsonify({
        "ACCESS-KEY": api_key,
        "ACCESS-SIGN": signature,
        "ACCESS-TIMESTAMP": timestamp,
        "ACCESS-PASSPHRASE": passphrase,
        "Content-Type": "application/json"
    })

if __name__ == "__main__":
    import os
    port = int(os.environ.get('PORT', 8080))
    app.run(host="0.0.0.0", port=port)
