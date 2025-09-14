"use client";
import React from "react";
import clsx from "clsx";

type CardProps = React.HTMLAttributes<HTMLDivElement> & {
  variant?: "elevated" | "gradient";
  children: React.ReactNode;
  className?: string;
};

export function Card({
  variant = "elevated",
  children,
  className,
  ...props
}: CardProps) {
  return (
    <div
      className={clsx(
        "rounded-2xl transition-all duration-200",
        variant === "elevated"
          ? "bg-white shadow-xl"
          : "bg-gradient-to-br from-blue-50 to-purple-50 shadow",
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
} 