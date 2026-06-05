import pandas as pd
from pathlib import Path

# ==========================================
# LOAD DATA
# ==========================================

DATA_DIR = Path("data")

events_path = DATA_DIR / "events.csv"
items_path = DATA_DIR / "items.csv"

if not events_path.exists():
    raise FileNotFoundError(
        f"File not found: {events_path}"
    )

if not items_path.exists():
    raise FileNotFoundError(
        f"File not found: {items_path}"
    )

events = pd.read_csv(
    events_path,
    parse_dates=["ts"]
)

items = pd.read_csv(
    items_path
)

# ==========================================
# VALIDATE SCHEMA
# ==========================================

required_columns = {
    "user_id",
    "item_id",
    "event",
    "ts"
}

missing = required_columns - set(events.columns)

if missing:
    raise ValueError(
        f"Missing columns: {missing}"
    )

# ==========================================
# IMPLICIT FEEDBACK WEIGHTS
# ==========================================

WEIGHTS = {
    "view": 1,
    "cart": 3,
    "purchase": 5
}

events["weight"] = (
    events["event"]
    .map(WEIGHTS)
    .fillna(0)
)

# ==========================================
# USER FEATURE STORE
# ==========================================

user_features = (
    events
    .groupby("user_id")
    .agg(
        total_views=(
            "event",
            lambda x: (x == "view").sum()
        ),
        total_carts=(
            "event",
            lambda x: (x == "cart").sum()
        ),
        total_purchases=(
            "event",
            lambda x: (x == "purchase").sum()
        ),
        implicit_score=(
            "weight",
            "sum"
        )
    )
    .reset_index()
)

# ==========================================
# ITEM FEATURE STORE
# ==========================================

item_features = (
    events
    .groupby("item_id")
    .agg(
        views=(
            "event",
            lambda x: (x == "view").sum()
        ),
        carts=(
            "event",
            lambda x: (x == "cart").sum()
        ),
        purchases=(
            "event",
            lambda x: (x == "purchase").sum()
        ),
        popularity_score=(
            "weight",
            "sum"
        )
    )
    .reset_index()
)

# ==========================================
# SAVE FEATURE STORE
# ==========================================

user_features.to_csv(
    "user_features.csv",
    index=False
)

item_features.to_csv(
    "item_features.csv",
    index=False
)

# ==========================================
# OUTPUT
# ==========================================

print("\n" + "=" * 50)
print("USER FEATURE STORE")
print("=" * 50)

print(user_features)

print("\n" + "=" * 50)
print("ITEM FEATURE STORE")
print("=" * 50)

print(item_features)

print("\nFiles Generated:")
print("✓ user_features.csv")
print("✓ item_features.csv")