
# 🚀 Smart Building HVAC Monitoring with Apache Spark

This project demonstrates how to leverage Apache Spark for real-time monitoring and analysis of HVAC (Heating, Ventilation, and Air Conditioning) systems in smart buildings. By simulating real-time sensor data, the solution provides actionable insights into indoor environmental conditions.

## 📝 Tasks Performed

1. 📦 Install Required Packages
* Installed PySpark and FindSpark to set up the Spark environment locally.
* Suppressed warnings for cleaner outputs.

```bash
!pip install pyspark==3.1.2 -q
!pip install findspark -q

```

2. 🛠️ Set Up Spark Session
* Initialized a Spark session named Smart Building HVAC Monitoring.
* Spark handles distributed data processing for real-time analytics.

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Smart Building HVAC Monitoring") \
    .getOrCreate()
```

3. 🔄 Simulate Real-Time Sensor Data
Used Spark’s rate source to simulate continuous streaming data.
Each row includes:
* room_id: Unique identifier for a room.
* temperature: Randomized temperature readings.
* humidity: Randomized humidity readings.

```python
from pyspark.sql.functions import expr, rand, when

sensor_data = spark.readStream.format("rate").option("rowsPerSecond", 5).load() \
    .withColumn("room_id", expr("CAST(value % 10 AS STRING)")) \
    .withColumn("temperature", when(expr("value % 10 == 0"), 15).otherwise(20 + rand() * 25)) \
    .withColumn("humidity", expr("40 + rand() * 30"))
```

4. 📋 Create Temporary SQL View
* Created a temporary SQL view to query the streaming data easily using Spark SQL.

```python
sensor_data.createOrReplaceTempView("sensor_table")
```



