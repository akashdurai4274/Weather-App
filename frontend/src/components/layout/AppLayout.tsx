import { Outlet, Navigate } from "react-router-dom";
import { useAppSelector } from "@/app/hooks";
import { Header } from "./Header";

export function AppLayout() {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      <main className="container py-6">
        <Outlet />
      </main> 
    </div>
  );
}

export function ProtectedRoute() {
  const { isAuthenticated } = useAppSelector((state) => state.auth);

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return <Outlet />;
}
