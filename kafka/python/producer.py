from kafka import KafkaProducer
from kafka.errors import KafkaError

producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
print(producer)
for _ in range(50):
    future = producer.send('msg-rapida', b'some_message_bytes')
    try:
        record_metadata = future.get(timeout=10)
    except KafkaError as ex:
        print(ex)
        pass