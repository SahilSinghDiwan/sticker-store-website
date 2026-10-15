import { useState } from "react";
import { Button } from "./ui/button";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../lib/auth-context";

const Signup = () => {
  const [formData, setFormData] = useState({
    firstName: "",
    lastName: "",
    email: "",
    phoneNumber: "",
    password: "",
    confirmPassword: "",
  });
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const { signup } = useAuth();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (!formData.firstName || !formData.lastName) {
      setError("First name and last name are required");
      return;
    }

    if (!formData.email) {
      setError("Email is required");
      return;
    }

    if (!formData.phoneNumber) {
      setError("Phone number is required");
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    if (formData.password.length < 6) {
      setError("Password must be at least 6 characters long");
      return;
    }

    const success = await signup(formData.email, formData.password, {
      firstName: formData.firstName,
      lastName: formData.lastName,
      phoneNumber: formData.phoneNumber,
    });

    if (success) {
      navigate("/login");
    } else {
      setError(
        "This email is already registered. Please use a different email."
      );
    }
  };

  return (
    <div className="auth-studio">
      <aside className="auth-brand">
        <div className="auth-brand-inner">
          <p className="font-mono text-[var(--text-xs)] uppercase tracking-[0.1em] mb-[var(--space-sm)] opacity-80">
            Join the studio
          </p>
          <h1 className="font-display text-[length:var(--text-display)] leading-[1.05] m-0 text-[var(--color-accent-ink)]">
            Sticker Shop
          </h1>
          <p className="mt-[var(--space-md)] text-[var(--text-md)] max-w-sm opacity-90">
            Create an account to collect stickers, track orders, and keep your
            cart across sessions.
          </p>
        </div>
      </aside>

      <section className="auth-panel">
        <div className="auth-card">
          <h2 className="font-display text-[length:var(--text-2xl)] m-0 mb-[var(--space-md)]">
            Sign up
          </h2>

          {error && <div className="form-error">{error}</div>}

          <form onSubmit={handleSubmit}>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-[var(--space-sm)]">
              <div className="field">
                <label htmlFor="firstName">First name</label>
                <input
                  id="firstName"
                  name="firstName"
                  type="text"
                  value={formData.firstName}
                  onChange={handleChange}
                  required
                />
              </div>
              <div className="field">
                <label htmlFor="lastName">Last name</label>
                <input
                  id="lastName"
                  name="lastName"
                  type="text"
                  value={formData.lastName}
                  onChange={handleChange}
                  required
                />
              </div>
            </div>

            <div className="field">
              <label htmlFor="email">Email</label>
              <input
                id="email"
                name="email"
                type="email"
                value={formData.email}
                onChange={handleChange}
                required
              />
            </div>

            <div className="field">
              <label htmlFor="phoneNumber">Phone</label>
              <input
                id="phoneNumber"
                name="phoneNumber"
                type="tel"
                value={formData.phoneNumber}
                onChange={handleChange}
                required
              />
            </div>

            <div className="field">
              <label htmlFor="password">Password</label>
              <input
                id="password"
                name="password"
                type="password"
                value={formData.password}
                onChange={handleChange}
                required
              />
            </div>

            <div className="field">
              <label htmlFor="confirmPassword">Confirm password</label>
              <input
                id="confirmPassword"
                name="confirmPassword"
                type="password"
                value={formData.confirmPassword}
                onChange={handleChange}
                required
              />
            </div>

            <Button type="submit" fullWidth>
              Create account
            </Button>
          </form>

          <p className="mt-[var(--space-lg)] text-[var(--text-sm)] text-[var(--color-ink-2)]">
            Already have an account?{" "}
            <Link to="/login" className="font-medium text-[var(--color-accent)]">
              Sign in
            </Link>
          </p>
        </div>
      </section>
    </div>
  );
};

export default Signup;
