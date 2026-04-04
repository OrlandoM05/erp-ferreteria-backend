import logo from "../assets/logo.png";

export default function Dashboard() {
  return (
    <div>

      <div className="flex items-center gap-4 mb-6">
        <img src={logo} alt="logo" className="w-20" />
        <div>
          <h1 className="text-2xl font-bold text-orange-500">
            Ferretería y Tlapalería La Unión
          </h1>
          <p className="text-gray-400 text-sm">
            Sistema ERP
          </p>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-6">

        <div className="bg-[#1e293b] p-4 rounded-xl">
          <h2 className="text-gray-400">Ventas hoy</h2>
          <p className="text-2xl font-bold text-orange-500">$0</p>
        </div>

        <div className="bg-[#1e293b] p-4 rounded-xl">
          <h2 className="text-gray-400">Inventario bajo</h2>
          <p className="text-2xl font-bold text-red-400">0</p>
        </div>

        <div className="bg-[#1e293b] p-4 rounded-xl">
          <h2 className="text-gray-400">Ganancia</h2>
          <p className="text-2xl font-bold text-green-400">$0</p>
        </div>

      </div>
    </div>
  );
}