import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/api";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      setLoading(true);
      setError("");

      const res = await api.post("/auth/login", {
        email,
        password,
      });

      localStorage.setItem("token", res.data.access_token);

      navigate("/");
    } catch (err) {
      if (err.response?.status === 401) {
        setError("Correo o contraseña incorrectos");
      } else if (err.response?.status === 403) {
        setError("Usuario inactivo");
      } else {
        setError("Error de conexión con el servidor");
      }
    } finally {
      setLoading(false);
    }
  };

  // 👉 Permite presionar ENTER
  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      handleLogin();
    }
  };

  return (
    <div className="h-screen flex items-center justify-center bg-[#0f172a]">

      <div className="bg-[#1e293b] p-8 rounded-2xl shadow-lg w-96">

        <h1 className="text-2xl font-bold text-orange-500 mb-6 text-center">
          ERP Ferretería
        </h1>

        {error && (
          <p className="text-red-400 text-sm mb-4 text-center">{error}</p>
        )}

        <input
          type="email"
          placeholder="Correo"
          className="w-full mb-4 p-3 rounded bg-[#020617] border border-gray-700 text-white"
          onChange={(e) => setEmail(e.target.value)}
          onKeyDown={handleKeyDown}
        />

        <input
          type="password"
          placeholder="Contraseña"
          className="w-full mb-6 p-3 rounded bg-[#020617] border border-gray-700 text-white"
          onChange={(e) => setPassword(e.target.value)}
          onKeyDown={handleKeyDown}
        />

        <button
          onClick={handleLogin}
          disabled={loading}
          className="w-full bg-orange-500 hover:bg-orange-600 p-3 rounded font-bold disabled:opacity-50"
        >
          {loading ? "Cargando..." : "Iniciar sesión"}
        </button>
      </div>
    </div>
  );
}