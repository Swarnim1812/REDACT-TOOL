import React, { useState } from 'react'
import Section from './Section'
import Heading from './Heading'
import { vidicon } from '../assets'
import { NavLink } from "react-router-dom";
import Button from "./Button";
import grid from "../assets/grid.png";
import { Gradient2, Gradient4 } from "./design/Roadmap";
import { ThreeDots } from "react-loader-spinner";

function Redact_Video() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('');
  const [loading, setLoading] = useState(false);
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
      setLoading(true);
      setUploadStatus('Uploading and processing...');

      // Replace with your actual API endpoint
      const response = await fetch('http://localhost:8004/upload-video', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        console.log("error response", response);
        throw new Error('Video upload failed');
      }

      const data = await response.json();
      console.log(data);

      // Construct download URL
      const downloadUrl = `http://localhost:8004/download-video/${data.output_video}`;

      setProcessedVideoUrl(downloadUrl);
      setUploadStatus('Video processed successfully!');
      setLoading(false);
    } catch (error) {
      console.error('Upload error:', error);
      setUploadStatus('Error processing video');
    }
  };

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
  // return (

  //   <Section className="min-h-screen" id="roadmap">
  //     <Heading
  //       className="text-center flex flex-col items-center"
  //       tag="READY TO GET STARTED"
  //       title="Choose Your Video File"
  //       text=""
  //     />
  //     <div className="text-white flex flex-col items-center justify-center px-4">
  //       <div className="md:flex even:md:translate-y-[4rem] p-0.25 rounded-[2.5rem] bg-conic-gradient overflow-hidden">
  //         <div className="p-10 sm:p-12 md:p-16 bg-[#090018] rounded-[2.4375rem] h-[37rem] w-[50rem] max-w-[43rem] h-full z-10">
  //           <img
  //             className="absolute top-[17rem] left-[43rem] max-w-full z-[-1] hidden lg:block"
  //             src={grid}
  //             width={520}
  //             height={550}
  //             alt="Grid"
  //           />
  //           <div className="h-auto w-full max-w-4xl">
  //             <label className="block text-xl font-semibold text-center text-gray-300 mb-10">
  //               Upload Your Video
  //             </label>
  //             <div className="flex items-center justify-center mb-6">
  //               <label className="block bg-green-900 text-white rounded-lg cursor-pointer hover:bg-blue-600 text-center font-medium text-sm px-5 py-[1.5rem] bg-gradient-to-r from-blue-500 via-blue-600 to-blue-700 hover:bg-gradient-to-br focus:ring-4 focus:outline-none focus:ring-blue-300 dark:focus:ring-blue-800 shadow-lg shadow-blue-500/50 dark:shadow-lg dark:shadow-blue-800/80 transition">
  //                 Choose File - (MP4, AVI, MOV)
  //                 <input
  //                   type="file"
  //                   accept="video/*"
  //                   className="hidden"
  //                   onChange={handleFileChange}
  //                 />
  //               </label>
  //             </div>
  //             <div className='text-center mb-3 p-1 h-[6rem]'>
  //               {selectedFile && (
  //                 <div className="mt-4 text-sm text-gray-400 text-center mb-6">
  //                   <p>{selectedFile.name}</p>
  //                   <p className="text-xs text-gray-500 mt-3">Video File</p>
  //                 </div>
  //               )}
  //             </div>

  //             <div className="mb-6 w-full flex justify-center">
  //               <Button
  //                 onClick={handleUpload}
  //                 className="w-[30rem]"
  //                 white
  //               >
  //                 Process Video
  //               </Button>
  //             </div>

  //             {uploadStatus && (
  //               <div className="flex justify-center mt-4">
  //                 <p
  //                   className={`text-base font-medium ${uploadStatus.includes("Error") ? "text-red-500" : "text-green-500"}`}
  //                 >
  //                   {uploadStatus}
  //                 </p>
  //               </div>
  //             )}
  //           </div>

  //           <Gradient2 />

  //           {processedVideoUrl && (
  //             <div className="flex justify-center mt-6">
  //               <button
  //                 onClick={handleDownload}
  //                 className="bg-green-600 px-4 py-2 rounded-lg text-lg text-white font-semibold hover:bg-green-500 transition"
  //               >
  //                 Download Processed Video
  //               </button>
  //             </div>
  //           )}
  //         </div>
  //       </div>
  //       <div className="mt-20">
  //         <NavLink to="/get-started">
  //           <Button>BACK</Button>
  //         </NavLink>
  //       </div>
  //     </div>
  //   </Section>
  // );

  return (
    <Section className="min-h-screen" id="roadmap">
      <Gradient4 />
      <Heading
        className="text-center flex flex-col items-center"
        tag="READY TO GET STARTED"
        title="Choose Your Video File"
        text=""
      />

      <div className="text-white flex flex-col items-center justify-center px-4">
        <div className="md:flex even:md:translate-y-[4rem] p-0.25 rounded-[2.5rem] bg-conic-gradient overflow-hidden">
          <div className="p-10 sm:p-12 md:p-16 bg-[#090018] rounded-[2.4375rem] w-full max-w-[43rem] h-full z-10 relative">
            <img
              className="absolute left-1/2 transform -translate-x-1/2 max-w-full z-[-1] hidden lg:block top-0"
              src={grid}
              width={520}
              height={550}
              alt="Grid"
            />
            <div className="h-auto w-full max-w-4xl">
              <label className="block text-xl font-semibold text-center text-gray-300 mb-10">
                Upload Your Video
              </label>
              <div className="flex items-center justify-center mb-6">
                <label className="block bg-green-900 text-white rounded-lg cursor-pointer hover:bg-blue-600 text-center font-medium text-sm px-5 py-[1.5rem] bg-gradient-to-r from-blue-500 via-blue-600 to-blue-700 hover:bg-gradient-to-br focus:ring-4 focus:outline-none focus:ring-blue-300 dark:focus:ring-blue-800 shadow-lg shadow-blue-500/50 dark:shadow-lg dark:shadow-blue-800/80 transition">
                  Choose File - (MP4, AVI, MOV)
                  <input
                    type="file"
                    accept="video/*"
                    className="hidden"
                    onChange={handleFileChange}
                  />
                </label>
              </div>
              <div className='text-center mb-3 p-1 h-[6rem]'>
                {selectedFile && (
                  <div className="mt-4 text-sm text-gray-400 text-center mb-6">
                    <p>{selectedFile.name}</p>
                    <p className="text-xs text-gray-500 mt-3">Video File</p>
                  </div>
                )}
              </div>

              <div className="mb-6 w-full flex justify-center">
                <Button
                  onClick={handleUpload}
                  className="w-full sm:w-[30rem]"
                  white
                >
                  Process Video
                </Button>
              </div>

              {uploadStatus && loading && (
                <div className="flex flex-col items-center justify-center mt-4">
                  <p className={`text-base font-medium ${uploadStatus.includes("Error") ? "text-red-500" : "text-green-500"}`}>
                    {uploadStatus}
                  </p>
                  <ThreeDots
                    height="80"
                    width="80"
                    radius="9"
                    color="#00BFFF"
                    ariaLabel="three-dots-loading"
                    wrapperStyle={{}}
                    wrapperClass=""
                    visible={loading}
                  />
                </div>
              )}
          </div>


          {processedVideoUrl && (
            <div className="flex justify-center mt-6">
              <button
                onClick={handleDownload}
                className="bg-green-600 px-4 py-2 rounded-lg text-lg text-white font-semibold hover:bg-green-500 transition"
              >
                Download Processed Video
              </button>
            </div>
          )}
        </div>
      </div>
      <div className="mt-20">
        <NavLink to="/get-started">
          <Button>BACK</Button>
        </NavLink>
      </div>
    </div>
    </Section >
  );

}

export default Redact_Video