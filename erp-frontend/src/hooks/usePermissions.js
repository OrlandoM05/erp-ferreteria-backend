import useAuth from "./useAuth";

export default function usePermissions() {
  const { user } = useAuth();

  const hasPermission = (code) => {
    return user?.permissions?.includes(code);
  };

  return { hasPermission };
}