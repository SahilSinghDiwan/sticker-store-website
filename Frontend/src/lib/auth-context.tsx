import {
  createContext,
  useContext,
  useState,
  useEffect,
  ReactNode,
} from "react";
import { api } from "./api";
import { useNavigate } from "react-router-dom";
import { useSnackbar } from "notistack";
import { authService } from "../services/auth";

export interface User {
  _id: string;
  email: string;
  firstName?: string;
  lastName?: string;
  role: "user" | "admin";
  phoneNumber: string;
}

interface AuthResponse {
  user: User;
  token: string;
  refreshToken: string;
}

interface RefreshResponse {
  token: string;
}

interface ProfileResponse {
  user: User;
}

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<boolean>;
  loginWithGoogle: (credential: string) => Promise<void>;
  signup: (
    email: string,
    password: string,
    userData: Partial<User>
  ) => Promise<boolean>;
  logout: () => void;
  updateProfile: (data: Partial<User>) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const TOKEN_REFRESH_INTERVAL = 14 * 60 * 1000; // 14 minutes

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const { enqueueSnackbar } = useSnackbar();
  const navigate = useNavigate();

  // Set up axios interceptor for token refresh
  useEffect(() => {
    let refreshInterval: NodeJS.Timeout;

    const setupTokenRefresh = () => {
      refreshInterval = setInterval(async () => {
        try {
          const refreshToken = localStorage.getItem("refreshToken");
          if (!refreshToken) return;

          const response = await api.post("/auth/refresh", { refreshToken });
          const { token } = response.data as RefreshResponse;
          localStorage.setItem("token", token);
        } catch (error) {
          console.error("Token refresh failed:", error);
          handleLogout();
        }
      }, TOKEN_REFRESH_INTERVAL);
    };

    // Check for existing token and validate
    const initializeAuth = async () => {
      const token = localStorage.getItem("token");
      if (!token) {
        setIsLoading(false);
        return;
      }

      try {
        const response = await api.get("/auth/me");
        const { user } = response.data as { user: User };
        setUser(user);
        setupTokenRefresh();
      } catch (error) {
        console.error("Session validation failed:", error);
        handleLogout();
      } finally {
        setIsLoading(false);
      }
    };

    initializeAuth();

    return () => {
      if (refreshInterval) {
        clearInterval(refreshInterval);
      }
    };
  }, []);

  const handleAuthResponse = ({ user, token, refreshToken }: AuthResponse) => {
    localStorage.setItem("token", token);
    localStorage.setItem("refreshToken", refreshToken);
    setUser(user);
  };

  const login = async (email: string, password: string): Promise<boolean> => {
    try {
      const response = await authService.login({ email, password });
      setUser(response.user);
      localStorage.setItem("token", response.token);
      return true;
    } catch (error) {
      console.error("Login failed:", error);
      return false;
    }
  };

  const loginWithGoogle = async (credential: string) => {
    setIsLoading(true);
    try {
      const response = await api.post("/auth/google", { credential });
      const data = response.data as AuthResponse;
      handleAuthResponse(data);
      enqueueSnackbar("Successfully logged in with Google", {
        variant: "success",
      });
      navigate("/");
    } catch (error) {
      console.error("Google login failed:", error);
      enqueueSnackbar("Failed to login with Google", { variant: "error" });
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const signup = async (
    email: string,
    password: string,
    userData: Partial<User>
  ): Promise<boolean> => {
    try {
      const response = await authService.register({
        email,
        password,
        firstName: userData.firstName || "",
        lastName: userData.lastName || "",
        phoneNumber: userData.phoneNumber || "",
      });
      return true;
    } catch (error) {
      console.error("Signup failed:", error);
      return false;
    }
  };

  const handleLogout = async () => {
    localStorage.removeItem("token");
    localStorage.removeItem("refreshToken");
    setUser(null);
    navigate("/login");
  };

  const logout = () => {
    setUser(null);
    authService.logout();
  };

  const updateProfile = async (data: Partial<User>) => {
    setIsLoading(true);
    try {
      const response = await api.patch("/auth/profile", data);
      const { user } = response.data as ProfileResponse;
      setUser(user);
      enqueueSnackbar("Profile updated successfully", { variant: "success" });
    } catch (error) {
      console.error("Profile update failed:", error);
      enqueueSnackbar("Failed to update profile", { variant: "error" });
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoading,
        login,
        loginWithGoogle,
        signup,
        logout,
        updateProfile,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
