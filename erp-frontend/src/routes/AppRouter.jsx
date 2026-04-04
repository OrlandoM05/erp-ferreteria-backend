import { BrowserRouter, Routes, Route } from "react-router-dom";
import Dashboard from "../pages/Dashboard";
import Login from "../pages/Login";
import MainLayout from "../layouts/MainLayout";
import ProtectedRoute from "./ProtectedRoute";
import Products from "../pages/Products";

export default function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>

        {/* Login */}
        <Route path="/login" element={<Login />} />

        {/* Sistema protegido */}
        <Route
          path="/*"
          element={
            <ProtectedRoute>
              <MainLayout>
                <Routes>
                  <Route path="/" element={<Dashboard />} />
                  <Route path="/products" element={<Products />} />
                </Routes>
              </MainLayout>
            </ProtectedRoute>
          }
        />

      </Routes>
    </BrowserRouter>
  );
}