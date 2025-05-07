from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='grp3bigf.francecentral.cloudapp.azure.com:9092')

producer.send('hi', b'Hello from VS Code!')
producer.flush()
producer.close()