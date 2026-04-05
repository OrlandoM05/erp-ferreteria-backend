import { useState } from "react";
import api from "../api/api";
import * as XLSX from "xlsx";
import { saveAs } from "file-saver";

export default function Reports() {
  const [data, setData] = useState(null);
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

  const fetchReport = async () => {
    try {
      const res = await api.get("/reports/sales", {
        params: {
          start_date: startDate,
          end_date: endDate,
        },
      });

      setData(res.data);
    } catch {
      alert("Error al cargar reporte");
    }
  };

  const exportToExcel = () => {
    if (!data) return;

    const ws = XLSX.utils.json_to_sheet(data.sales);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Ventas");

    const excelBuffer = XLSX.write(wb, { bookType: "xlsx", type: "array" });

    const blob = new Blob([excelBuffer], {
      type: "application/octet-stream",
    });

    saveAs(blob, "reporte.xlsx");
  };

  return (
    <div>

      <h1 className="text-2xl font-bold text-orange-500 mb-6">
        Reportes
      </h1>

      {/* FILTROS */}
      <div className="bg-[#1e293b] p-4 rounded-xl mb-6 flex gap-4">

        <input
          type="date"
          className="p-2 rounded bg-[#020617] text-white"
          value={startDate}
          onChange={(e) => setStartDate(e.target.value)}
        />

        <input
          type="date"
          className="p-2 rounded bg-[#020617] text-white"
          value={endDate}
          onChange={(e) => setEndDate(e.target.value)}
        />

        <button
          onClick={fetchReport}
          className="bg-orange-500 px-4 rounded font-bold"
        >
          Buscar
        </button>

        {/* EXPORTAR */}
        <button
          onClick={exportToExcel}
          className="bg-green-500 px-4 rounded font-bold"
        >
          Exportar Excel
        </button>

      </div>

      {/* RESUMEN */}
      {data && (
        <div className="grid grid-cols-2 gap-4 mb-6">

          <div className="bg-[#1e293b] p-4 rounded-xl">
            <h2 className="text-gray-400">Ventas</h2>
            <p className="text-xl font-bold">{data.count}</p>
          </div>

          <div className="bg-[#1e293b] p-4 rounded-xl">
            <h2 className="text-gray-400">Total</h2>
            <p className="text-xl font-bold text-green-400">
              ${data.total}
            </p>
          </div>

        </div>
      )}

      {/* TABLA */}
      {data && (
        <div className="bg-[#1e293b] rounded-xl overflow-hidden">
          <table className="w-full text-sm">

            <thead className="bg-[#020617] text-gray-400">
              <tr>
                <th className="p-3 text-left">ID</th>
                <th className="p-3 text-left">Total</th>
                <th className="p-3 text-left">Fecha</th>
              </tr>
            </thead>

            <tbody>
              {data.sales.map((s) => (
                <tr key={s.id} className="border-t border-gray-700">
                  <td className="p-3">{s.id}</td>
                  <td className="p-3">${s.total}</td>
                  <td className="p-3">
                    {new Date(s.date).toLocaleString()}
                  </td>
                </tr>
              ))}
            </tbody>

          </table>
        </div>
      )}

    </div>
  );
}