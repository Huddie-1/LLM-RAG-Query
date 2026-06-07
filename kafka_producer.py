# backend/kafka_producer.py

from kafka import KafkaProducer
import json
import os

KAFKA_BROKER_URL = os.getenv("KAFKA_BROKER_URL", "localhost:9092")
TOPIC_NAME = os.getenv("KAFKA_TOPIC", "query-events")

# Create a global Kafka producer instance
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER_URL,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

def send_event_to_kafka(event: dict):
    """
    Send a JSON-serializable event to Kafka topic.
    """
    try:
        producer.send(TOPIC_NAME, event)
        producer.flush()
        print(f"[Kafka] Sent event to {TOPIC_NAME}")
    except Exception as e:
        print(f"[Kafka Error] {e}")
