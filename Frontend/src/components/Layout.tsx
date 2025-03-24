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
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo and main navigation */}
            <div className="flex items-center">
              <Link to="/" className="text-xl font-bold text-gray-900">
                Sticker Shop
              </Link>
              <nav className="hidden md:ml-8 md:flex space-x-4">
                <Link
                  to="/"
                  className="text-gray-500 hover:text-gray-900 px-3 py-2 rounded-md"
                >
                  Shop
                </Link>
                <Link
                  to="/orders"
                  className="text-gray-500 hover:text-gray-900 px-3 py-2 rounded-md"
                >
                  Orders
                </Link>
                {user?.role === "admin" && (
                  <Link
                    to="/admin"
                    className="text-gray-500 hover:text-gray-900 px-3 py-2 rounded-md"
                  >
                    Admin
                  </Link>
                )}
              </nav>
            </div>

            {/* Right side navigation */}
            <div className="flex items-center space-x-4">
              <Link
                to="/cart"
                className="text-gray-500 hover:text-gray-900 p-2 rounded-md"
              >
                <ShoppingCart className="h-6 w-6" />
              </Link>
              <Link
                to="/profile"
                className="text-gray-500 hover:text-gray-900 px-3 py-2 rounded-md"
              >
                Profile
              </Link>
              <Button variant="ghost" onClick={handleLogout}>
                Logout
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="bg-white border-t">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center text-gray-500">
            <p>&copy; 2024 Sticker Shop. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
