import { useState } from "react";
import api from "../api/api";

export default function Inventory() {
  const [productId, setProductId] = useState("");
  const [branchId, setBranchId] = useState(1); // matriz
  const [quantity, setQuantity] = useState("");
  const [reason, setReason] = useState("");

  // ➕ ENTRADA
  const handleIn = async () => {
    try {
      await api.post("/inventory/in", {
        product_id: Number(productId),
        branch_id: branchId,
        quantity: Number(quantity),
        reason,
      });

      alert("Stock agregado");
      clear();
    } catch {
      alert("Error entrada");
    }
  };

  // ➖ SALIDA
  const handleOut = async () => {
    try {
      await api.post("/inventory/out", {
        product_id: Number(productId),
        branch_id: branchId,
        quantity: Number(quantity),
        reason,
      });

      alert("Stock retirado");
      clear();
    } catch {
      alert("Error salida");
    }
  };

  const clear = () => {
    setProductId("");
    setQuantity("");
    setReason("");
  };

  return (
    <div>

      <h1 className="text-2xl font-bold text-orange-500 mb-6">
        Inventario
      </h1>

      <div className="bg-[#1e293b] p-6 rounded-xl flex flex-col gap-4 max-w-xl">

        <input
          placeholder="ID Producto"
          className="p-3 rounded bg-[#020617] border border-gray-700 text-white"
          value={productId}
          onChange={(e) => setProductId(e.target.value)}
        />

        <input
          placeholder="Cantidad"
          className="p-3 rounded bg-[#020617] border border-gray-700 text-white"
          value={quantity}
          onChange={(e) => setQuantity(e.target.value)}
        />

        <input
          placeholder="Motivo"
          className="p-3 rounded bg-[#020617] border border-gray-700 text-white"
          value={reason}
          onChange={(e) => setReason(e.target.value)}
        />

        <div className="flex gap-4">

          <button
            onClick={handleIn}
            className="flex-1 bg-green-500 p-3 rounded font-bold hover:bg-green-600"
          >
            Entrada
          </button>

          <button
            onClick={handleOut}
            className="flex-1 bg-red-500 p-3 rounded font-bold hover:bg-red-600"
          >
            Salida
          </button>

        </div>

      </div>
    </div>
  );
}