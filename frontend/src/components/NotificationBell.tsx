"use client";

import React, { useEffect, useState, useRef } from "react";
import { Bell } from "lucide-react";

export default function NotificationBell() {
  const [notifications, setNotifications] = useState<any[]>([]);
  const [unread, setUnread] = useState(0);
  const [toast, setToast] = useState<string | null>(null);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    // TODO: récupérer le token utilisateur dynamiquement
    const token = localStorage.getItem("token");
    if (!token) return;
    const ws = new WebSocket(`ws://localhost:8000/ws/notifications/?token=${token}`);
    wsRef.current = ws;
    ws.onmessage = (event) => {
      try {
        const notif = JSON.parse(event.data);
        setNotifications((prev) => [notif, ...prev]);
        setUnread((u) => u + 1);
        setToast(notif?.feedback?.message || notif.message || "Nouvelle notification");
        setTimeout(() => setToast(null), 4000);
      } catch (e) {
        // fallback notification
        setToast("Nouvelle notification reçue");
        setTimeout(() => setToast(null), 4000);
      }
    };
    ws.onclose = () => {
      wsRef.current = null;
    };
    return () => {
      ws.close();
    };
  }, []);

  return (
    <div className="relative">
      <button className="relative p-2 rounded-full hover:bg-blue-100 transition">
        <Bell className="w-7 h-7 text-blue-600" />
        {unread > 0 && (
          <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full px-1.5 py-0.5 font-bold">
            {unread}
          </span>
        )}
      </button>
      {/* Toast notification */}
      {toast && (
        <div className="fixed bottom-6 right-6 bg-blue-700 text-white px-6 py-3 rounded-xl shadow-lg z-50 animate-fade-in">
          {toast}
        </div>
      )}
    </div>
  );
} 