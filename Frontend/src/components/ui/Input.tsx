import { forwardRef, InputHTMLAttributes } from "react";
import { cn } from "../../lib/utils";

export interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  error?: boolean;
  helperText?: string;
  label?: string;
  fullWidth?: boolean;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  (
    { className, error, helperText, label, fullWidth = false, ...props },
    ref
  ) => {
    return (
      <div className={cn("flex flex-col gap-1.5", fullWidth && "w-full")}>
        {label && (
          <label
            htmlFor={props.id}
            className="text-sm font-medium text-gray-700"
          >
            {label}
          </label>
        )}
        <input
          className={cn(
            "px-3 py-2 bg-white border rounded-md text-sm shadow-sm placeholder-gray-400",
            "focus:outline-none focus:border-primary-500 focus:ring-1 focus:ring-primary-500",
            "disabled:bg-gray-50 disabled:text-gray-500 disabled:border-gray-200 disabled:shadow-none",
            error
              ? "border-error-main text-error-main focus:border-error-main focus:ring-error-main"
              : "border-gray-300",
            fullWidth && "w-full",
            className
          )}
          ref={ref}
          {...props}
        />
        {helperText && (
          <p
            className={cn(
              "text-sm",
              error ? "text-error-main" : "text-gray-500"
            )}
          >
            {helperText}
          </p>
        )}
      </div>
    );
  }
);
