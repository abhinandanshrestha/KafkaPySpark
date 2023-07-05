from pyspark.streaming import StreamingContext
from pyspark.sql import SparkSession
# from pyspark.sql.functions import from_json,lit
from pyspark.sql.functions import col,from_json,explode
from pyspark.sql.types import DoubleType,StringType,IntegerType,StructField,StructType,LongType,ArrayType

# Define my scala and spark version
scala_version = '2.12'
spark_version = '3.4.1'

# TODO: Ensure match above values match the correct versions
packages = [
    f'org.apache.spark:spark-sql-kafka-0-10_{scala_version}:{spark_version}',
    'org.apache.kafka:kafka-clients:3.2.1'
    #  'com.datastax.spark:spark-cassandra-connector_2.12:3.1.0'
]

spark = SparkSession.builder \
    .master("local[*]") \
    .appName("KafkaIntegrationApp") \
    .config("spark.jars.packages", ",".join(packages))\
    .getOrCreate()
# Modified JSON data
json_data = '''
{
    "messageId": 130,
    "sessionId": "3f94b299-ade7-4d26-9bff-bb928ec1f0a3",
    "deviceId": "e6e9008c-993f-4592-b31f-728d1332ff32",
    "payload": [
        {
            "name": "gyroscope",
            "values": {
                "x": 0.00000000029,
                "y": -0.000000000123,
                "z": -0.0000000123
            },
            "accuracy": 3,
            "time": 1688465302192565500
        },
        {
            "name": "gyroscope",
            "values": {
                "x": 0.00000000029,
                "y": -0.000000000123,
                "z": -0.0000000123
            },
            "accuracy": 3,
            "time": 1688465302312532700
        },
        {
            "name": "gyroscope",
            "values": {
                "x": 0.00000000029,
                "y": -0.000000000123,
                "z": -0.0000000123
            },
            "accuracy": 3,
            "time": 1688465302312532700
        },
        {
            "name": "gyroscope",
            "values": {
                "x": 0.00000000029,
                "y": -0.000000000123,
                "z": -0.0000000123
            },
            "accuracy": 3,
            "time": 1688465302312532700
        }
    ]
}
'''

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

# Convert the JSON data to DataFrame
df = spark.createDataFrame([(json_data,)], ["value"])
df = df.select(from_json(col("value"), schema).alias("data")).select("data.*")

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

# Print the DataFrame
df.printSchema()
df.show(truncate=False)
