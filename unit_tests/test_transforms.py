from transforms import cast_types, deduplicate, split_valid_invalid

COLUMNS = ["transaction_id", "amount", "status", "timestamp"]


def make_df(spark, rows):
    return cast_types(spark.createDataFrame(rows, COLUMNS))


def test_deduplicate_removes_repeated_ids(spark):
    df = make_df(spark, [
        ("t1", "10.5", "COMPLETED", "2026-01-01T10:00:00"),
        ("t1", "10.5", "COMPLETED", "2026-01-01T10:00:00"),
    ])
    assert deduplicate(df).count() == 1


def test_blank_amount_goes_to_quarantine(spark):
    df = make_df(spark, [
        ("t1", "", "COMPLETED", "2026-01-01T10:00:00"),
        ("t2", "20", "COMPLETED", "2026-01-01T10:00:00"),
    ])
    valid, invalid = split_valid_invalid(df)
    assert valid.count() == 1
    assert invalid.count() == 1


def test_non_numeric_amount_goes_to_quarantine(spark):
    df = make_df(spark, [("t1", "abc", "COMPLETED", "2026-01-01T10:00:00")])
    valid, invalid = split_valid_invalid(df)
    assert valid.count() == 0
    assert invalid.count() == 1


def test_negative_amount_is_invalid(spark):
    df = make_df(spark, [("t1", "-5", "COMPLETED", "2026-01-01T10:00:00")])
    valid, invalid = split_valid_invalid(df)
    assert valid.count() == 0
    assert invalid.count() == 1


def test_unknown_status_is_invalid(spark):
    df = make_df(spark, [("t1", "5", "WEIRD", "2026-01-01T10:00:00")])
    valid, invalid = split_valid_invalid(df)
    assert invalid.count() == 1


def test_every_row_is_in_exactly_one_output(spark):
    df = make_df(spark, [
        ("t1", "10", "COMPLETED", "2026-01-01T10:00:00"),
        ("t2", "", "COMPLETED", "2026-01-01T10:00:00"),
        ("t3", "5", "WEIRD", "2026-01-01T10:00:00"),
        ("t4", "7", "PENDING", "not-a-date"),
    ])
    valid, invalid = split_valid_invalid(df)
    assert valid.count() + invalid.count() == df.count()

def test_excessive_amount_goes_to_quarantine(spark):
    df = make_df(spark, [("t1", "2000000", "COMPLETED", "2026-01-01T10:00:00")])
    valid, invalid = split_valid_invalid(df)
    assert valid.count() == 0
    assert invalid.count() == 1

def test_zero_amount_is_invalid(spark):
    df = make_df(spark, [("t1", "0", "COMPLETED", "2026-01-01T10:00:00")])
    valid, invalid = split_valid_invalid(df)
    assert valid.count() == 0
    assert invalid.count() == 1



