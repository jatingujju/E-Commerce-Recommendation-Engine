from fastapi import FastAPI
import pandas as pd

from ranking_engine import rank_products

app = FastAPI(
    title="Nexus Commerce Intelligence API"
)

items = pd.read_csv("data/items.csv")

@app.get("/")
def home():

    return {
        "status": "running",
        "project": "E-Commerce Recommendation Engine"
    }


@app.get("/recommend")
def recommend(
    product_name: str,
    k: int = 5
):

    recommendations = rank_products(
        product_name,
        k
    )

    return {
        "product": product_name,
        "recommendations": recommendations
    } 