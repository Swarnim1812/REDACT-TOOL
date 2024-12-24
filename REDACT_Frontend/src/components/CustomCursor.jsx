import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";

const CustomCursor = () => {
  const [cursorPosition, setCursorPosition] = useState(null);
  const [cursorScale, setCursorScale] = useState(0.4);

  useEffect(() => {
    const moveCursor = (e) => {
      setCursorPosition({ x: e.clientX, y: e.clientY });
    };

    const handleMouseEnter = (e) => {
      // Check if the target is a button or text element
      if (
        e.target.tagName === "BUTTON" ||
        e.target.tagName === "A" ||
        e.target.classList.contains("hover_target")
      ) {
        setCursorScale(2.3);
      }
    };

    const handleMouseLeave = (e) => {
      setCursorScale(0.4);
    };

    window.addEventListener("mousemove", moveCursor);
    window.addEventListener("mouseover", handleMouseEnter);
    window.addEventListener("mouseout", handleMouseLeave);

    return () => {
      window.removeEventListener("mousemove", moveCursor);
      window.removeEventListener("mouseover", handleMouseEnter);
      window.removeEventListener("mouseout", handleMouseLeave);
    };
  }, []);
  if (!cursorPosition) {
    return null; // Hide the cursor until the first mousemove event
  }
  return (
    <motion.div
      className="custom-cursor"
      style={{
        top: cursorPosition.y,
        left: cursorPosition.x,
        transform: `translate(-50%, -50%) scale(${cursorScale})`,
      }}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.1 }}
    />
  );
};

export default CustomCursor;
