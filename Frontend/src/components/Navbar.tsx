import { Link } from "react-router-dom";
import { useAuth } from "../lib/auth-context";
import { Button } from "./ui/button";

export default function Navbar() {
  const { user, logout } = useAuth();

  return (
    <nav className="bg-white shadow-sm">
      <div className="container mx-auto px-4">
        <div className="flex h-16 justify-between items-center">
          <Link to="/" className="text-xl font-bold text-gray-800">
            Sticker Shop
          </Link>

          <div className="flex items-center gap-4">
            {user ? (
              <>
                <Link to="/cart" className="text-gray-600 hover:text-gray-900">
                  Cart
                </Link>
                <Link
                  to="/orders"
                  className="text-gray-600 hover:text-gray-900"
                >
                  Orders
                </Link>
                <Link
                  to="/profile"
                  className="text-gray-600 hover:text-gray-900"
                >
                  Profile
                </Link>
                {user.role === "admin" && (
                  <Link
                    to="/admin"
                    className="text-gray-600 hover:text-gray-900"
                  >
                    Admin
                  </Link>
                )}
                <Button variant="outline" onClick={logout}>
                  Logout
                </Button>
              </>
            ) : (
              <>
                <Link to="/login">
                  <Button variant="outline">Login</Button>
                </Link>
                <Link to="/register">
                  <Button>Sign Up</Button>
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
