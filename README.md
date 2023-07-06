

## 1. Run zookeper: 
/home/abhi/Kafka/kafka_2.12-2.3.0/bin/zookeeper-server-start.sh /home/abhi/Kafka/kafka_2.12-2.3.0/config/zookeeper.properties

## 2. Run Kafka-broker:
/home/abhi/Kafka/kafka_2.12-2.3.0/bin/kafka-server-start.sh /home/abhi/Kafka/kafka_2.12-2.3.0/config/server.properties

## 3. Ensure that you have topic created:
/home/abhi/Kafka/kafka_2.12-2.3.0/bin/kafka-topics.sh --list --bootstrap-server localhost:9092

## 4. Create Topic:
/home/abhi/Kafka/kafka_2.12-2.3.0/bin/kafka-topics.sh --create --topic iot --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

## 4. Make sure localip of windows is mapped to IP of WSL:
Listen on ipv4:             Connect to ipv4:

Address         Port        Address         Port
--------------- ----------  --------------- ----------
0.0.0.0         5000        172.22.54.196   5000

netsh interface portproxy add v4tov4 listenport=<port> listenaddress=<IP on windows> connectport=<port> connectaddress=<IP on WSL>
netsh interface portproxy add v4tov4 listenport=5000 listenaddress=0.0.0.0 connectport=5000 connectaddress=172.22.54.196

## 6. Run producer-flask app:
python3 /home/abhi/Projects/2/sensor-producer.py

## 7. Make sure you have keyspace and table created in Cassandra:
DESCRIBE KEYSPACES; //shows all the keyspaces
DROP KEYSPACE keyspace_name; //to drop keyspace

CREATE KEYSPACE iot
WITH replication = {
   'class': 'SimpleStrategy',
   'replication_factor': 1
};

CREATE TABLE IF NOT EXISTS iot.gyro (
    id BIGINT PRIMARY KEY,
    messageId BIGINT,
    sessionId TEXT,
    deviceId TEXT,
    name TEXT,
    x DOUBLE,
    y DOUBLE,
    z DOUBLE,
    accuracy DOUBLE,
    time BIGINT,
);

## 8. Run pyspark-app:

python3 /home/abhi/Projects/2/pyspark-process.py

## 9. Query Data saved in Cassandra:
SELECT count(*) FROM iot.gyro WHERE messageid = 2415 ALLOW FILTERING;
Select * from iot.gyro;