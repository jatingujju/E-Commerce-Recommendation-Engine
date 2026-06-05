from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

from ranking_engine import rank_products

# ======================================
# FASTAPI APP
# ======================================

app = FastAPI(
    title="Nexus Commerce Intelligence API",
    description="AI Powered Product Recommendation Engine",
    version="1.0.0"
)

# ======================================
# CORS
# ======================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================================
# LOAD DATA
# ======================================

items = pd.read_csv("data/items.csv")

# ======================================
# HOME
# ======================================

@app.get("/")
def home():

    return {
        "status": "running",
        "project": "Nexus Commerce Intelligence Platform",
        "products": len(items)
    }

# ======================================
# HEALTH CHECK
# ======================================

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }

# ======================================
# PRODUCT LIST
# ======================================

@app.get("/products")
def get_products():

    return {
        "products": items["name"].tolist()
    }

# ======================================
# RECOMMENDATION ENDPOINT
# ======================================

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

# ======================================
# PRODUCT DETAILS
# ======================================

@app.get("/product")
def product_details(
    product_name: str
):

    result = items[
        items["name"].str.lower()
        ==
        product_name.lower()
    ]

    if len(result) == 0:

        return {
            "error": "Product not found"
        }

    return result.iloc[0].to_dict()

# ======================================
# API INFO
# ======================================

@app.get("/about")
def about():

    return {
        "project":
            "E-Commerce Product Recommendation Engine",

        "features": [

            "TF-IDF Candidate Generation",

            "Cosine Similarity",

            "Heap-Based Top-K Ranking",

            "Product Similarity Graph",

            "Streamlit Dashboard",

            "LightGBM LambdaRank",

            "FastAPI REST API"
        ]
    }

