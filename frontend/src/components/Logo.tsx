"use client";
import React from "react";
import { BookOpen } from "lucide-react";

export default function Logo({ size = 40 }: { size?: number }) {
  return (
    <div
      className="bg-gradient-to-br from-blue-600 to-purple-600 rounded-xl flex items-center justify-center animate-pulse-slow shadow"
      style={{ width: size, height: size }}
    >
      <BookOpen className="text-white" size={size * 0.6} />
    </div>
  );
} 