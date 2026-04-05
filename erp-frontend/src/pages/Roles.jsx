import { useEffect, useState } from "react";
import api from "../api/api";

export default function Roles() {
  const [roles, setRoles] = useState([]);
  const [permissions, setPermissions] = useState([]);
  const [selectedRole, setSelectedRole] = useState(null);
  const [selectedPermissions, setSelectedPermissions] = useState([]);
  const [loading, setLoading] = useState(false);

  // 🔄 cargar datos
  const fetchData = async () => {
    try {
      const rolesRes = await api.get("/users/roles");
      const permRes = await api.get("/users/permissions");

      setRoles(rolesRes.data);
      setPermissions(permRes.data);
    } catch (err) {
      console.error(err);
      alert("Error cargando datos");
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  // 🎯 seleccionar rol
  const handleSelectRole = (role) => {
    setSelectedRole(role);

    // 🔥 cargar permisos actuales del rol
    const current = role.permissions?.map((p) => p.id) || [];
    setSelectedPermissions(current);
  };

  // 🔄 toggle (forma segura)
  const togglePermission = (id) => {
    setSelectedPermissions((prev) =>
      prev.includes(id)
        ? prev.filter((p) => p !== id)
        : [...prev, id]
    );
  };

  // 💾 guardar
  const save = async () => {
    if (!selectedRole) return;

    try {
      setLoading(true);

      await api.post(
        `/users/roles/${selectedRole.id}/permissions`,
        selectedPermissions
      );

      alert("Permisos actualizados 🔥");

      // 🔄 refrescar datos (PRO)
      fetchData();
    } catch (err) {
      console.error(err);
      alert("Error al guardar");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>

      <h1 className="text-2xl font-bold text-orange-500 mb-6">
        Roles y Permisos
      </h1>

      {/* ROLES */}
      <div className="flex gap-3 mb-6 flex-wrap">
        {roles.map((r) => (
          <button
            key={r.id}
            onClick={() => handleSelectRole(r)}
            className={`px-4 py-2 rounded font-semibold 
              ${
                selectedRole?.id === r.id
                  ? "bg-orange-500"
                  : "bg-[#1e293b] hover:bg-[#334155]"
              }`}
          >
            {r.name}
          </button>
        ))}
      </div>

      {/* PERMISOS */}
      {selectedRole && (
        <div className="bg-[#1e293b] p-6 rounded-xl">

          <h2 className="mb-4 text-gray-400">
            Permisos de {selectedRole.name}
          </h2>

          <div className="grid grid-cols-2 gap-3">

            {permissions.map((p) => (
              <label
                key={p.id}
                className="flex items-center gap-2 bg-[#020617] p-2 rounded cursor-pointer hover:bg-[#334155]"
              >
                <input
                  type="checkbox"
                  checked={selectedPermissions.includes(p.id)}
                  onChange={() => togglePermission(p.id)}
                />
                <span className="text-sm">{p.code}</span>
              </label>
            ))}

          </div>

          <button
            onClick={save}
            disabled={loading}
            className="mt-6 bg-orange-500 px-6 py-2 rounded font-bold hover:bg-orange-600 disabled:opacity-50"
          >
            {loading ? "Guardando..." : "Guardar cambios"}
          </button>

        </div>
      )}
    </div>
  );
}