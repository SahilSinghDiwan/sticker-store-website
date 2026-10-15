import { useState } from "react";
import { useAuth } from "../lib/auth-context";
import { Button } from "./ui/button";

export default function Profile() {
  const { user } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    firstName: user?.firstName || "",
    lastName: user?.lastName || "",
    phoneNumber: user?.phoneNumber || "",
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsEditing(false);
  };

  return (
    <div className="max-w-xl">
      <h1 className="font-display text-[length:var(--text-display-s)] m-0 mb-[var(--space-lg)]">
        Profile
      </h1>

      <div className="border border-[var(--color-rule)] rounded-[var(--radius-card)] p-[var(--space-md)] bg-[var(--color-paper-2)]">
        {isEditing ? (
          <form onSubmit={handleSubmit}>
            <div className="field">
              <label htmlFor="firstName">First name</label>
              <input
                id="firstName"
                type="text"
                value={formData.firstName}
                onChange={(e) =>
                  setFormData((prev) => ({
                    ...prev,
                    firstName: e.target.value,
                  }))
                }
              />
            </div>
            <div className="field">
              <label htmlFor="lastName">Last name</label>
              <input
                id="lastName"
                type="text"
                value={formData.lastName}
                onChange={(e) =>
                  setFormData((prev) => ({
                    ...prev,
                    lastName: e.target.value,
                  }))
                }
              />
            </div>
            <div className="field">
              <label htmlFor="phoneNumber">Phone</label>
              <input
                id="phoneNumber"
                type="tel"
                value={formData.phoneNumber}
                onChange={(e) =>
                  setFormData((prev) => ({
                    ...prev,
                    phoneNumber: e.target.value,
                  }))
                }
              />
            </div>
            <div className="flex gap-2">
              <Button type="submit">Save</Button>
              <Button
                type="button"
                variant="outline"
                onClick={() => setIsEditing(false)}
              >
                Cancel
              </Button>
            </div>
          </form>
        ) : (
          <div className="space-y-[var(--space-md)]">
            <div>
              <p className="font-mono text-[var(--text-xs)] uppercase tracking-wide text-[var(--color-ink-2)] m-0">
                Email
              </p>
              <p className="m-0 mt-1">{user?.email}</p>
            </div>
            <div>
              <p className="font-mono text-[var(--text-xs)] uppercase tracking-wide text-[var(--color-ink-2)] m-0">
                Name
              </p>
              <p className="m-0 mt-1">
                {user?.firstName} {user?.lastName}
              </p>
            </div>
            <div>
              <p className="font-mono text-[var(--text-xs)] uppercase tracking-wide text-[var(--color-ink-2)] m-0">
                Phone
              </p>
              <p className="m-0 mt-1">{user?.phoneNumber}</p>
            </div>
            <Button onClick={() => setIsEditing(true)}>Edit</Button>
          </div>
        )}
      </div>
    </div>
  );
}
