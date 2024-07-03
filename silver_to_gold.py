# Databricks notebook source
from pyspark.sql.functions import *
from pyspark.sql.types import *

# COMMAND ----------

table_names=[]
for i in dbutils.fs.ls('/mnt/silver/Sales'):
    table_names.append(i.name.split('/')[0])
print(table_names)

# COMMAND ----------

# df = spark.read.format('delta').load('/mnt/silver/Sales/SpecialOffer')
# cols=df.columns
# for c in cols:
    # for i, char in enumerate(c):
    #     print(i,char)
    # new_col="".join(["_" + char if char.isupper() and not old_c[i-1].isupper() and i!=0 else char for i, char in enumerate(old_c)])
    # print(new_col)

# COMMAND ----------

# trying with function
# def convertCol(col_name):
#     new_col=""
#     for i, char in enumerate(col_name):
#         if char.isupper() and i!=0 and not col_name[i-1].isupper():
#             new_col=new_col+'_'+char
#         else:
#             new_col+=char
#     return new_col
# print(convertCol("DimensionTable"))

# COMMAND ----------


for i in table_names:
    path='/mnt/silver/Sales/'+i
    df = spark.read.format('delta').load(path)
    cols=df.columns

    for old_c in cols:
        new_col="".join(["_" + char if char.isupper() and not old_c[i-1].isupper() and i!=0 else char for i, char in enumerate(old_c)])
        df=df.withColumnRenamed(old_c,new_col)
    
    output_path = '/mnt/gold/Sales/'+i+'/'
    df.write.format('delta').mode('overwrite').save(output_path)

# COMMAND ----------

# display(df)

# COMMAND ----------


