import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { TabSwitchProvider } from './TabSwitchContext';
import Login from './components/Login';
import Home from './components/Home';

function App() {
  const [visibility, setVisibility] = useState(true);

  useEffect(() => {
    const handleVisibilityChange = () => {
      // Check if the page is currently hidden or visible
      const isVisible = !document.hidden;

      // Update the visibility state
      setVisibility(isVisible);

      // Update local storage
      localStorage.setItem('visibility', isVisible ? 'visible' : 'hidden');
    };

    // Add event listener for visibility change
    document.addEventListener('visibilitychange', handleVisibilityChange);

    // Check initial visibility state
    handleVisibilityChange();

    // Clean up event listener
    return () => {
      document.removeEventListener('visibilitychange', handleVisibilityChange);
    };
  }, []);

  return (
    <div className="App">
      <TabSwitchProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Login />} />
            <Route path="/home" element={<Home />} />
          </Routes>
        </BrowserRouter>
      </TabSwitchProvider>
    </div>
  );
}

export default App;