import { useState } from "react";
import { Button } from "./ui/button";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../lib/auth-context";
import { GoogleLogin, GoogleOAuthProvider } from "@react-oauth/google";

const googleClientId = import.meta.env.VITE_GOOGLE_CLIENT_ID;

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const { login, loginWithGoogle, isLoading } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    const success = await login(email, password);
    if (success) {
      navigate("/");
    } else {
      setError("Invalid email or password. Please try again.");
    }
  };

  return (
    <div className="auth-studio">
      <aside className="auth-brand" aria-hidden={false}>
        <div className="auth-brand-inner">
          <p className="font-mono text-[var(--text-xs)] uppercase tracking-[0.1em] mb-[var(--space-sm)] opacity-80">
            Print studio
          </p>
          <h1 className="font-display text-[length:var(--text-display)] leading-[1.05] m-0 text-[var(--color-accent-ink)]">
            Sticker Shop
          </h1>
          <p className="mt-[var(--space-md)] text-[var(--text-md)] max-w-sm opacity-90">
            Sign in to browse the rack, fill a cart, and peel something new onto
            the world.
          </p>
        </div>
      </aside>

      <section className="auth-panel">
        <div className="auth-card">
          <h2 className="font-display text-[length:var(--text-2xl)] m-0 mb-[var(--space-md)]">
            Sign in
          </h2>

          {error && <div className="form-error">{error}</div>}

          <form onSubmit={handleSubmit}>
            <div className="field">
              <label htmlFor="email">Email</label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@studio.com"
                required
                autoComplete="email"
              />
            </div>

            <div className="field">
              <label htmlFor="password">Password</label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Your password"
                required
                autoComplete="current-password"
              />
              <div className="text-right">
                <Link
                  to="/forgot-password"
                  className="text-[var(--text-sm)] text-[var(--color-accent)]"
                >
                  Forgot password?
                </Link>
              </div>
            </div>

            <Button type="submit" fullWidth loading={isLoading}>
              Sign in
            </Button>
          </form>

          {googleClientId && (
            <div className="mt-[var(--space-md)]">
              <div className="relative my-[var(--space-md)]">
                <div className="absolute inset-0 flex items-center">
                  <div className="w-full border-t border-[var(--color-rule)]" />
                </div>
                <div className="relative flex justify-center text-[var(--text-xs)]">
                  <span className="bg-[var(--color-paper)] px-2 text-[var(--color-ink-2)] font-mono uppercase tracking-wide">
                    Or continue with
                  </span>
                </div>
              </div>

              <div className="flex justify-center">
                <GoogleOAuthProvider clientId={googleClientId}>
                  <GoogleLogin
                    onSuccess={async (credentialResponse) => {
                      if (credentialResponse.credential) {
                        try {
                          await loginWithGoogle(credentialResponse.credential);
                          navigate("/");
                        } catch {
                          setError("Google login failed. Please try again.");
                        }
                      }
                    }}
                    onError={() => {
                      setError("Google login failed. Please try again.");
                    }}
                    theme="outline"
                    shape="rectangular"
                    size="large"
                    text="signin_with"
                    width="100%"
                  />
                </GoogleOAuthProvider>
              </div>
            </div>
          )}

          <p className="mt-[var(--space-lg)] text-[var(--text-sm)] text-[var(--color-ink-2)]">
            No account?{" "}
            <Link
              to="/signup"
              className="font-medium text-[var(--color-accent)]"
            >
              Sign up
            </Link>
          </p>
        </div>
      </section>
    </div>
  );
};

export default Login;
