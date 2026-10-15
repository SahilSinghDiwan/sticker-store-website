import { ButtonHTMLAttributes, forwardRef } from "react";
import { cn } from "../../lib/utils";

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "outline" | "ghost" | "link";
  size?: "sm" | "md" | "lg";
  fullWidth?: boolean;
  loading?: boolean;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      className,
      variant = "primary",
      size = "md",
      fullWidth = false,
      loading = false,
      disabled,
      children,
      ...props
    },
    ref
  ) => {
    const variants = {
      primary:
        "bg-[var(--color-accent)] text-[var(--color-accent-ink)] hover:brightness-95 active:translate-y-px",
      secondary:
        "bg-[var(--color-ink)] text-[var(--color-accent-ink)] hover:brightness-110 active:translate-y-px",
      outline:
        "border border-[var(--color-rule)] text-[var(--color-ink)] bg-transparent hover:bg-[var(--color-paper-2)] active:translate-y-px",
      ghost:
        "text-[var(--color-ink-2)] hover:text-[var(--color-ink)] hover:bg-[var(--color-paper-2)]",
      link: "text-[var(--color-accent)] hover:underline p-0 h-auto",
    };

    const sizes = {
      sm: "px-3 py-1.5 text-sm",
      md: "px-4 py-2 text-sm",
      lg: "px-5 py-2.5 text-base",
    };

    return (
      <button
        className={cn(
          "inline-flex items-center justify-center font-medium whitespace-nowrap",
          "rounded-[var(--radius-card)] transition-[background-color,transform,filter,color]",
          "[transition-duration:var(--dur-short)] [transition-timing-function:var(--ease-out)]",
          "focus:outline-none focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--color-focus)]",
          "disabled:opacity-50 disabled:cursor-not-allowed disabled:active:translate-y-0",
          variant !== "link" && sizes[size],
          variants[variant],
          fullWidth && "w-full",
          className
        )}
        disabled={disabled || loading}
        ref={ref}
        {...props}
      >
        {loading ? (
          <>
            <svg
              className="w-4 h-4 mr-2 animate-spin"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              aria-hidden
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              />
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              />
            </svg>
            Working…
          </>
        ) : (
          children
        )}
      </button>
    );
  }
);

Button.displayName = "Button";
