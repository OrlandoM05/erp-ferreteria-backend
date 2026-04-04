import { useEffect, useState } from "react";
import api from "../api/api";
import logo from "../assets/logo.png";

export default function Dashboard() {
  const [data, setData] = useState({
    total_sales: 0,
    total_products: 0,
    low_stock: 0,
  });

  const fetchData = async () => {
    try {
      const res = await api.get("/reports/dashboard");
      setData(res.data);
    } catch (error) {
      console.error("Error dashboard");
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div>

      {/* HEADER */}
      <div className="flex items-center gap-4 mb-6">
        <img src={logo} alt="logo" className="w-20" />
        <div>
          <h1 className="text-2xl font-bold text-orange-500">
            Ferretería y Tlapalería La Unión
          </h1>
          <p className="text-gray-400 text-sm">
            Panel de control
          </p>
        </div>
      </div>

      {/* CARDS */}
      <div className="grid grid-cols-3 gap-6">

        <div className="bg-[#1e293b] p-4 rounded-xl">
          <h2 className="text-gray-400">Ventas realizadas</h2>
          <p className="text-2xl font-bold text-orange-500">
            {data.total_sales}
          </p>
        </div>

        <div className="bg-[#1e293b] p-4 rounded-xl">
          <h2 className="text-gray-400">Productos registrados</h2>
          <p className="text-2xl font-bold text-blue-400">
            {data.total_products}
          </p>
        </div>

        <div className="bg-[#1e293b] p-4 rounded-xl">
          <h2 className="text-gray-400">Stock bajo</h2>
          <p className="text-2xl font-bold text-red-400">
            {data.low_stock}
          </p>
        </div>

      </div>
    </div>
  );
}