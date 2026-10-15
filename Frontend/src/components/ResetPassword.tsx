import React, { useState } from "react";
import { useNavigate, useSearchParams, Link } from "react-router-dom";
import { Button } from "./ui/button";

export default function ResetPassword() {
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const token = searchParams.get("token");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    if (password.length < 6) {
      setError("Password must be at least 6 characters long");
      return;
    }

    try {
      navigate("/login");
    } catch {
      setError("Failed to reset password. Please try again.");
    }
  };

  if (!token) {
    return (
      <div className="auth-panel min-h-screen">
        <div className="auth-card">
          <p className="form-error">
            Invalid or expired reset link. Please request a new one.
          </p>
          <Link to="/forgot-password" className="text-[var(--color-accent)]">
            Request a new link
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="auth-studio">
      <aside className="auth-brand">
        <div className="auth-brand-inner">
          <h1 className="font-display text-[length:var(--text-display)] leading-[1.05] m-0 text-[var(--color-accent-ink)]">
            Sticker Shop
          </h1>
        </div>
      </aside>
      <section className="auth-panel">
        <div className="auth-card">
          <h2 className="font-display text-[length:var(--text-2xl)] m-0 mb-[var(--space-md)]">
            New password
          </h2>

          {error && <div className="form-error">{error}</div>}

          <form onSubmit={handleSubmit}>
            <div className="field">
              <label htmlFor="password">New password</label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            <div className="field">
              <label htmlFor="confirmPassword">Confirm password</label>
              <input
                id="confirmPassword"
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
              />
            </div>
            <Button type="submit" fullWidth>
              Reset password
            </Button>
          </form>
        </div>
      </section>
    </div>
  );
}
