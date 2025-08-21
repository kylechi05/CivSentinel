import os
import threading

from dotenv import load_dotenv
from confluent_kafka import Consumer, KafkaException

from predictions.predict import predict_crime_hotspots

load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))

def handle_ping():
    threading.Thread(target=predict_crime_hotspots).start()

def main():
    bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS')
    polling_freq = int(os.getenv('KAFKA_POLLING_FREQ'))
    topic = 'model-ping'

    consumer = Consumer({
        'bootstrap.servers': bootstrap_servers,
        'group.id': 'model-group',
        'auto.offset.reset': 'latest',
    })

    consumer.subscribe([topic])
    
    print(f"Listening for messages on topic '{topic}' every {polling_freq} seconds...")

    try:
        while True:
            msg = consumer.poll(timeout=polling_freq)

            if msg is None:
                print(f'No ping received in the last {polling_freq} seconds.')
                continue

            if msg.error():
                raise KafkaException(f"Error while consuming message: {msg.error()}")
            
            print(f'Received ping: {msg.value().decode("utf-8")}')
            handle_ping()

    except KeyboardInterrupt:
        print('Shutting down model prediction consumer...')
    finally:
        consumer.close()

if __name__ == '__main__':
    main()
    