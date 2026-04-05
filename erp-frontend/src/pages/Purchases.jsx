import { useState } from "react";
import api from "../api/api";

export default function Purchases() {
  const [productId, setProductId] = useState("");
  const [supplierId, setSupplierId] = useState("");
  const [quantity, setQuantity] = useState("");
  const [price, setPrice] = useState("");

  const handlePurchase = async () => {
    if (!productId || !supplierId || !quantity || !price) {
      alert("Completa todos los campos");
      return;
    }

    try {
      await api.post("/purchases", {
        product_id: Number(productId),
        supplier_id: Number(supplierId),
        quantity: Number(quantity),
        price: Number(price),
      });

      alert("Compra registrada");

      setProductId("");
      setSupplierId("");
      setQuantity("");
      setPrice("");

    } catch {
      alert("Error al registrar compra");
    }
  };

  return (
    <div>

      <h1 className="text-2xl font-bold text-orange-500 mb-6">
        Compras
      </h1>

      <div className="bg-[#1e293b] p-6 rounded-xl flex flex-col gap-4 max-w-xl">

        <input
          placeholder="ID Producto"
          className="p-3 rounded bg-[#020617] border border-gray-700 text-white"
          value={productId}
          onChange={(e) => setProductId(e.target.value)}
        />

        <input
          placeholder="ID Proveedor"
          className="p-3 rounded bg-[#020617] border border-gray-700 text-white"
          value={supplierId}
          onChange={(e) => setSupplierId(e.target.value)}
        />

        <input
          placeholder="Cantidad"
          className="p-3 rounded bg-[#020617] border border-gray-700 text-white"
          value={quantity}
          onChange={(e) => setQuantity(e.target.value)}
        />

        <input
          placeholder="Precio unitario"
          className="p-3 rounded bg-[#020617] border border-gray-700 text-white"
          value={price}
          onChange={(e) => setPrice(e.target.value)}
        />

        <button
          onClick={handlePurchase}
          className="bg-orange-500 p-3 rounded font-bold hover:bg-orange-600"
        >
          Registrar compra
        </button>

      </div>
    </div>
  );
}