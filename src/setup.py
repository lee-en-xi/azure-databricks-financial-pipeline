# Databricks notebook source
dbutils.widgets.text("catalog", "workspace")
dbutils.widgets.text("schema", "fin_pipeline")
catalog = dbutils.widgets.get("catalog")
schema = dbutils.widgets.get("schema")

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.{schema}")
spark.sql(f"CREATE VOLUME IF NOT EXISTS {catalog}.{schema}.landing")
spark.sql(f"CREATE VOLUME IF NOT EXISTS {catalog}.{schema}.checkpoints")
print(f"Ready: {catalog}.{schema}")
