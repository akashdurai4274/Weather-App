import { Outlet, Navigate } from "react-router-dom";
import { useAppSelector } from "@/app/hooks";
import { getWeatherBgClass } from "@/lib/utils";
import { Header } from "./Header";

export function AppLayout() {
  const { weatherDescription } = useAppSelector((state) => state.weather);
  const bgClass = weatherDescription ? getWeatherBgClass(weatherDescription) : "weather-bg-default";

  return (
    <div className={`min-h-screen weather-bg ${bgClass} bg-fixed bg-cover`}>
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

export function PublicRoute() {
  const { isAuthenticated } = useAppSelector((state) => state.auth);

  if (isAuthenticated) {
    return <Navigate to="/" replace />;
  }

  return <Outlet />;
}
