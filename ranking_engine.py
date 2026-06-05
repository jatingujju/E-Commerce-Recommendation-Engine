import heapq
from candidate_generator import get_candidates

def rank_products(product_name, k=5):

    candidates = get_candidates(
        product_name,
        top_n=20
    )

    top_k = heapq.nlargest(
        k,
        candidates,
        key=lambda x: x["score"]
    )

    return top_k


if __name__ == "__main__":

    product = input(
        "Enter Product Name: "
    )

    ranked = rank_products(
        product
    )

    print("\nTop Recommendations")

    for idx, item in enumerate(
        ranked,
        start=1
    ):
        print(
            f"{idx}. "
            f"{item['product']} "
            f"({item['score']})"
        )