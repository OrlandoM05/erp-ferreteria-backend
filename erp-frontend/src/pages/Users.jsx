import { useEffect, useState } from "react";
import api from "../api/api";

export default function Users() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [roleId, setRoleId] = useState("");
  const [branchId, setBranchId] = useState(1);
  const [roles, setRoles] = useState([]);

  // 🔄 cargar roles desde backend
  useEffect(() => {
    fetchRoles();
  }, []);

  const fetchRoles = async () => {
    try {
      const res = await api.get("/users/roles");
      setRoles(res.data);
    } catch (err) {
      console.error(err);
      alert("Error cargando roles");
    }
  };

  const handleCreate = async () => {
    if (!email || !password || !roleId) {
      alert("Completa los campos");
      return;
    }

    try {
      await api.post("/users", {
        email,
        password,
        role_id: Number(roleId),
        branch_id: branchId,
      });

      alert("Usuario creado");

      setEmail("");
      setPassword("");
      setRoleId("");
    } catch {
      alert("Error al crear usuario");
    }
  };

  return (
    <div>

      <h1 className="text-2xl font-bold text-orange-500 mb-6">
        Usuarios
      </h1>

      <div className="bg-[#1e293b] p-6 rounded-xl flex flex-col gap-4 max-w-xl">

        <input
          placeholder="Correo"
          className="p-3 rounded bg-[#020617] border border-gray-700 text-white"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          placeholder="Contraseña"
          type="password"
          className="p-3 rounded bg-[#020617] border border-gray-700 text-white"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        {/* 🔥 ROLES DINÁMICOS */}
        <select
          className="p-3 rounded bg-[#020617] text-white"
          value={roleId}
          onChange={(e) => setRoleId(e.target.value)}
        >
          <option value="">Seleccionar rol</option>

          {roles.map((r) => (
            <option key={r.id} value={r.id}>
              {r.name}
            </option>
          ))}

        </select>

        <button
          onClick={handleCreate}
          className="bg-orange-500 p-3 rounded font-bold hover:bg-orange-600"
        >
          Crear usuario
        </button>

      </div>
    </div>
  );
}