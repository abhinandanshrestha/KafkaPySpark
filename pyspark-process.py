from pyspark.streaming import StreamingContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json,explode,lit,monotonically_increasing_id,col
from pyspark.sql.types import DoubleType,StringType,StructField,StructType,LongType,ArrayType


# Define my scala and spark version
scala_version = '2.12'
spark_version = '3.4.1'

# TODO: Ensure match above values match the correct versions
packages = [
    f'org.apache.spark:spark-sql-kafka-0-10_{scala_version}:{spark_version}',
    'org.apache.kafka:kafka-clients:3.2.1',
     'com.datastax.spark:spark-cassandra-connector_2.12:3.1.0'
]

spark = SparkSession.builder \
    .master("local[*]") \
    .appName("KafkaIntegrationApp") \
    .config("spark.jars.packages", ",".join(packages))\
    .config("spark.cassandra.connection.host", "localhost") \
    .config("spark.cassandra.connection.port", "9042") \
    .config("spark.sql.extensions", "com.datastax.spark.connector.CassandraSparkExtensions") \
    .getOrCreate()
    

# Create a StreamingContext with a batch interval (e.g., 1 second)
ssc = StreamingContext(spark.sparkContext, 1)

# Define the kafka topic and bootstrap servers
kafka_topic = "iot"
kafka_bootstrap_servers = "localhost:9092"

# Read from Kafka using the readStream API
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
    .option("subscribe", kafka_topic) \
    .option("startingOffsets", "latest") \
    .load()

# Convert the value column from Kafka to string and apply the schema
df = df.selectExpr("CAST(value AS STRING)")

# Define the schema for your data
schema = StructType([
    StructField("messageId", LongType(), nullable=True),
    StructField("sessionId", StringType(), nullable=True),
    StructField("deviceId", StringType(), nullable=True),
    StructField("payload", ArrayType(StructType([
        StructField("name", StringType(), nullable=True),
        StructField("values", StructType([
            StructField("x", DoubleType(), nullable=True),
            StructField("y", DoubleType(), nullable=True),
            StructField("z", DoubleType(), nullable=True)
        ]), nullable=True),
        StructField("accuracy", DoubleType(), nullable=True),
        StructField("time", LongType(), nullable=True)
    ])), nullable=True)
])

# Apply the schema to the DataFrame
df = df.select(from_json(df.value, schema).alias("data")).select("data.*")

# Explode the payload array to create separate rows for each gyroscope value
df = df.select("messageId", "sessionId", "deviceId", explode("payload").alias("payload"))

# Select the individual gyroscope columns and flatten the nested values struct
df = df.select(
    "messageId",
    "sessionId",
    "deviceId",
    "payload.name",
    "payload.values.x",
    "payload.values.y",
    "payload.values.z",
    "payload.accuracy",
    "payload.time"
)

df = df.withColumnRenamed("messageId", "messageid")
df = df.withColumnRenamed("sessionId", "sessionid")
df = df.withColumnRenamed("deviceId", "deviceid")

# Specify the Cassandra keyspace and table
cassandra_keyspace = "iot"
cassandra_table = "gyro"


# Save the processed data to Cassandra
def save_to_cassandra(batch_df, batch_id):
    # Add the primary key column to the DataFrame
    batch_df_with_key = batch_df.withColumn("id", lit(batch_id) + monotonically_increasing_id())

    batch_df_with_key.write \
        .format("org.apache.spark.sql.cassandra") \
        .mode("append") \
        .options(table="gyro", keyspace="iot") \
        .save()

# Write the streaming data to Cassandra
query = df.writeStream \
    .format("org.apache.spark.sql.cassandra") \
    .option("keyspace", cassandra_keyspace) \
    .option("table", cassandra_table) \
    .option("checkpointLocation", "/home/abhi/Projects/2/cheeckpoint") \
    .foreachBatch(save_to_cassandra) \
    .start()

# Print the data to the console
# query = df.writeStream \
#     .outputMode("append") \
#     .format("console") \
#     .start()

query.awaitTermination()