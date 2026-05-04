import os
from dotenv import load_dotenv

load_dotenv()

BOOTSTRAP = os.getenv("BOOTSTRAP_SERVER")
TOPIC = os.getenv("TOPIC")

SSL_CONFIG = {
    "security_protocol": "SSL",
    "ssl_cafile": "certs/ca.pem",
    "ssl_certfile": "certs/service.cert",
    "ssl_keyfile": "certs/service.key",
}