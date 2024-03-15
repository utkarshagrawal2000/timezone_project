// TabSwitchContext.js

import React, { createContext, useState, useEffect } from 'react';

const TabSwitchContext = createContext();

export const TabSwitchProvider = ({ children }) => {
  const [lastTabSwitchTime, setLastTabSwitchTime] = useState(0);

  useEffect(() => {
    const tabSwitchListener = () => {
      setLastTabSwitchTime(Date.now());
    };
    document.addEventListener('visibilitychange', tabSwitchListener);
    return () => {
      document.removeEventListener('visibilitychange', tabSwitchListener);
    };
  }, []);

  return (
    <TabSwitchContext.Provider value={{ lastTabSwitchTime }}>
      {children}
    </TabSwitchContext.Provider>
  );
};

export default TabSwitchContext;
