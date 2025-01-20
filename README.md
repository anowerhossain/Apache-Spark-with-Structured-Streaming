
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

5. 🔍 Define Analytical SQL Queries
* Defined three SQL queries for real-time analysis:

🔴 Critical Temperatures Query

+ Detects rooms with extreme temperatures (below 18°C or above 60°C).

```sql
SELECT room_id, temperature, humidity, timestamp 
FROM sensor_table 
WHERE temperature < 18 OR temperature > 60;
```

📊 Average Readings Query

+ Calculates the average temperature and humidity for each room over a 1-minute sliding window.

```sql
SELECT room_id, 
       AVG(temperature) AS avg_temperature, 
       AVG(humidity) AS avg_humidity, 
       window.start AS window_start 
FROM sensor_table
GROUP BY room_id, window(timestamp, '1 minute');
```

⚠️ Attention Needed Query

+ Identifies rooms with abnormal humidity levels (below 45% or above 75%).

```sql
SELECT room_id, COUNT(*) AS critical_readings 
FROM sensor_table 
WHERE humidity < 45 OR humidity > 75
GROUP BY room_id;
```

6. 📥 Execute SQL Queries
* Executed the SQL queries on the simulated streaming data to generate insights:

```python
critical_temperatures_stream = spark.sql(critical_temperature_query)
average_readings_stream = spark.sql(average_readings_query)
attention_needed_stream = spark.sql(attention_needed_query)
```

7. 📤 Output Results to Console
* Displayed the results of each query in real-time for immediate insights:

**Critical Temperatures**
- Displays rooms with extreme temperature conditions.

```python
critical_temperatures_stream.writeStream \
    .outputMode("append") \
    .format("console") \
    .queryName("Critical Temperatures") \
    .start()
```

**Average Readings**
- Shows the 1-minute average temperature and humidity for each room.

```python
average_readings_stream.writeStream \
    .outputMode("complete") \
    .format("console") \
    .queryName("Average Readings") \
    .start()
```

**Attention Needed**
- Lists rooms requiring immediate attention due to abnormal humidity.

```python
attention_needed_stream.writeStream \
    .outputMode("complete") \
    .format("console") \
    .queryName("Attention Needed") \
    .start()
```
