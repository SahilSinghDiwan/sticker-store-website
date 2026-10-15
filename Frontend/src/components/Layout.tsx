import { Outlet, Link, useNavigate } from "react-router-dom";
import { useAuth } from "../lib/auth-context";
import { Button } from "./ui/button";
import { ShoppingCart } from "lucide-react";

export default function Layout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div className="shop-shell">
      <header className="nav-pill">
        <Link to="/" className="wordmark">
          Sticker Shop
        </Link>

        <nav className="flex items-center gap-1 flex-wrap justify-end">
          <Link to="/" className="nav-link">
            Shop
          </Link>
          <Link to="/orders" className="nav-link">
            Orders
          </Link>
          {user?.role === "admin" && (
            <Link to="/admin" className="nav-link">
              Admin
            </Link>
          )}
          <Link
            to="/cart"
            className="nav-link inline-flex items-center gap-1"
            aria-label="Cart"
          >
            <ShoppingCart className="h-4 w-4" />
            Cart
          </Link>
          <Link to="/profile" className="nav-link">
            Profile
          </Link>
          <Button variant="ghost" size="sm" onClick={handleLogout}>
            Logout
          </Button>
        </nav>
      </header>

      <main className="page-frame">
        <Outlet />
      </main>

      <footer className="colophon">
        <span>Sticker Shop · print studio</span>
        <span>© {new Date().getFullYear()}</span>
      </footer>
    </div>
  );
}
