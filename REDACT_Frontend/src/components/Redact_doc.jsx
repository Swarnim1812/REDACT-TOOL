import React, { useState } from "react";
import Section from "./Section";
import Heading from "./Heading";
import { NavLink } from "react-router-dom";
import grid from "../assets/grid.png";
import { Gradient2 } from "./design/Roadmap";
import Button from "./Button";

function Redact_doc() {
  const [file, setFile] = useState(null);
  const [gradation, setGradation] = useState(1);
  const [loading, setLoading] = useState(false);
  const [customGradation, setCustomGradation] = useState([]);
  const [useCustomGradation, setUseCustomGradation] = useState(false);

  const gradationDescriptions = {
    1: "Level 1: GPE (City/Location)",
    2: "Level 2: GPE, ORG (Organization)",
    3: "Level 3: GPE, ORG, JOB_TITLE",
    4: "Level 4: GPE, ORG, JOB_TITLE, PERSON (Name)",
    5: "Level 5: GPE, ORG, JOB_TITLE, PERSON, TRANSACTION (Amount, Date), TIME (Meeting Time)",
    6: "Level 6: GPE, ORG, JOB_TITLE, PERSON, TRANSACTION, TIME, PHONE_NUMBER, EMAIL",
    7: "Level 7: GPE, ORG, JOB_TITLE, PERSON, TRANSACTION, TIME, PHONE_NUMBER, EMAIL, DRIVING_LICENSE, VOTER_ID",
    8: "Level 8: GPE, ORG, JOB_TITLE, PERSON, TRANSACTION, TIME, PHONE_NUMBER, EMAIL, DRIVING_LICENSE, VOTER_ID, IFSC_CODE, UPI_ID, GSTIN",
    9: "Level 9: GPE, ORG, JOB_TITLE, PERSON, TRANSACTION, TIME, PHONE_NUMBER, EMAIL, DRIVING_LICENSE, VOTER_ID, IFSC_CODE, UPI_ID, GSTIN, BANK_ACCOUNT, CREDIT_CARD, EPF_NUMBER",
    10: "Level 10: GPE, ORG, JOB_TITLE, PERSON, TRANSACTION, TIME, PHONE_NUMBER, EMAIL, DRIVING_LICENSE, VOTER_ID, IFSC_CODE, UPI_ID, GSTIN, BANK_ACCOUNT, CREDIT_CARD, EPF_NUMBER, AADHAAR_NUMBER, PAN_NUMBER, PASSPORT_NUMBER",
  };
  const entities = [
    { label: "GPE (City/Location)", value: "GPE" },
    { label: "ORG (Organization)", value: "ORG" },
    { label: "JOB_TITLE", value: "JOB_TITLE" },
    { label: "PERSON (Name)", value: "PERSON" },
    { label: "(Amount)", value: "TRANSACTION" },
    { label: "(Date)", value: "TRANSACTION1" },
    { label: "TIME (Meeting Time)", value: "TIME" },
    { label: "PHONE_NUMBER", value: "PHONE_NUMBER" },
    { label: "EMAIL", value: "EMAIL" },
    { label: "DRIVING_LICENSE", value: "DRIVING_LICENSE" },
    { label: "VOTER_ID", value: "VOTER_ID" },
    { label: "IFSC_CODE", value: "IFSC_CODE" },
    { label: "UPI_ID", value: "UPI_ID" },
    { label: "GSTIN", value: "GSTIN" },
    { label: "BANK_ACCOUNT", value: "BANK_ACCOUNT" },
    { label: "CREDIT_CARD", value: "CREDIT_CARD" },
    { label: "EPF_NUMBER", value: "EPF_NUMBER" },
    { label: "AADHAAR_NUMBER", value: "AADHAAR_NUMBER" },
    { label: "PAN_NUMBER", value: "PAN_NUMBER" },
    { label: "PASSPORT_NUMBER", value: "PASSPORT_NUMBER" },
  ];
  const handleFileUpload = (e) => {
    setFile(e.target.files[0]);
  };

  const handleGradationChange = (e) => {
    setGradation(e.target.value);
  };
  // const handleCustomSelectionChange = (e) => {
  //   const { value, checked } = e.target;
  //   setCustomGradation((prev) => {
  //     if (checked) {
  //       return [...prev, value]; // Add the selected tag
  //     } else {
  //       return prev.filter((tag) => tag !== value); // Remove the deselected tag
  //     }
  //   });
  // };
  const handleCustomSelectionChange = (e) => {
    const { value, checked } = e.target;
    setCustomGradation((prev) => {
      if (checked) {
        return [...prev, value]; // Add the selected tag
      } else {
        return prev.filter((tag) => tag !== value); // Remove the deselected tag
      }
    });
  };
  const handlePreview = () => {
    if (file) {
      const fileURL = URL.createObjectURL(file);
      window.open(fileURL, "_blank");
    } else {
      alert("Please upload a document first!");
    }
  };

  const handleClearFile = () => {
    setFile(null);
  };

  // const handleRedact = async () => {
  //   if (!file) {
  //     alert("Please upload a document first!");
  //     return;
  //   }

  //   setLoading(true);

  //   const formData = new FormData();
  //   formData.append("file", file);
  //   // formData.append("gradation", gradation);
  //   console.log(customGradation)
  //   if (useCustomGradation) {
  //     formData.append("custom_gradation", JSON.stringify(customGradation));
  //   } else {
  //     formData.append("gradation", gradation);
  //   }
  //   console.log(formData)
  //   try {
  //     const response = await fetch("http://localhost:5000/redact-img", {
  //       method: "POST",
  //       body: formData,
  //     });

  //     if (response.ok) {
  //       const blob = await response.blob();

  //       // Create a downloadable link
  //       const url = window.URL.createObjectURL(blob);
  //       const link = document.createElement("a");
  //       link.href = url;
  //       link.download = "final_output.pdf"; // File name for the downloaded PDF
  //       link.click();

  //       // Clean up the object URL
  //       window.URL.revokeObjectURL(url);

  //       // alert("Document redacted and downloaded successfully!");
  //     } else {
  //       alert("Failed to redact the document.");
  //     }
  //   } catch (error) {
  //     const errorData = await response.json();
  //     alert(`Failed to redact the document: ${errorData.message}`);
  //   } finally {
  //     setLoading(false);
  //   }
  // };
  const handleRedact2 = async () => {
    if (!file) {
      alert("Please upload a document first!");
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);
    // formData.append("gradation", gradation);
    console.log(customGradation)
    if (useCustomGradation) {
      formData.append("custom_gradation", JSON.stringify(customGradation));
    } else {
      formData.append("gradation", gradation);
    }
    console.log(formData)
    const fileType = file.type.split("/")[0]; // Get the type (e.g., "image" or "application")
    try {
      // const response = await fetch("http://localhost:5000/redact-document", {
      //   method: "POST",
      //   body: formData,
      // });
      let response;

      // Check if the file is an image or other type
      if (fileType === "image") {
        response = await fetch("http://localhost:5000/redact-img", {
          method: "POST",
          body: formData,
        });
      } else {
        response = await fetch("http://localhost:5000/redact-document", {
          method: "POST",
          body: formData,
        });
      }

      if (response.ok) {

        const blob = await response.blob();

        // Create a downloadable link
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        // link.download = "final_output.pdf"; // File name for the downloaded PDF
        link.download = response.file_name || "redacted_output"; // File name for the downloaded PDF
        link.click();

        // Clean up the object URL
        window.URL.revokeObjectURL(url);

        // alert("Document redacted and downloaded successfully!");
      } else {
        alert("Failed to redact the document.");
      }
    } catch (error) {
      const errorData = await response.json();
      alert(`Failed to redact the document: ${errorData.message}`);
    } finally {
      setLoading(false);
    }
  };

  const fileType = file ? file.type.split("/")[0] : "";

  return (
    <>
      <Section className="min-h-screen" id="roadmap">
        <Heading className="text-center flex flex-col items-center" tag="REDACT YOUR FILE" title="Document Redaction Tool" text="" />
        {/* <div className="bg-blue-700 h-[30rem] w-[49rem] fixed blur-[2.5rem] transform translate-x-[30rem] rounded-full  z-[-1] opacity-50"></div> */}
        <div className="text-white flex flex-col items-center justify-center px-4">
          <div className="md:flex even:md:translate-y-[4rem] p-0.25 rounded-[2.5rem] bg-conic-gradient overflow-hidden">
            <div className="p-16 bg-[#090018] rounded-[2.4375rem] w-[43rem] h-full z-10 ">
              <img
                className="absolute top-[16rem] max-w-full z-[-1]"
                src={grid}
                width={550}
                height={550}
                alt="Grid"
              />
              <div className="mb-6">
                <label className="block text-xl font-semibold text-center text-gray-300 mb-4">
                  Upload your Document
                </label>
                <div className="flex items-center justify-center">
                  <label className="block bg-green-900 text-white rounded-lg cursor-pointer hover:bg-blue-600 text-center font-medium text-sm px-5 py-[1.5rem] bg-gradient-to-r from-blue-500 via-blue-600 to-blue-700 hover:bg-gradient-to-br focus:ring-4 focus:outline-none focus:ring-blue-300 dark:focus:ring-blue-800 shadow-lg shadow-blue-500/50 dark:shadow-lg dark:shadow-blue-800/80 transition">
                    Choose File - ( PDF, DOCX, XML, CSV, TXT, PPT)
                    <input
                      type="file"
                      accept="image/*,application/pdf,.docx,.xml,text/plain,.csv,.txt,.pptx,.xlsx"
                      className="hidden"
                      onChange={handleFileUpload}
                    />
                  </label>
                </div>
                {file && (
                  <div className="mt-4 text-sm text-gray-400">
                    <p>{file.name}</p>
                    <p className="text-xs text-gray-500">
                      {fileType === "image" ? "Image File" : file.type}
                    </p>
                  </div>
                )}
              </div>
              {file && (
                <div className="mb-6">
                  <button
                    onClick={handleClearFile}
                    className="bg-red-600 px-4 py-2 w-full sm:w-auto rounded-lg text-lg text-white font-semibold hover:bg-red-500 transition"
                  >
                    Clear Document
                  </button>
                </div>
              )}

              <div className="mb-6">
                <label
                  htmlFor="gradation"
                  className="block mb-4 text-lg font-medium text-gray-300"
                >
                  Gradation Level: {gradation}
                </label>
                <div className="relative">
                  <input
                    type="range"
                    id="gradation"
                    min="1"
                    max="10"
                    value={gradation}
                    onChange={handleGradationChange}
                    className="w-full h-2 bg-gradient-to-r from-green-500 via-yellow-500 to-red-500 rounded-lg appearance-none cursor-pointer focus:outline-none"
                  />
                  <div className="absolute left-0 right-0 flex justify-between text-sm text-gray-400 mt-2">
                    <span>1</span>
                    <span>10</span>
                  </div>
                </div>
                <p className="p-4 mt-11 text-sm text-gray-300 bg-gray-700 rounded-lg">
                  {gradationDescriptions[gradation]}
                </p>
              </div>

              <div className="flex flex-wrap gap-4 justify-center">
                {file && (
                  <button
                    onClick={handlePreview}
                    className="bg-green-600 px-4 py-2 rounded-lg text-lg text-white font-semibold hover:bg-green-500 transition h-[3rem] w-full sm:w-auto"
                  >
                    Preview Document
                  </button>
                )}
                <div className="mb-6">
                  <label className="block text-lg font-medium text-gray-300 mb-4">
                    Gradation Input type
                  </label>
                  <select
                    value={useCustomGradation ? "custom" : gradation}
                    onChange={(e) =>
                      setUseCustomGradation(e.target.value === "custom")
                    }
                    className="w-full p-2 rounded-lg bg-gray-700 text-gray-300 cursor-pointer"
                  >
                    <option value="1">Slider</option>
                    <option value="custom">Custom Gradation</option>
                  </select>
                  {useCustomGradation && (
                    <div className="mt-4 flex flex-wrap items-center justify-center">
                      {entities.map((entity) => (
                        <label key={entity.value} className="block m-1 p-1 w-[15rem]">
                          <input
                            type="checkbox"
                            value={entity.value}
                            onChange={handleCustomSelectionChange}
                            className="mr-2"
                          />
                          {entity.label}
                        </label>
                      ))}
                    </div>
                  )}
                </div>
                <button
                  onClick={handleRedact2}
                  className={`bg-green-800 px-4 py-2 rounded-lg text-lg text-white font-semibold hover:bg-green-700 transition h-[6rem] w-full sm:w-auto ${loading ? "opacity-50 cursor-not-allowed" : ""
                    }`}
                  disabled={loading}
                >
                  {loading ? "Processing and Downloading..." : "Redact and Download"}
                </button>
                <Gradient2 />
              </div>
            </div>
          </div>
          <div className="mt-10">
            {/* <NavLink
              to="/get-started"
              className="bg-blue-900 opacity-50 text-white px-6 py-3 rounded-lg text-lg font-semibold hover:bg-blue-600 transition"
            >
              BACK
            </NavLink> */}
            <NavLink to="/"><Button>BACK TO HOME</Button></NavLink>
          </div>
        </div>
      </Section>
    </>
  );
}

export default Redact_doc;
