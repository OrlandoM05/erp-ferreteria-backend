import { useEffect, useState } from "react";
import api from "../api/api";

export default function Products() {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);

  const [name, setName] = useState("");
  const [categoryId, setCategoryId] = useState("");

  // 🔄 cargar productos
  const fetchProducts = async () => {
    try {
      const res = await api.get("/products");
      setProducts(res.data);
    } catch (error) {
      console.error("Error productos");
    }
  };

  // 🔄 cargar categorías
  const fetchCategories = async () => {
    try {
      const res = await api.get("/products/categories");
      setCategories(res.data);
    } catch (error) {
      console.error("Error categorías");
    }
  };

  useEffect(() => {
    fetchProducts();
    fetchCategories();
  }, []);

  // ➕ crear producto
  const handleCreate = async () => {
    if (!name || !categoryId) {
      alert("Completa los campos");
      return;
    }

    try {
      await api.post("/products", {
        name,
        category_id: Number(categoryId),
      });

      setName("");
      setCategoryId("");

      fetchProducts();
    } catch {
      alert("Error al crear producto");
    }
  };

  return (
    <div>

      <h1 className="text-2xl font-bold mb-6 text-orange-500">
        Productos
      </h1>

      {/* FORM PRO */}
      <div className="bg-[#1e293b] p-4 rounded-xl mb-6 flex gap-4">

        <input
          placeholder="Nombre del producto"
          className="p-2 rounded bg-[#020617] border border-gray-700 text-white flex-1"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />

        {/* 🔥 SELECT PRO */}
        <select
          className="p-2 rounded bg-[#020617] border border-gray-700 text-white w-56"
          value={categoryId}
          onChange={(e) => setCategoryId(e.target.value)}
        >
          <option value="">Seleccionar categoría</option>
          {categories.map((c) => (
            <option key={c.id} value={c.id}>
              {c.name}
            </option>
          ))}
        </select>

        <button
          onClick={handleCreate}
          className="bg-orange-500 px-4 rounded font-bold hover:bg-orange-600"
        >
          Crear
        </button>
      </div>

      {/* TABLA */}
      <div className="bg-[#1e293b] rounded-xl overflow-hidden">
        <table className="w-full text-sm">

          <thead className="bg-[#020617] text-gray-400">
            <tr>
              <th className="p-3 text-left">ID</th>
              <th className="p-3 text-left">Nombre</th>
              <th className="p-3 text-left">SKU</th>
              <th className="p-3 text-left">Categoría</th>
            </tr>
          </thead>

          <tbody>
            {products.map((p) => (
              <tr key={p.id} className="border-t border-gray-700 hover:bg-[#334155]">
                <td className="p-3">{p.id}</td>
                <td className="p-3">{p.name}</td>
                <td className="p-3">{p.sku}</td>
                <td className="p-3">
                  {categories.find(c => c.id === p.category_id)?.name || p.category_id}
                </td>
              </tr>
            ))}
          </tbody>

        </table>
      </div>

    </div>
  );
}