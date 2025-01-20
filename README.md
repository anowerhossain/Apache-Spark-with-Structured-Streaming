
# 🚀 Smart Building HVAC Monitoring with Apache Spark

This project demonstrates how to leverage Apache Spark for real-time monitoring and analysis of HVAC (Heating, Ventilation, and Air Conditioning) systems in smart buildings. By simulating real-time sensor data, the solution provides actionable insights into indoor environmental conditions.

## 📝 Tasks Performed

1. 📦 Install Required Packages
Installed PySpark and FindSpark to set up the Spark environment locally.
Suppressed warnings for cleaner outputs.

```bash
!pip install pyspark==3.1.2 -q
!pip install findspark -q

```

2. 🛠️ Set Up Spark Session
Initialized a Spark session named Smart Building HVAC Monitoring.
Spark handles distributed data processing for real-time analytics.

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Smart Building HVAC Monitoring") \
    .getOrCreate()
```



