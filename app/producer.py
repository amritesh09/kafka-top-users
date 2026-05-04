from kafka import KafkaProducer
import json, random
from config import BOOTSTRAP, TOPIC, SSL_CONFIG

producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP,
    **SSL_CONFIG,
    value_serializer=lambda v: json.dumps(v).encode()
)

users = [f"user{i}" for i in range(20)]

def generate_log(i):
    user = random.choice(users)
    action = random.choice(["click", "login", "scroll"])
    return user, f"{user} {action} {i}"

def send_events(n=1000):
    for i in range(n):
        user, log = generate_log(i)

        producer.send(
            TOPIC,
            key=user.encode(),  # 🔑 partition key
            value={"log": log}
        )

    producer.flush()
    print("Sent events")

if __name__ == "__main__":
    send_events()