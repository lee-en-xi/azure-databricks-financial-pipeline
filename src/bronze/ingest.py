# Databricks notebook source
dbutils.widgets.text("catalog", "workspace")
dbutils.widgets.text("schema", "fin_pipeline")
catalog = dbutils.widgets.get("catalog")
schema = dbutils.widgets.get("schema")

from pyspark.sql import functions as F

landing = f"/Volumes/{catalog}/{schema}/landing"
checkpoint = f"/Volumes/{catalog}/{schema}/checkpoints/bronze_transactions"
target = f"{catalog}.{schema}.bronze_transactions"

df = (
    spark.readStream.format("cloudFiles")
    .option("cloudFiles.format", "csv")
    .option("header", "true")
    .option("cloudFiles.inferColumnTypes", "false")
    .option("cloudFiles.schemaLocation", checkpoint + "_schema")
    .load(landing)
    .withColumn("_ingested_at", F.current_timestamp())
    .withColumn("_source_file", F.col("_metadata.file_path"))
)

(
    df.writeStream
    .option("checkpointLocation", checkpoint)
    .trigger(availableNow=True)
    .toTable(target)
    .awaitTermination()
)
