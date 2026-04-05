import { Navigate } from "react-router-dom";
import useAuth from "../hooks/useAuth";

export default function RoleRoute({ children, roles }) {
  const { user } = useAuth();

  if (!user) return null;

  if (!roles.includes(user.role)) {
    return <Navigate to="/" />;
  }

  return children;
}