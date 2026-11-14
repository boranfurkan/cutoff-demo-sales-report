import math

from report import tables

ROWS = [
    ["north", "2025-01-15", 10.0, 2.5],
    ["south", "2025-01-20", None, 3.0],
    ["north", "2025-03-10", 30.0, None],
]


def df():
    return tables.load(ROWS)


def test_fill_gaps_does_not_mutate_input_and_fills_all_columns():
    d = df()
    out = tables.fill_gaps(d)
    assert math.isnan(d["units"].iloc[1])
    assert out["units"].tolist() == [10.0, 10.0, 30.0]
    assert out["price"].tolist() == [2.5, 3.0, 3.0]
    assert out["region"].tolist() == ["north", "south", "north"]


def test_region_counts_plain_types():
    counts = tables.region_counts(df())
    assert counts == {"north": 2, "south": 1}
    assert all(type(k) is str for k in counts)
    assert all(int(v) == v for v in counts.values())


def test_monthly_totals_month_end_bins_include_empty_months():
    assert tables.monthly_totals(tables.fill_gaps(df())) == [20.0, 0.0, 30.0]


def test_first_units_is_positional_with_integer_like_labels():
    d = tables.fill_gaps(df())
    d.index = [2, 1, 0]
    assert tables.first_units(d) == 10.0


def test_by_region_keys_are_str():
    out = tables.by_region(tables.fill_gaps(df()))
    assert out == {"north": 40.0, "south": 10.0}
    assert all(type(k) is str for k in out)


def test_growth_pads_missing_values():
    rows = [
        ["a", "2025-01-01", 10.0, 1.0],
        ["a", "2025-01-02", None, 1.0],
        ["a", "2025-01-03", None, 1.0],
        ["a", "2025-01-04", 20.0, 1.0],
    ]
    assert tables.growth(tables.load(rows)) == [0.0, 0.0, 1.0]


def test_formatted_strings():
    out = tables.formatted(tables.fill_gaps(df()))
    assert out.iloc[2].tolist() == ["30.0", "3.0"]
