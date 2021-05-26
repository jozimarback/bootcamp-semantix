from kafka import KafkaConsumer

consumer = KafkaConsumer('msg-rapida',bootstrap_servers=['localhost:9092'])
for msg in consumer:
    print (msg)