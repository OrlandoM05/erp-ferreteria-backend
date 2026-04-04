import { useState } from "react";
import api from "../api/api";

export default function Sales() {
  const [barcode, setBarcode] = useState("");
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);

  // ➕ agregar producto con info real
  const addItem = async () => {
    if (!barcode.trim()) return;

    try {
      const res = await api.get(`/products/pos/${barcode.trim()}`);
      const product = res.data;

      const price = product.price;

      const existing = items.find(i => i.barcode === product.barcode);

      if (existing) {
        setItems(items.map(i =>
          i.barcode === product.barcode
            ? {
                ...i,
                quantity: i.quantity + 1,
                subtotal: (i.quantity + 1) * i.price
              }
            : i
        ));
      } else {
        setItems([
          ...items,
          {
            barcode: product.barcode, // 🔥 usar el del backend
            name: product.name,
            price,
            quantity: 1,
            subtotal: price
          }
        ]);
      }

      setBarcode("");

    } catch (error) {
      console.error("ERROR PRODUCTO:", error.response?.data || error);
      alert("Producto no encontrado");
    }
  };

  // ❌ eliminar
  const removeItem = (barcode) => {
    setItems(items.filter(i => i.barcode !== barcode));
  };

  // 💰 total
  const total = items.reduce((sum, i) => sum + i.subtotal, 0);

  // 💰 vender
  const handleSale = async () => {
    if (items.length === 0) return;

    try {
      setLoading(true);

      const payload = {
        items: items.map(i => ({
          barcode: i.barcode,
          quantity: i.quantity
        }))
      };

      // 🔥 DEBUG (puedes quitar luego)
      console.log("PAYLOAD:", payload);

      await api.post("/sales", payload);

      setItems([]);
      alert("Venta realizada");

    } catch (error) {
      console.error("ERROR VENTA:", error.response?.data || error);
      alert("Error en venta");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>

      <h1 className="text-2xl font-bold text-orange-500 mb-6">
        Punto de Venta
      </h1>

      {/* INPUT */}
      <div className="bg-[#1e293b] p-4 rounded-xl mb-6 flex gap-4">

        <input
          placeholder="Escanea código de barras"
          className="p-3 rounded bg-[#020617] border border-gray-700 text-white flex-1"
          value={barcode}
          onChange={(e) => setBarcode(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && addItem()}
        />

        <button
          onClick={addItem}
          className="bg-orange-500 px-6 rounded font-bold hover:bg-orange-600"
        >
          Agregar
        </button>
      </div>

      {/* LISTA */}
      <div className="bg-[#1e293b] rounded-xl p-4 mb-6">

        {items.length === 0 && (
          <p className="text-gray-400">No hay productos</p>
        )}

        {items.map((item) => (
          <div
            key={item.barcode}
            className="grid grid-cols-5 gap-4 border-b border-gray-700 py-2 items-center"
          >
            <span className="col-span-2">{item.name}</span>
            <span>${item.price}</span>
            <span>x{item.quantity}</span>
            <span className="text-orange-400 font-bold">
              ${item.subtotal}
            </span>

            <button
              onClick={() => removeItem(item.barcode)}
              className="text-red-400"
            >
              ❌
            </button>
          </div>
        ))}

      </div>

      {/* TOTAL */}
      <div className="bg-[#1e293b] p-4 rounded-xl mb-6 flex justify-between text-xl">
        <span>Total:</span>
        <span className="text-green-400 font-bold">${total}</span>
      </div>

      {/* BOTÓN */}
      <button
        onClick={handleSale}
        disabled={loading}
        className="w-full bg-green-500 p-4 rounded font-bold text-lg hover:bg-green-600"
      >
        {loading ? "Procesando..." : "Finalizar Venta"}
      </button>

    </div>
  );
}