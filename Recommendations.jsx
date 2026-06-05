import React, { useState } from "react";

export default function Recommendations() {

  const [product, setProduct] = useState("iPhone 15");
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchRecommendations = async () => {

    setLoading(true);

    try {

      const response = await fetch(
        `http://127.0.0.1:8000/recommend?product_name=${encodeURIComponent(product)}&k=8`
      );

      const data = await response.json();

      setItems(data.recommendations || []);

    } catch (error) {

      console.error(error);

    } finally {

      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "30px" }}>

      <h1>Nexus Commerce Intelligence</h1>

      <div style={{ marginBottom: "20px" }}>

        <input
          type="text"
          value={product}
          onChange={(e) => setProduct(e.target.value)}
          placeholder="Enter Product Name"
          style={{
            padding: "10px",
            width: "250px",
            marginRight: "10px"
          }}
        />

        <button
          onClick={fetchRecommendations}
          style={{
            padding: "10px 20px",
            cursor: "pointer"
          }}
        >
          Generate Recommendations
        </button>

      </div>

      {loading && <p>Loading...</p>}

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(4, 1fr)",
          gap: "20px"
        }}
      >

        {items.map((item, index) => (

          <div
            key={index}
            style={{
              border: "1px solid #ddd",
              borderRadius: "12px",
              padding: "20px",
              boxShadow: "0 4px 10px rgba(0,0,0,0.1)"
            }}
          >

            <h3>{item.product}</h3>

            <p>
              Score:
              {" "}
              {Number(item.score).toFixed(4)}
            </p>

          </div>

        ))}

      </div>

    </div>
  );
}