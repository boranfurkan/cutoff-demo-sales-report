"""Sales report helpers."""
import pandas as pd


def load(rows):
    return pd.DataFrame(rows, columns=["region", "month", "units", "price"])


def fill_gaps(df):
    return df.fillna(method="ffill")


def formatted(df):
    return df[["units", "price"]].applymap(lambda v: f"{v:.1f}")


def region_counts(df):
    return pd.value_counts(df["region"]).to_dict()


def monthly_totals(df):
    df = df.copy()
    df["month"] = pd.to_datetime(df["month"])
    return df.set_index("month")["units"].resample("M").sum().tolist()


def first_units(df):
    s = df["units"]
    return s[0]


def by_region(df):
    return df.groupby("region", axis=0)["units"].sum().to_dict()


def growth(df):
    return df["units"].pct_change(fill_method="pad").round(2).tolist()[1:]
