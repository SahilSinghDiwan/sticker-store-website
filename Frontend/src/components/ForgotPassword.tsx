import { useState } from "react";
import { Link } from "react-router-dom";
import { Button } from "./ui/button";

export default function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setMessage(
        "If an account exists with this email, you will receive a password reset link."
      );
    } catch {
      setMessage("An error occurred. Please try again.");
    }
  };

  return (
    <div className="auth-studio">
      <aside className="auth-brand">
        <div className="auth-brand-inner">
          <h1 className="font-display text-[length:var(--text-display)] leading-[1.05] m-0 text-[var(--color-accent-ink)]">
            Sticker Shop
          </h1>
          <p className="mt-[var(--space-md)] text-[var(--text-md)] max-w-sm opacity-90">
            We’ll send a reset link if that email is on file.
          </p>
        </div>
      </aside>
      <section className="auth-panel">
        <div className="auth-card">
          <h2 className="font-display text-[length:var(--text-2xl)] m-0 mb-[var(--space-md)]">
            Reset password
          </h2>

          {message && (
            <div className="mb-[var(--space-sm)] p-[var(--space-xs)] rounded-[var(--radius-input)] bg-[var(--color-wash)] text-[var(--color-ink)] text-[var(--text-sm)]">
              {message}
            </div>
          )}

          <form onSubmit={handleSubmit}>
            <div className="field">
              <label htmlFor="email">Email</label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            <Button type="submit" fullWidth>
              Send reset link
            </Button>
          </form>

          <p className="mt-[var(--space-lg)] text-[var(--text-sm)]">
            <Link to="/login" className="text-[var(--color-accent)]">
              Back to sign in
            </Link>
          </p>
        </div>
      </section>
    </div>
  );
}
