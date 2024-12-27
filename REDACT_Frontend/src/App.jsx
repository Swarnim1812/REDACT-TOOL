import React, { useEffect, useState } from "react";
import ButtonGradient from "./assets/svg/ButtonGradient";
import Allroutes from "./components/Allroutes";
import Loader from "./components/Loader";
import CustomCursor from "./components/CustomCursor";
const App = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [showCustomCursor, setShowCustomCursor] = useState(false);

  const handleLoadComplete = () => {
    setIsLoading(false); // Hide loader after loading
  };
  useEffect(() => {
    // Check screen size and update state
    const updateCursorVisibility = () => {
      setShowCustomCursor(window.innerWidth > 1024); // Show custom cursor only for screens wider than 1024px
    };

    updateCursorVisibility(); // Initial check
    window.addEventListener("resize", updateCursorVisibility); // Update on window resize

    return () => {
      window.removeEventListener("resize", updateCursorVisibility);
    };
  }, []);

  return (
    <>
      {isLoading ? (
        <Loader onLoadComplete={handleLoadComplete} />
      ) : (
        <>
          {showCustomCursor && <CustomCursor />}
          <Allroutes />
          <ButtonGradient />
        </>
      )}
    </>
  );
};

export default App;
