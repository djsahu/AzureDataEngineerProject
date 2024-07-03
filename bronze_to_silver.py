# Databricks notebook source
from pyspark.sql.functions import *
from pyspark.sql.types import *

# COMMAND ----------

table_names=[]
for i in dbutils.fs.ls('/mnt/bronze/Sales'):
    table_names.append(i.name.split('/')[0])
print(table_names)

# COMMAND ----------

for i in table_names:
    path='/mnt/bronze/Sales/'+i+'/'+i+'.parquet'
    df = spark.read.format('parquet').load(path)
    cols =df.columns

    for c in cols:
        if "date" in c or "Date" in c:
            df=df.withColumn(c,date_format(from_utc_timestamp(col(c).cast(TimestampType()),"UTC"),"yyyy-MM-dd"))
    output_path = '/mnt/silver/Sales/'+i+'/'
    df.write.format('delta').mode('overwrite').save(output_path)

# COMMAND ----------

display(df)

# COMMAND ----------

df = spark.read.format('delta').option('header',True).load('/mnt/silver/Sales/CountryRegionCurrency/')
df.show()

# COMMAND ----------



# COMMAND ----------


