export default function Dashboard() {
  return (
    <div className="grid grid-cols-3 gap-6">
      
      <div className="bg-[#1e293b] p-4 rounded-xl shadow">
        <h2 className="text-gray-400">Ventas hoy</h2>
        <p className="text-2xl font-bold text-orange-500">$0</p>
      </div>

      <div className="bg-[#1e293b] p-4 rounded-xl shadow">
        <h2 className="text-gray-400">Inventario bajo</h2>
        <p className="text-2xl font-bold text-red-400">0</p>
      </div>

      <div className="bg-[#1e293b] p-4 rounded-xl shadow">
        <h2 className="text-gray-400">Ganancia</h2>
        <p className="text-2xl font-bold text-green-400">$0</p>
      </div>

    </div>
  );
}