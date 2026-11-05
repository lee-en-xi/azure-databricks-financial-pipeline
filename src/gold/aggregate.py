# Databricks notebook source
dbutils.widgets.text("catalog", "workspace")
dbutils.widgets.text("schema", "fin_pipeline")
dbutils.widgets.text("max_quarantine_ratio", "0.10")
catalog = dbutils.widgets.get("catalog")
schema = dbutils.widgets.get("schema")
max_ratio = float(dbutils.widgets.get("max_quarantine_ratio"))

from pyspark.sql import functions as F

silver = spark.table(f"{catalog}.{schema}.silver_transactions")
quarantine = spark.table(f"{catalog}.{schema}.quarantine_transactions")

# 1. Business table: completed transactions per day and merchant
daily = (
    silver.filter(F.col("status") == "COMPLETED")
    .groupBy(F.to_date("timestamp").alias("txn_date"), "merchant")
    .agg(
        F.count("*").alias("txn_count"),
        F.round(F.sum("amount"), 2).alias("total_amount"),
    )
)
daily.write.mode("overwrite").saveAsTable(f"{catalog}.{schema}.gold_daily_merchant")

# 2. Data quality log: one row appended per run
valid_rows = silver.count()
bad_rows = quarantine.count()
total = valid_rows + bad_rows
ratio = bad_rows / total if total else 0.0

log = (
    spark.createDataFrame(
        [(valid_rows, bad_rows, float(ratio))],
        "valid_rows long, quarantined_rows long, quarantine_ratio double",
    )
    .withColumn("checked_at", F.current_timestamp())
)
log.write.mode("append").saveAsTable(f"{catalog}.{schema}.gold_quality_log")

print(f"valid={valid_rows} quarantined={bad_rows} ratio={ratio:.3f}")

# 3. Quality gate: fail the job if too many rows are bad
if ratio > max_ratio:
    raise Exception(
        f"Data quality check failed: quarantine ratio {ratio:.3f} is above {max_ratio}"
    )
