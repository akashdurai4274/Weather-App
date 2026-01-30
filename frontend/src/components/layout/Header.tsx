import { useState } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { useAppDispatch, useAppSelector } from "@/app/hooks";
import { logout } from "@/features/auth/authSlice";
import { Button } from "../ui/button";

export function Header() {
  const [mobileOpen, setMobileOpen] = useState(false);
  const dispatch = useAppDispatch();
  const navigate = useNavigate();
  const location = useLocation();
  const { isAuthenticated, username, role } = useAppSelector((state) => state.auth);

  const handleLogout = () => {
    dispatch(logout());
    setMobileOpen(false);
    navigate("/login");
  };

  const navTo = (path: string) => {
    setMobileOpen(false);
    navigate(path);
  };

  const isActive = (path: string) => location.pathname === path;

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-14 items-center justify-between px-4">
        <Link to="/" className="flex items-center space-x-2" onClick={() => setMobileOpen(false)}>
          <span className="text-lg sm:text-xl font-bold whitespace-nowrap">Weather Monitor</span>
        </Link>

        {/* Desktop nav */}
        <nav className="hidden md:flex items-center space-x-2 lg:space-x-4">
          {isAuthenticated ? (
            <>
              <Link to="/">
                <Button variant={isActive("/") ? "secondary" : "ghost"} size="sm">Home</Button>
              </Link>
              <Link to="/search">
                <Button variant={isActive("/search") ? "secondary" : "ghost"} size="sm">Search</Button>
              </Link>
              <Link to="/watchlist">
                <Button variant={isActive("/watchlist") ? "secondary" : "ghost"} size="sm">Watchlist</Button>
              </Link>
              <span className="text-sm text-muted-foreground truncate max-w-[120px]">
                {username}
                {role === "ADMIN" && (
                  <span className="ml-1.5 inline-flex items-center rounded-full bg-purple-100 px-2 py-0.5 text-xs font-medium text-purple-700">
                    Admin
                  </span>
                )}
              </span>
              <Button variant="outline" size="sm" onClick={handleLogout}>Logout</Button>
            </>
          ) : (
            <>
              <Link to="/login">
                <Button variant="ghost" size="sm">Login</Button>
              </Link>
              <Link to="/signup">
                <Button size="sm">Sign Up</Button>
              </Link>
            </>
          )}
        </nav>

        {/* Mobile hamburger */}
        <button
          className="md:hidden p-2 rounded-md hover:bg-muted transition-colors"
          onClick={() => setMobileOpen(!mobileOpen)}
          aria-label="Toggle menu"
        >
          <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            {mobileOpen ? (
              <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
            ) : (
              <path strokeLinecap="round" strokeLinejoin="round" d="M4 6h16M4 12h16M4 18h16" />
            )}
          </svg>
        </button>
      </div>

      {/* Mobile menu */}
      {mobileOpen && (
        <div className="md:hidden border-t bg-background animate-slide-down">
          <div className="container px-4 py-3 space-y-2">
            {isAuthenticated ? (
              <>
                <div className="flex items-center gap-2 pb-2 mb-2 border-b">
                  <span className="text-sm font-medium truncate">{username}</span>
                  {role === "ADMIN" && (
                    <span className="inline-flex items-center rounded-full bg-purple-100 px-2 py-0.5 text-xs font-medium text-purple-700">
                      Admin
                    </span>
                  )}
                </div>
                <button
                  onClick={() => navTo("/")}
                  className={`block w-full text-left px-3 py-2 rounded-md text-sm ${isActive("/") ? "bg-secondary font-medium" : "hover:bg-muted"}`}
                >
                  Home
                </button>
                <button
                  onClick={() => navTo("/search")}
                  className={`block w-full text-left px-3 py-2 rounded-md text-sm ${isActive("/search") ? "bg-secondary font-medium" : "hover:bg-muted"}`}
                >
                  Search
                </button>
                <button
                  onClick={() => navTo("/watchlist")}
                  className={`block w-full text-left px-3 py-2 rounded-md text-sm ${isActive("/watchlist") ? "bg-secondary font-medium" : "hover:bg-muted"}`}
                >
                  Watchlist
                </button>
                <div className="pt-2 border-t">
                  <Button variant="outline" size="sm" className="w-full" onClick={handleLogout}>
                    Logout
                  </Button>
                </div>
              </>
            ) : (
              <>
                <button
                  onClick={() => navTo("/login")}
                  className="block w-full text-left px-3 py-2 rounded-md text-sm hover:bg-muted"
                >
                  Login
                </button>
                <button
                  onClick={() => navTo("/signup")}
                  className="block w-full text-left px-3 py-2 rounded-md text-sm hover:bg-muted font-medium"
                >
                  Sign Up
                </button>
              </>
            )}
          </div>
        </div>
      )}
    </header>
  );
}
