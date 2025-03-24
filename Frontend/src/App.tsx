import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { SnackbarProvider } from "notistack";
import { ThemeProvider } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import { AuthProvider } from "./lib/auth-context";
import { ProtectedRoute } from "./components/ProtectedRoute";
import theme from "./theme";

// Public components
import Login from "./components/Login.tsx";
import Signup from "./components/Signup.tsx";
import ForgotPassword from "./components/ForgotPassword.tsx";
import ResetPassword from "./components/ResetPassword.tsx";

// Protected components
import Layout from "./components/Layout";
import Home from "./components/Home";
import Profile from "./components/Profile";
import Cart from "./components/Cart";
import Checkout from "./components/Checkout";
import OrderHistory from "./components/OrderHistory";

// Admin components
import AdminLayout from "./components/admin/AdminLayout";
import ProductManagement from "./components/admin/ProductManagement";
import OrderManagement from "./components/admin/OrderManagement";
import UserManagement from "./components/admin/UserManagement";
import AnalyticsDashboard from "./components/admin/AnalyticsDashboard";

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <SnackbarProvider maxSnack={3}>
        <AuthProvider>
          <Router>
            <Routes>
              {/* Public Routes */}
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Signup />} />
              <Route path="/forgot-password" element={<ForgotPassword />} />
              <Route path="/reset-password" element={<ResetPassword />} />

              {/* Protected Customer Routes */}
              <Route element={<ProtectedRoute />}>
                <Route element={<Layout />}>
                  <Route path="/" element={<Home />} />
                  <Route path="/profile" element={<Profile />} />
                  <Route path="/cart" element={<Cart />} />
                  <Route path="/checkout" element={<Checkout />} />
                  <Route path="/orders" element={<OrderHistory />} />
                </Route>
              </Route>

              {/* Protected Admin Routes */}
              <Route element={<ProtectedRoute requireAdmin />}>
                <Route element={<AdminLayout />}>
                  <Route path="/admin" element={<AnalyticsDashboard />} />
                  <Route
                    path="/admin/products"
                    element={<ProductManagement />}
                  />
                  <Route path="/admin/orders" element={<OrderManagement />} />
                  <Route path="/admin/users" element={<UserManagement />} />
                  <Route
                    path="/admin/analytics"
                    element={<AnalyticsDashboard />}
                  />
                </Route>
              </Route>
            </Routes>
          </Router>
        </AuthProvider>
      </SnackbarProvider>
    </ThemeProvider>
  );
}

export default App;
