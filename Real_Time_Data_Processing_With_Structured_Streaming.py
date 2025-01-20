## Install required packages (only for local environments)
!pip install pyspark==3.1.2 -q
!pip install findspark -q

# Suppress warnings
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn
warnings.filterwarnings('ignore')

# Initialize FindSpark to simplify using Apache Spark with Python
import findspark
findspark.init()

# Import necessary modules
from pyspark.sql import SparkSession
from pyspark.sql.functions import expr, rand, when

# Initialize the Spark session
spark = SparkSession.builder \
    .appName("Smart Building HVAC Monitoring") \
    .getOrCreate()

### Simulate real-time sensor data
# Using Spark's `rate` source, generate continuous rows of data at 5 rows/second
sensor_data = spark.readStream.format("rate").option("rowsPerSecond", 5).load() \
    .withColumn("room_id", expr("CAST(value % 10 AS STRING)")) \
    .withColumn("temperature", when(expr("value % 10 == 0"), 15)  # Temperature = 15 for specific records
                .otherwise(20 + rand() * 25)) \
    .withColumn("humidity", expr("40 + rand() * 30"))

# Create a temporary SQL view for the simulated data
sensor_data.createOrReplaceTempView("sensor_table")

### Define SQL queries for analysis

# Detect rooms with critical temperatures (less than 18°C or greater than 60°C)
critical_temperature_query = """
    SELECT 
        room_id, 
        temperature, 
        humidity, 
        timestamp 
    FROM sensor_table 
    WHERE temperature < 18 OR temperature > 60
"""

# Calculate average temperature and humidity over a 1-minute window
average_readings_query = """
    SELECT 
        room_id, 
        AVG(temperature) AS avg_temperature, 
        AVG(humidity) AS avg_humidity, 
        window.start AS window_start 
    FROM sensor_table
    GROUP BY room_id, window(timestamp, '1 minute')
"""

# Identify rooms needing attention based on humidity thresholds (<45% or >75%)
attention_needed_query = """
    SELECT 
        room_id, 
        COUNT(*) AS critical_readings 
    FROM sensor_table 
    WHERE humidity < 45 OR humidity > 75
    GROUP BY room_id
"""

### Execute SQL queries to create streaming DataFrames

# Execute critical temperature query
critical_temperatures_stream = spark.sql(critical_temperature_query)

# Execute average readings query
average_readings_stream = spark.sql(average_readings_query)

# Execute attention needed query
attention_needed_stream = spark.sql(attention_needed_query)

### Output the results to the console

# Display critical temperature values in real-time
critical_query = critical_temperatures_stream.writeStream \
    .outputMode("append") \
    .format("console") \
    .queryName("Critical Temperatures") \
    .start()

# Display average readings for each room over a 1-minute window
average_query = average_readings_stream.writeStream \
    .outputMode("complete") \
    .format("console") \
    .queryName("Average Readings") \
    .start()

# Display rooms needing immediate attention due to humidity issues
attention_query = attention_needed_stream.writeStream \
    .outputMode("complete") \
    .format("console") \
    .queryName("Attention Needed") \
    .start()

# Keep the streams running
print("********Critical Temperature Values*******")
critical_query.awaitTermination()

print("********Average Readings Values********")
average_query.awaitTermination()

print("********Attention Needed Values********")
attention_query.awaitTermination()
