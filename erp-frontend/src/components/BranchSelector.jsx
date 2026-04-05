import { useState } from "react";

export default function BranchSelector() {
  const [branch, setBranch] = useState(1);

  const changeBranch = (id) => {
    setBranch(id);
    localStorage.setItem("branch_id", id);
  };

  return (
    <select
      className="bg-[#020617] text-white p-2 rounded"
      value={branch}
      onChange={(e) => changeBranch(e.target.value)}
    >
      <option value={1}>Sucursal Centro</option>
      <option value={2}>Sucursal Norte</option>
    </select>
  );
}