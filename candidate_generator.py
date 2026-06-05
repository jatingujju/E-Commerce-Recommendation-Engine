import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load products
items = pd.read_csv("data/items.csv")

# Create text features
items["features"] = (
    items["category"].fillna("") + " " +
    items["brand"].fillna("") + " " +
    items["description"].fillna("")
)

# TF-IDF
vectorizer = TfidfVectorizer()

feature_matrix = vectorizer.fit_transform(
    items["features"]
)

# Similarity Matrix
similarity_matrix = cosine_similarity(
    feature_matrix
)

def get_candidates(product_name, top_n=5):

    matches = items[
        items["name"].str.lower() ==
        product_name.lower()
    ]

    if matches.empty:
        return []

    idx = matches.index[0]

    scores = list(
        enumerate(
            similarity_matrix[idx]
        )
    )

    scores.sort(
        key=lambda x: x[1],
        reverse=True
    )

    candidates = []

    for i, score in scores[1:top_n+1]:

        candidates.append({
            "product": items.iloc[i]["name"],
            "score": round(float(score), 4)
        })

    return candidates


if __name__ == "__main__":

    product = input(
        "Enter Product Name: "
    )

    results = get_candidates(product)

    print("\nCandidates")

    for r in results:
        print(r)