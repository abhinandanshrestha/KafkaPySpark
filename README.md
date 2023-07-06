
![Overview](https://github.com/abhinandanshrestha/KafkaPySpark/assets/43780258/c0eb1b08-d1bf-4d84-8999-430c026fbdda)
<p align="center">
  <img src="https://github.com/abhinandanshrestha/KafkaPySpark/assets/43780258/05ad74fe-7dd4-4d19-b860-5bcf667abb9f" alt="image1" width="400" />
  <img src="https://github.com/abhinandanshrestha/KafkaPySpark/assets/43780258/cd513496-0313-4be3-b0b7-286c1f3542bc" alt="image2" width="400" />
</p>


## 1. Run zookeper: 
/home/abhi/Kafka/kafka_2.12-2.3.0/bin/zookeeper-server-start.sh /home/abhi/Kafka/kafka_2.12-2.3.0/config/zookeeper.properties

## 2. Run Kafka-broker:
/home/abhi/Kafka/kafka_2.12-2.3.0/bin/kafka-server-start.sh /home/abhi/Kafka/kafka_2.12-2.3.0/config/server.properties

## 3. Ensure that you have topic created:
/home/abhi/Kafka/kafka_2.12-2.3.0/bin/kafka-topics.sh --list --bootstrap-server localhost:9092

## 4. Create Topic:
/home/abhi/Kafka/kafka_2.12-2.3.0/bin/kafka-topics.sh --create --topic iot --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

## 4. Make sure localip of windows is mapped to IP of WSL. Also make sure you enter IP of Windows in the Sensor Logger:
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
