import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from "../pages/Dashboard";
import Login from "../pages/Login";
import MainLayout from "../layouts/MainLayout";
import ProtectedRoute from "./ProtectedRoute";
import RoleRoute from "./RoleRoute"; // 🔥 NUEVO
import Products from "../pages/Products";
import Sales from "../pages/Sales";
import Inventory from "../pages/Inventory";
import Purchases from "../pages/Purchases";
import Reports from "../pages/Reports";

export default function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>

        {/* 🔓 Login */}
        <Route path="/login" element={<Login />} />

        {/* 🔐 Sistema protegido */}
        <Route
          path="/*"
          element={
            <ProtectedRoute>
              <MainLayout>
                <Routes>

                  <Route path="/" element={<Dashboard />} />

                  <Route path="/products" element={<Products />} />

                  <Route path="/sales" element={<Sales />} />

                  <Route path="/inventory" element={<Inventory />} />

                  {/* 🔐 SOLO ADMIN */}
                  <Route
                    path="/purchases"
                    element={
                      <RoleRoute roles={["Admin"]}>
                        <Purchases />
                      </RoleRoute>
                    }
                  />

                  {/* 🔐 ADMIN + GERENTE */}
                  <Route
                    path="/reports"
                    element={
                      <RoleRoute roles={["Admin", "Gerente"]}>
                        <Reports />
                      </RoleRoute>
                    }
                  />

                </Routes>
              </MainLayout>
            </ProtectedRoute>
          }
        />

      </Routes>
    </BrowserRouter>
  );
}