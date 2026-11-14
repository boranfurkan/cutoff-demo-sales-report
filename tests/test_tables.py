from report import tables

ROWS = [
    ["north", "2025-01-15", 10.0, 2.5],
    ["south", "2025-01-20", None, 3.0],
    ["north", "2025-02-10", 30.0, 2.0],
]


def df():
    return tables.load(ROWS)


def test_fill_gaps():
    assert tables.fill_gaps(df())["units"].tolist() == [10.0, 10.0, 30.0]


def test_formatted():
    assert tables.formatted(tables.fill_gaps(df())).iloc[0].tolist() == ["10.0", "2.5"]


def test_region_counts():
    assert tables.region_counts(df()) == {"north": 2, "south": 1}


def test_monthly_totals():
    assert tables.monthly_totals(tables.fill_gaps(df())) == [20.0, 30.0]


def test_first_units():
    d = tables.fill_gaps(df())
    d.index = ["a", "b", "c"]
    assert tables.first_units(d) == 10.0


def test_by_region():
    assert tables.by_region(tables.fill_gaps(df())) == {"north": 40.0, "south": 10.0}


def test_growth():
    assert tables.growth(df()) == [0.0, 2.0]
