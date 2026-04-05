import { useEffect, useState } from "react";
import api from "../api/api";

export default function useAuth() {
  const [user, setUser] = useState(undefined); // 🔥 CLAVE

  const fetchUser = async () => {
    try {
      const res = await api.get("/users/me");
      setUser(res.data);
    } catch {
      setUser(null);
    }
  };

  useEffect(() => {
    fetchUser();
  }, []);

  return { user };
}