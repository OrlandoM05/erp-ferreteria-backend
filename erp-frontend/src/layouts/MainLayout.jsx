import { Link } from "react-router-dom";
import BranchSelector from "../components/BranchSelector";
import useAuth from "../hooks/useAuth";
import usePermissions from "../hooks/usePermissions";

export default function MainLayout({ children }) {
  const { user } = useAuth();
  const { hasPermission } = usePermissions();

  return (
    <div className="flex h-screen bg-[#0f172a] text-[#e2e8f0]">

      {/* Sidebar */}
      <aside className="w-64 bg-[#020617] border-r border-[#1e293b] p-4">
        <h1 className="text-xl font-bold text-orange-500 mb-6">
          ERP Ferretería
        </h1>

        <nav className="flex flex-col gap-3 text-sm">

          <Link to="/" className="hover:text-orange-400">
            Dashboard
          </Link>

          {hasPermission("products:view") && (
            <Link to="/products" className="hover:text-orange-400">
              Productos
            </Link>
          )}

          {hasPermission("inventory:view") && (
            <Link to="/inventory" className="hover:text-orange-400">
              Inventario
            </Link>
          )}

          {hasPermission("sales:create") && (
            <Link to="/sales" className="hover:text-orange-400">
              Ventas
            </Link>
          )}

          {hasPermission("purchases:create") && (
            <Link to="/purchases" className="hover:text-orange-400">
              Compras
            </Link>
          )}

          {hasPermission("reports:view") && (
            <Link to="/reports" className="hover:text-orange-400">
              Reportes
            </Link>
          )}

          {hasPermission("users:manage") && (
            <Link to="/users" className="hover:text-orange-400">
              Usuarios
            </Link>
          )}

          {hasPermission("roles:manage") && (
            <Link to="/roles" className="hover:text-orange-400">
              Roles
            </Link>
          )}

        </nav>
      </aside>

      {/* Main */}
      <div className="flex-1 flex flex-col">

        {/* Topbar */}
        <header className="h-16 border-b border-[#1e293b] flex items-center justify-between px-6">
          
          {/* IZQUIERDA */}
          <span className="text-sm text-gray-400">
            Sistema ERP - Ferretería
          </span>

          {/* DERECHA */}
          <div className="flex items-center gap-4">

            {/* Selector de sucursal */}
            <BranchSelector />

            {/* 👤 Rol dinámico */}
            <span className="text-sm text-gray-400">
              {user?.role || "Cargando..."}
            </span>

            {/* 🔥 Logout */}
            <button
              onClick={() => {
                localStorage.removeItem("token");
                window.location.href = "/login";
              }}
              className="text-red-400 text-sm hover:text-red-300"
            >
              Logout
            </button>

            {/* Avatar */}
            <div className="w-8 h-8 bg-orange-500 rounded-full" />

          </div>

        </header>

        {/* Content */}
        <main className="p-6 overflow-y-auto">
          {children}
        </main>

      </div>
    </div>
  );
}