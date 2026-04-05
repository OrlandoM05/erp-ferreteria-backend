import useAuth from "./useAuth";

export default function usePermissions() {
  const { user } = useAuth();

  const hasPermission = (code) => {
    // 🔥 SUPER ADMIN (modo dios)
    if (user?.role === "Admin") return true;

    if (!user || !user.permissions) return false;

    return user.permissions.includes(code);
  };

  return { hasPermission };
}