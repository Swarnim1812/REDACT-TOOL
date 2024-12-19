import React, { useEffect } from "react";

const Loader = ({ onLoadComplete }) => {
  useEffect(() => {
    const timer = setTimeout(() => {
      onLoadComplete(); // Call the callback function after loading
    }, 3000); // Adjust the duration of the loader (3 seconds in this case)

    return () => clearTimeout(timer); // Cleanup the timer on unmount
  }, [onLoadComplete]);

  return (
    <div className="loader-container bg-n-8">
      <div className="ripple-container">
        <div className="ripple"></div>
      </div>

      <style>{`
        .loader-container {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          height: 100vh;
          color: #fff; /* Text color */
          font-family: 'Arial', sans-serif;
        }

        .ripple-container {
          position: relative;
          width: 120px;
          height: 120px;
          border-radius: 50%;
          overflow: hidden;
          animation: ripple-animation 2s infinite ease-out;
        }

        .ripple {
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          background: rgba(255, 255, 255, 0.3);
          border-radius: 50%;
          transform-origin: center;
          animation: ripple-expand 3s infinite ease-out, ripple-opacity 3s infinite;
          box-shadow: 0 0 30px rgba(255, 255, 255, 0.5), 0 0 60px rgba(255, 255, 255, 0.3);
        }

        /* Animation for expanding the ripple */
        @keyframes ripple-expand {
          0% {
            transform: scale(0.4) rotate(0deg);
            opacity: 0.6;
          }
          50% {
            transform: scale(1.2) rotate(180deg);
            opacity: 0.4;
          }
          100% {
            transform: scale(2.5) rotate(360deg);
            opacity: 0;
          }
        }

        /* Animation for opacity fading */
        @keyframes ripple-opacity {
          0% {
            opacity: 0.6;
          }
          50% {
            opacity: 0.4;
          }
          100% {
            opacity: 0;
          }
        }

        /* Extra subtle 3D shadow effect */
        .ripple-container {
          box-shadow: 0 0 15px rgba(255, 255, 255, 0.4), 0 0 25px rgba(255, 255, 255, 0.2);
        }

        /* 3D rotation effect */
        .ripple-container::after {
          content: '';
          position: absolute;
          top: 50%;
          left: 50%;
          width: 100%;
          height: 100%;
          border-radius: 50%;
          background: rgba(255, 255, 255, 0.1);
          transform: translate(-50%, -50%) scale(0);
          animation: rotate-3d 4s infinite ease-out;
        }

        @keyframes rotate-3d {
          0% {
            transform: translate(-50%, -50%) rotate(0deg) scale(0);
          }
          50% {
            transform: translate(-50%, -50%) rotate(180deg) scale(1.3);
          }
          100% {
            transform: translate(-50%, -50%) rotate(360deg) scale(0);
          }
        }
      `}</style>
    </div>
  );
};

export default Loader;
