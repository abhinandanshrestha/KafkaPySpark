Run zookeper: 
/home/abhi/Kafka/kafka_2.12-2.3.0/bin/zookeeper-server-start.sh /home/abhi/Kafka/kafka_2.12-2.3.0/config/zookeeper.properties

Run Kafka-broker:
/home/abhi/Kafka/kafka_2.12-2.3.0/bin/kafka-server-start.sh /home/abhi/Kafka/kafka_2.12-2.3.0/config/server.properties

Ensure that you have topic created:
/home/abhi/Kafka/kafka_2.12-2.3.0/bin/kafka-topics.sh --list --bootstrap-server localhost:9092

Create Topic:
/home/abhi/Kafka/kafka_2.12-2.3.0/bin/kafka-topics.sh --create --topic iot --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

Run producer-flask app:
python3 /home/abhi/Projects/2/pyspark-process.py

Run pyspark-app:
python3 /home/abhi/Projects/2/sensor-producer.py
