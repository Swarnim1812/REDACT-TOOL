import React, { useEffect, useState } from "react";

const LoaderBasic = ({ onLoadComplete }) => {
  useEffect(() => {
    const timer = setTimeout(() => {
      onLoadComplete(); // Call the callback function after loading
    }, 3000); // Adjust the duration of the loader (3 seconds in this case)

    return () => clearTimeout(timer); // Cleanup the timer on unmount
  }, [onLoadComplete]);

  return (
    <div className="loader-container">
      <div className="spinner"></div>
      <p className="mt-4">Loading...</p>
      <style jsx>{`
        .loader-container {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          height: 100vh;
          background: #000; /* Background color */
          color: #fff; /* Text color */
        }
        .spinner {
          width: 50px;
          height: 50px;
          border: 5px solid rgba(255, 255, 255, 0.3);
          border-top-color: #fff;
          border-radius: 50%;
          animation: spin 1s linear infinite;
        }
        @keyframes spin {
          to {
            transform: rotate(360deg);
          }
        }
      `}</style>
    </div>
  );
};

export default LoaderBasic;
