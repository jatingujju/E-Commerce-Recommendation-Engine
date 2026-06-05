import lightgbm as lgb
import pandas as pd

model = lgb.Booster(
    model_file="lgb_ranker.txt"
)

sample = pd.DataFrame([
    {
        "user_score": 11,
        "user_views": 3,
        "user_carts": 1,
        "user_purchases": 1,
        "item_popularity": 10,
        "item_views": 2,
        "item_purchases": 1
    }
])

score = model.predict(sample)

print("Prediction Score:")
print(score)