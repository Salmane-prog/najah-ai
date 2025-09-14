"use client";
import React from "react";
import clsx from "clsx";

type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: "primary" | "secondary" | "outline";
  size?: "sm" | "md" | "lg";
  icon?: React.ReactNode;
  loading?: boolean;
  fullWidth?: boolean;
  children: React.ReactNode;
  className?: string;
};

export default function Button({
  variant = "primary",
  size = "md",
  icon,
  loading,
  fullWidth,
  children,
  className,
  ...props
}: ButtonProps) {
  return (
    <button
      className={clsx(
        "inline-flex items-center justify-center font-semibold rounded-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500",
        variant === "primary"
          ? "bg-gradient-to-tr from-blue-600 to-purple-600 text-white hover:from-blue-700 hover:to-purple-700 shadow"
          : variant === "secondary"
          ? "bg-white text-blue-600 border border-blue-600 hover:bg-blue-50"
          : "bg-white text-gray-700 border border-gray-300 hover:bg-gray-50",
        size === "sm" && "px-3 py-1.5 text-sm",
        size === "md" && "px-5 py-2 text-base",
        size === "lg" && "px-7 py-3 text-lg",
        fullWidth && "w-full",
        loading && "opacity-60 cursor-not-allowed",
        className
      )}
      disabled={loading || props.disabled}
      {...props}
    >
      {icon && <span className="mr-2">{icon}</span>}
      {loading ? (
        <span className="flex items-center gap-2">
          <span className="animate-spin rounded-full h-4 w-4 border-b-2 border-white" />
          {typeof children === "string" ? children : "Chargement..."}
        </span>
      ) : (
        children
      )}
    </button>
  );
} 