from pyspark.sql import DataFrame
from pyspark.sql import functions as F

VALID_STATUSES = ["COMPLETED", "PENDING", "FAILED"]


def cast_types(df: DataFrame) -> DataFrame:
    """Convert raw strings to proper types. Bad values become null."""
    return (
        df.withColumn("amount", F.expr("try_cast(amount AS DOUBLE)"))
          .withColumn("timestamp", F.expr("try_cast(timestamp AS TIMESTAMP)"))
    )


def deduplicate(df: DataFrame) -> DataFrame:
    """Keep one row per transaction_id."""
    return df.dropDuplicates(["transaction_id"])


def split_valid_invalid(df: DataFrame):
    """Return (valid_rows, invalid_rows). Every row lands in exactly one."""
    rule = F.coalesce(
        F.col("transaction_id").isNotNull()
        & F.col("amount").isNotNull()
        & (F.col("amount") >= 0)
        & F.col("status").isin(VALID_STATUSES)
        & F.col("timestamp").isNotNull(),
        F.lit(False),
    )
    return df.filter(rule), df.filter(~rule)
