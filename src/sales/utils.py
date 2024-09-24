import hmac
import hashlib
import base64

import random
import string

import hashlib
import hmac
import base64
from datetime import datetime


def generate_hmac_sha256(message: str, secret: str) -> str:
    message_bytes = message.encode("utf-8")
    secret_bytes = secret.encode("utf-8")
    s = hmac.new(secret_bytes, message_bytes, hashlib.sha256).digest()
    return base64.b64encode(s).decode("utf-8")


def generate_random_product_code() -> str:
    random_string = "".join(random.choices(string.ascii_letters + string.digits, k=8))
    current_time = datetime.now()
    formatted_time = (
        current_time.strftime("%y%m%d") + "-" + current_time.strftime("%H%M%S")
    )
    return f"{str(random_string)}-{formatted_time}"


def generate_signature(total_amount: str, product_code: str, secret: str) -> None: ...
