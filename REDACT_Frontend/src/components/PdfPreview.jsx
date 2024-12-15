import React, { useEffect, useRef } from 'react';
import { fabric } from 'fabric';

const PdfPreview = ({ jsonData }) => {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = new fabric.Canvas(canvasRef.current, {
      width: 960, // Adjust according to desired canvas size
      height: 540, // Adjust according to desired canvas size
    });

    // Scale factor for rendering
    const scaleFactor = Math.min(
      canvas.width / jsonData.metadata.width,
      canvas.height / jsonData.metadata.height
    );

    // Draw text elements
    jsonData.text.forEach((textObj) => {
      const [topLeft] = textObj.coordinates;
      const x = topLeft[0] * jsonData.metadata.width * scaleFactor;
      const y = topLeft[1] * jsonData.metadata.height * scaleFactor;

      const text = new fabric.Text(textObj.content, {
        left: x,
        top: y,
        fontSize: textObj.font_size * scaleFactor,
        fill: 'black',
      });

      canvas.add(text);
    });

    return () => {
      canvas.dispose();
    };
  }, [jsonData]);

  return (
    <div>
      <canvas ref={canvasRef} />
    </div>
  );
};

export default PdfPreview;