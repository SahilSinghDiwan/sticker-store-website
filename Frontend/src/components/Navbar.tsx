import { Link } from "react-router-dom";
import { useAuth } from "../lib/auth-context";
import { Button } from "./ui/button";

/** Legacy shell — prefer Layout.tsx. Kept for compatibility. */
export default function Navbar() {
  const { user, logout } = useAuth();

  return (
    <nav className="nav-pill !static !mt-0 !mb-[var(--space-md)]">
      <Link to="/" className="wordmark">
        Sticker Shop
      </Link>

      <div className="flex items-center gap-1 flex-wrap">
        {user ? (
          <>
            <Link to="/cart" className="nav-link">
              Cart
            </Link>
            <Link to="/orders" className="nav-link">
              Orders
            </Link>
            <Link to="/profile" className="nav-link">
              Profile
            </Link>
            {user.role === "admin" && (
              <Link to="/admin" className="nav-link">
                Admin
              </Link>
            )}
            <Button variant="ghost" size="sm" onClick={logout}>
              Logout
            </Button>
          </>
        ) : (
          <>
            <Link to="/login">
              <Button variant="outline" size="sm">
                Login
              </Button>
            </Link>
            <Link to="/register">
              <Button size="sm">Sign up</Button>
            </Link>
          </>
        )}
      </div>
    </nav>
  );
}
