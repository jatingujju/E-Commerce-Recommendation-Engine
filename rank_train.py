import pandas as pd

# Load features
users = pd.read_csv("user_features.csv")
items = pd.read_csv("item_features.csv")
events = pd.read_csv("data/events.csv")

# Purchase labels
purchases = events[events["event"] == "purchase"]

rows = []

for _, p in purchases.iterrows():

    user_id = p["user_id"]
    item_id = p["item_id"]

    uf = users[users["user_id"] == user_id]
    it = items[items["item_id"] == item_id]

    if len(uf) == 0 or len(it) == 0:
        continue

    rows.append({
        "user_id": user_id,
        "item_id": item_id,

        "user_score":
            uf.iloc[0]["implicit_score"],

        "user_views":
            uf.iloc[0]["total_views"],

        "user_carts":
            uf.iloc[0]["total_carts"],

        "user_purchases":
            uf.iloc[0]["total_purchases"],

        "item_popularity":
            it.iloc[0]["popularity_score"],

        "item_views":
            it.iloc[0]["views"],

        "item_purchases":
            it.iloc[0]["purchases"],

        "label": 1
    })

rank_df = pd.DataFrame(rows)

rank_df.to_parquet(
    "rank_train.parquet",
    index=False
)

print(rank_df.head())
print("\nSaved: rank_train.parquet")