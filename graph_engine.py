import networkx as nx
import matplotlib.pyplot as plt

from ranking_engine import rank_products


def build_graph(product_name):

    G = nx.Graph()

    recommendations = rank_products(
        product_name,
        k=5
    )

    G.add_node(product_name)

    for rec in recommendations:

        G.add_node(rec["product"])

        G.add_edge(
            product_name,
            rec["product"],
            weight=rec["score"]
        )

    return G


def visualize_graph(product_name):

    G = build_graph(product_name)

    plt.figure(figsize=(12, 8))

    pos = nx.spring_layout(
        G,
        seed=42
    )

    nx.draw_networkx_nodes(
        G,
        pos,
        node_size=3000
    )

    nx.draw_networkx_edges(
        G,
        pos,
        width=2
    )

    nx.draw_networkx_labels(
        G,
        pos,
        font_size=10
    )

    edge_labels = nx.get_edge_attributes(
        G,
        "weight"
    )

    edge_labels = {
        k: round(v, 2)
        for k, v in edge_labels.items()
    }

    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=edge_labels
    )

    plt.title(
        f"Product Similarity Graph - {product_name}",
        fontsize=14
    )

    plt.axis("off")

    # Automatically save graph image
    plt.savefig(
        "product_similarity_graph.png",
        dpi=300,
        bbox_inches="tight"
    )

    print(
        "\nGraph saved as: product_similarity_graph.png"
    )

    plt.show()


if __name__ == "__main__":

    product = input(
        "Enter Product Name: "
    )

    visualize_graph(product)