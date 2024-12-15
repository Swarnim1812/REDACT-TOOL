import React, { useState } from 'react'
import Section from './Section'
import Heading from './Heading'
import { vidicon } from '../assets'

function Redact_Video() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('');
  const [processedVideoUrl, setProcessedVideoUrl] = useState(null);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setUploadStatus('Please select a video file first');
      return;
    }

    const formData = new FormData();
    formData.append('video', selectedFile);

    try {
      setUploadStatus('Uploading and processing...');
      
      // Replace with your actual API endpoint
      const response = await fetch('http://localhost:5000/upload-video', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        console.log("error aara bhaiiiiiiiiiiiiiiiiiiiiiiii")
        throw new Error('Video upload failed');
      }
      console.log(response);

      const data = await response.json();
      console.log(data);

      // Construct download URL
      const downloadUrl = `http://localhost:5000/download-video/${data.output_video}`;
      
      setProcessedVideoUrl(downloadUrl);
      setUploadStatus('Video processed successfully!');
    } catch (error) {
      console.error('Upload error:', error);
      setUploadStatus('Error processing video');
    }
  };

  // const handleDownload = () => {
  //   if (processedVideoUrl) {
  //     window.open(processedVideoUrl, '_blank');
  //   }

  const handleDownload = async () => {
    if (processedVideoUrl) {
      try {
        const response = await fetch(`${processedVideoUrl}`, {
          method: 'GET'
        });
  
        if (!response.ok) {
          throw new Error('Download failed');
        }
  
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = processedVideoUrl;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
      } catch (error) {
        console.error('Download error:', error);
        setUploadStatus('Error downloading video');
      }
    }
  };

  return (
    <Section className="h-screen" id="roadmap">
      <Heading tag="Ready to get started" title="Choose Your Video file" />
      <div className="flex justify-center">
        <div className="flex items-center space-x-6">
          <div className="shrink-0">
            <img 
              className="h-16 w-16 object-cover rounded-full" 
              src={vidicon} 
              alt="Video upload icon" 
            />
          </div>
          <label className="block">
            <span className="sr-only">Choose video file</span>
            <input 
              type="file" 
              accept="video/*"
              className="block w-full text-sm text-slate-500
                file:mr-4 file:py-2 file:px-4
                file:rounded-full file:border-0
                file:text-sm file:font-semibold
                file:bg-violet-50 file:text-violet-700
                hover:file:bg-violet-100"
              onChange={handleFileChange}
            />
          </label>
        </div>
      </div>

      {selectedFile && (
        <div className="flex justify-center mt-4">
          <div className="text-center">
            <p className="text-sm text-gray-600">
              Selected file: {selectedFile.name}
            </p>
            <button 
              onClick={handleUpload}
              className="mt-2 px-4 py-2 bg-violet-600 text-white rounded-full hover:bg-violet-700"
            >
              Process Video
            </button>
          </div>
        </div>
      )}

      {uploadStatus && (
        <div className="flex justify-center mt-4">
          <p className={`text-sm ${uploadStatus.includes('Error') ? 'text-red-500' : 'text-green-500'}`}>
            {uploadStatus}
          </p>
        </div>
      )}

      {processedVideoUrl && (
        <div className="flex justify-center mt-4">
          <button 
            onClick={handleDownload}
            className="px-4 py-2 bg-green-600 text-white rounded-full hover:bg-green-700"
          >
            Download Processed Video
          </button>
        </div>
      )}
    </Section>
  )
}

export default Redact_Video