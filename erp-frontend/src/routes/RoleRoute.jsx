import { Navigate } from "react-router-dom";
import useAuth from "../hooks/useAuth";

export default function RoleRoute({ children, roles }) {
  const { user } = useAuth();

  // 🔄 Mientras carga el user
  if (user === undefined) return null;

  // 🔐 No autenticado
  if (!user) {
    return <Navigate to="/login" />;
  }

  // ✅ Normalizar roles (evita errores por mayúsculas/minúsculas)
  const userRole = user.role?.toLowerCase().trim();
  const allowedRoles = roles.map(r => r.toLowerCase().trim());

  // 🚫 Sin permiso
  if (!allowedRoles.includes(userRole)) {
    return <Navigate to="/" />;
  }

  return children;
}