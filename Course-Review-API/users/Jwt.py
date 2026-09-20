import hashlib
import base64
import hmac
import json


with open("key.txt", "r", encoding="utf-8") as f:
    JWT_SECRET = f.read().strip()


def create_jwt(user_id, username):

    header = {
        "alg": "HS256",
        "typ": "JWT"
    }

    payload = {
        "user_id": user_id,
        "username": username
    }

    header_b64 = base64.urlsafe_b64encode( json.dumps(header).encode()).decode()

    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode() ).decode()

    message = f"{header_b64}.{payload_b64}"
    signature = hmac.new(JWT_SECRET.encode(),message.encode(), hashlib.sha256).hexdigest()

    return f"{message}.{signature}"


def decode_jwt(token):

    try:

        header_b64, payload_b64, signature = token.split(".")

        message = f"{header_b64}.{payload_b64}"

        expected_signature = hmac.new(JWT_SECRET.encode(), message.encode(), hashlib.sha256 ).hexdigest()

        if signature != expected_signature:
            return None

        payload_json = base64.urlsafe_b64decode(payload_b64).decode()

        payload = json.loads(payload_json)

        return payload

    except Exception:
        return None