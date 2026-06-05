import lightgbm as lgb

model = lgb.Booster(
    model_file="lgb_ranker.txt"
)

print(model.feature_importance())