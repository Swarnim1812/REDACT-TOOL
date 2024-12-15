import React from 'react';
import PdfPreview from './PdfPreview';
import jsonData from '../sample_json.json'; // Replace with the path to your JSON file

const NewF = () => {
  return (
    <div>
      <h1>PDF Preview</h1>
      <PdfPreview jsonData={jsonData} />
    </div>
  );
};

export default NewF;