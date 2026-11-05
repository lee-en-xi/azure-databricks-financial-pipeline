# Databricks notebook source
dbutils.widgets.text("catalog", "workspace")
dbutils.widgets.text("schema", "fin_pipeline")
catalog = dbutils.widgets.get("catalog")
schema = dbutils.widgets.get("schema")

from transforms import cast_types, deduplicate, split_valid_invalid

bronze = spark.table(f"{catalog}.{schema}.bronze_transactions")
typed = deduplicate(cast_types(bronze))
valid, invalid = split_valid_invalid(typed)

valid.write.mode("overwrite").saveAsTable(f"{catalog}.{schema}.silver_transactions")
invalid.write.mode("overwrite").saveAsTable(f"{catalog}.{schema}.quarantine_transactions")

print(f"valid={valid.count()} quarantined={invalid.count()}")
