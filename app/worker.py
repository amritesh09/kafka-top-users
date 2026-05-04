from kafka import KafkaConsumer
import json
from config import BOOTSTRAP, TOPIC, SSL_CONFIG

consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=BOOTSTRAP,
    group_id="workers",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    value_deserializer=lambda m: json.loads(m.decode()),
    **SSL_CONFIG
)

counts = {}

for msg in consumer:
    log = msg.value["log"]
    user = log.split()[0]

    counts[user] = counts.get(user, 0) + 1

    # print every 100 events
    if sum(counts.values()) % 100 == 0:
        top = sorted(counts.items(), key=lambda x: -x[1])[:5]
        print("Top users:", top)