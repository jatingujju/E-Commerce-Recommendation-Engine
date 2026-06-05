import lightgbm as lgb
import pandas as pd

# Load training data
X = pd.read_parquet(
    "rank_train.parquet"
)

feature_cols = [

    "user_score",
    "user_views",
    "user_carts",
    "user_purchases",

    "item_popularity",
    "item_views",
    "item_purchases"
]

# Query groups
X = X.sort_values("user_id")

group = (
    X.groupby("user_id")
    .size()
    .values
)

dtrain = lgb.Dataset(
    X[feature_cols],
    label=X["label"],
    group=group
)

params = {

    "objective":
        "lambdarank",

    "metric":
        "ndcg",

    "learning_rate":
        0.05,

    "num_leaves":
        31,

    "min_data_in_leaf":
        5,

    "verbosity":
        -1
}

model = lgb.train(
    params,
    dtrain,
    num_boost_round=100
)

model.save_model(
    "lgb_ranker.txt"
)

print(
    "\nModel saved: lgb_ranker.txt"
)