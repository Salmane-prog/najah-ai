'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';

interface DashboardContextType {
  refreshTrigger: number;
  triggerRefresh: () => void;
  lastUpdate: Date;
}

const DashboardContext = createContext<DashboardContextType | undefined>(undefined);

export function DashboardProvider({ children }: { children: React.ReactNode }) {
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [lastUpdate, setLastUpdate] = useState(new Date());

  const triggerRefresh = () => {
    setRefreshTrigger(prev => prev + 1);
    setLastUpdate(new Date());
  };

  return (
    <DashboardContext.Provider value={{ refreshTrigger, triggerRefresh, lastUpdate }}>
      {children}
    </DashboardContext.Provider>
  );
}

export function useDashboard() {
  const context = useContext(DashboardContext);
  if (context === undefined) {
    throw new Error('useDashboard must be used within a DashboardProvider');
  }
  return context;
} 