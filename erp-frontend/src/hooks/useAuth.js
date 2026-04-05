import { useEffect, useState } from "react";
import api from "../api/api";

export default function useAuth() {
  const [user, setUser] = useState(undefined); // undefined = loading
  const [loading, setLoading] = useState(true); // 🔥 NUEVO

  const fetchUser = async () => {
    try {
      const res = await api.get("/users/me");
      setUser(res.data);
    } catch {
      setUser(null);
    } finally {
      setLoading(false); // 🔥 CLAVE
    }
  };

  useEffect(() => {
    fetchUser();
  }, []);

  return { user, loading };
}