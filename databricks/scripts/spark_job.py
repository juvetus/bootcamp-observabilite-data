from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, count, max
import os
import time
import uuid
from datadog import initialize, statsd
from dotenv import load_dotenv
import logging

# Configuration Datadog
load_dotenv()

options = {
    'api_key': os.getenv('DD_API_KEY', 'b9aeda243419af4396e5f7fb40273c78'),
    'app_key': os.getenv('DD_APP_KEY', ''),
    'statsd_host': os.getenv('DD_AGENT_HOST', 'dd-agent'),
    'statsd_port': int(os.getenv('DD_DOGSTATSD_PORT', 8125))
}

initialize(**options)

# Génération execution_id pour corrélation
execution_id = str(uuid.uuid4())
env = os.getenv('ENV', 'dev')

# Tags communs
COMMON_TAGS = [
    f'service:spark-job',
    f'env:{env}',
    f'execution_id:{execution_id}',
    'job:truck_telemetry'
]

# Logger
logging.basicConfig(
    level=logging.INFO,
    format=f'%(asctime)s - [execution_id:{execution_id}] - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

logger.info(f"Starting Spark job - execution_id: {execution_id}")
start_time = time.time()

spark = SparkSession.builder \
    .appName("TruckTelemetryJob") \
    .master("local[*]") \
    .config("spark.driver.host", "localhost") \
    .getOrCreate()

# Chemins absolus
data_path = "/app/data/input/truck_data.csv"
output_path = "/app/data/output/truck_metrics"

# Lecture
logger.info(f"Reading data from: {data_path}")
statsd.increment('spark.job.start', tags=COMMON_TAGS)

df = spark.read.option("header", True).csv(data_path)
raw_count = df.count()

logger.info(f"Raw data loaded: {raw_count} records")
statsd.gauge('spark.records.raw', raw_count, tags=COMMON_TAGS)

print("=== Raw data ===")
df.show(truncate=False)

# Cast des types
typed_df = df \
    .withColumn("speed", col("speed").cast("int")) \
    .withColumn("consumption", col("consumption").cast("int")) \
    .withColumn("fuel_level", col("fuel_level").cast("int")) \
    .withColumn("engine_temp", col("engine_temp").cast("int")) \
    .withColumn("location_lat", col("location_lat").cast("double")) \
    .withColumn("location_lon", col("location_lon").cast("double"))

# Nettoyage métier
logger.info("Applying data quality filters")
clean_df = typed_df \
    .filter((col("speed") > 0) & (col("speed") <= 120)) \
    .filter((col("engine_temp") > 0) & (col("engine_temp") <= 120)) \
    .filter(col("fuel_level") >= 0)

clean_count = clean_df.count()
filtered_count = raw_count - clean_count

logger.info(f"Data cleaned: {clean_count} valid records, {filtered_count} filtered")
statsd.gauge('spark.records.clean', clean_count, tags=COMMON_TAGS)
statsd.gauge('spark.records.filtered', filtered_count, tags=COMMON_TAGS)

if filtered_count > 0:
    quality_rate = (clean_count / raw_count) * 100
    statsd.gauge('spark.data.quality_rate', quality_rate, tags=COMMON_TAGS)
    logger.info(f"Data quality rate: {quality_rate:.2f}%")

print("=== Clean data ===")
clean_df.show(truncate=False)

# Agrégations utiles métier
logger.info("Computing aggregations by vehicle_id")
agg_df = clean_df.groupBy("vehicle_id").agg(
    avg("speed").alias("avg_speed"),
    avg("consumption").alias("avg_consumption"),
    avg("fuel_level").alias("avg_fuel_level"),
    max("engine_temp").alias("max_engine_temp"),
    count("*").alias("nb_events")
)

agg_count = agg_df.count()
logger.info(f"Aggregations completed: {agg_count} vehicles processed")
statsd.gauge('spark.vehicles.processed', agg_count, tags=COMMON_TAGS)

print("=== Aggregated metrics ===")
agg_df.show(truncate=False)

# Écriture (zone curated)
logger.info(f"Writing output to: {output_path}")
agg_df.write.mode("overwrite").parquet(output_path)

end_time = time.time()
duration = end_time - start_time

logger.info(f"✅ Job completed successfully in {duration:.2f}s")
logger.info(f"Output saved to {output_path}")

# Métriques finales
statsd.gauge('spark.job.duration', duration, tags=COMMON_TAGS)
statsd.increment('spark.job.success', tags=COMMON_TAGS)

throughput = raw_count / duration if duration > 0 else 0
statsd.gauge('spark.job.throughput', throughput, tags=COMMON_TAGS)

logger.info(f"Performance: {throughput:.2f} records/second")
logger.info(f"Execution ID: {execution_id}")

print(f"✅ Output saved to {output_path}")

spark.stop()
