import pyspark
import os
from dotenv import load_dotenv
from pathlib import Path

from pyspark.sql.functions import (
    from_json, col, sum, window, count,
    date_format, current_timestamp, expr, when, avg,
    approxCountDistinct as countDistinct, round as round_
)
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, LongType, TimestampType

dotenv_path = Path("/opt/app/.env")
load_dotenv(dotenv_path=dotenv_path)

spark_hostname = os.getenv("SPARK_MASTER_HOST_NAME")
spark_port = os.getenv("SPARK_MASTER_PORT")
kafka_host = os.getenv("KAFKA_HOST")
kafka_topic = os.getenv("KAFKA_TOPIC_NAME")

spark_host = f"spark://{spark_hostname}:{spark_port}"

os.environ["PYSPARK_SUBMIT_ARGS"] = (
    "--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2 org.postgresql:postgresql:42.2.18"
)

# Initialize Spark Session
spark = (
    pyspark.sql.SparkSession.builder.appName("FurnitureStoreAnalytics")
    .master(spark_host)
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0")
    .config("spark.sql.shuffle.partitions", 4)
    .config("spark.sql.streaming.forceDeleteTempCheckpointLocation", True)
    .getOrCreate()
)

spark.sparkContext.setLogLevel("WARN")

# Schema matching the producer's data structure
schema = StructType([
    StructField("order_id", StringType(), True),
    StructField("customer_id", IntegerType(), True),
    StructField("furniture", StringType(), True),
    StructField("color", StringType(), True),
    StructField("price", IntegerType(), True),
    StructField("ts", LongType(), True),
])

# Read from Kafka
stream_df = (
    spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", f"{kafka_host}:9092")
    .option("subscribe", kafka_topic)
    .option("startingOffsets", "latest")
    .load()
)

# Parse JSON data
parsed_df = (
    stream_df.selectExpr("CAST(value AS STRING)")
    .select(from_json(col("value"), schema).alias("data"))
    .select("data.*")
)

# Convert timestamp and add price ranges
parsed_df = (
    parsed_df
    .withColumn("event_timestamp", (col("ts") / 1000).cast(TimestampType()))
    .withColumn(
        "price_category",
        when(col("price") <= 1000, "Budget")
        .when(col("price") <= 5000, "Mid-Range")
        .when(col("price") <= 10000, "Premium")
        .otherwise("Luxury")
    )
)

# 1. Real-time Sales Dashboard (5-minute windows)
sales_dashboard = (
    parsed_df
    .withWatermark("event_timestamp", "5 minutes")
    .groupBy(window("event_timestamp", "5 minutes"))
    .agg(
        count("order_id").alias("order_count"),
        sum("price").alias("total_revenue"),
        round_(avg("price"), 2).alias("avg_order_value"),
        countDistinct("customer_id").alias("unique_customers")
    )
    .select(
        date_format(col("window.start"), "yyyy-MM-dd HH:mm:ss").alias("period_start"),
        col("order_count"),
        col("total_revenue"),
        col("avg_order_value"),
        col("unique_customers")
    )
)

# 2. Product Performance Analysis
product_analysis = (
    parsed_df
    .withWatermark("event_timestamp", "5 minutes")
    .groupBy(
        window("event_timestamp", "5 minutes"),
        "furniture"
    )
    .agg(
        count("order_id").alias("units_sold"),
        sum("price").alias("revenue"),
        round_(avg("price"), 2).alias("avg_price"),
        countDistinct("customer_id").alias("unique_buyers")
    )
    .orderBy(col("revenue").desc())
)

# 3. Color Trends by Furniture Type
color_trends = (
    parsed_df
    .withWatermark("event_timestamp", "5 minutes")
    .groupBy(
        window("event_timestamp", "5 minutes"),
        "furniture",
        "color"
    )
    .agg(
        count("*").alias("sales_count"),
        sum("price").alias("revenue")
    )
    .orderBy(
        col("window").desc(),
        col("sales_count").desc()
    )
)

# Print headers for better readability
print("\n=== Real-time Furniture Store Analytics ===\n")

# Write sales dashboard to console
query_sales = (
    sales_dashboard.writeStream
    .outputMode("complete")
    .format("console")
    .option("truncate", False)
    .trigger(processingTime="10 seconds")
    .option("checkpointLocation", "/tmp/checkpoint/sales")
    .start()
)

# Write product analysis to console
query_products = (
    product_analysis.writeStream
    .outputMode("complete")
    .format("console")
    .option("truncate", False)
    .trigger(processingTime="10 seconds")
    .option("checkpointLocation", "/tmp/checkpoint/products")
    .start()
)

# Write color trends to console
query_colors = (
    color_trends.writeStream
    .outputMode("complete")
    .format("console")
    .option("truncate", False)
    .trigger(processingTime="10 seconds")
    .option("checkpointLocation", "/tmp/checkpoint/colors")
    .start()
)

# Wait for termination
spark.streams.awaitAnyTermination()
