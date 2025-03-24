import { ReactNode } from "react";
import { cn } from "../../lib/utils";

interface CardProps {
  children: ReactNode;
  className?: string;
  onClick?: () => void;
  hoverable?: boolean;
  padding?: "none" | "small" | "medium" | "large";
}

export function Card({
  children,
  className,
  onClick,
  hoverable = false,
  padding = "medium",
}: CardProps) {
  const paddingMap = {
    none: "p-0",
    small: "p-3",
    medium: "p-4",
    large: "p-6",
  };

  return (
    <div
      className={cn(
        "bg-white rounded-lg shadow-sm",
        paddingMap[padding],
        hoverable && "transition-shadow hover:shadow-md cursor-pointer",
        className
      )}
      onClick={onClick}
    >
      {children}
    </div>
  );
}

interface CardHeaderProps {
  children: ReactNode;
  className?: string;
}

export function CardHeader({ children, className }: CardHeaderProps) {
  return (
    <div className={cn("border-b border-gray-200 pb-4 mb-4", className)}>
      {children}
    </div>
  );
}

interface CardTitleProps {
  children: ReactNode;
  className?: string;
}

export function CardTitle({ children, className }: CardTitleProps) {
  return (
    <h3 className={cn("text-lg font-semibold text-gray-900", className)}>
      {children}
    </h3>
  );
}

interface CardContentProps {
  children: ReactNode;
  className?: string;
}

export function CardContent({ children, className }: CardContentProps) {
  return <div className={cn("", className)}>{children}</div>;
}

interface CardFooterProps {
  children: ReactNode;
  className?: string;
}

export function CardFooter({ children, className }: CardFooterProps) {
  return (
    <div className={cn("border-t border-gray-200 pt-4 mt-4", className)}>
      {children}
    </div>
  );
}
