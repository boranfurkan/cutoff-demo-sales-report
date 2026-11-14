"""Sales report helpers."""
import pandas as pd


def load(rows):
    return pd.DataFrame(rows, columns=["region", "month", "units", "price"])


def fill_gaps(df):
    return df.ffill()


def formatted(df):
    return df[["units", "price"]].map(lambda v: f"{v:.1f}")


def region_counts(df):
    return df["region"].value_counts().to_dict()


def monthly_totals(df):
    df = df.copy()
    df["month"] = pd.to_datetime(df["month"])
    return df.set_index("month")["units"].resample("ME").sum().tolist()


def first_units(df):
    s = df["units"]
    return s.iloc[0]


def by_region(df):
    return df.groupby("region")["units"].sum().to_dict()


def growth(df):
    return df["units"].ffill().pct_change().round(2).tolist()[1:]
