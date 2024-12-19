import React from "react";

const ChatFAQs = () => {
  const faqs = [
    { question: "What file formats are supported?", answer: "RE-DACT currently supports text files,images, PDFs, docx, CSV, Powerpoint presentations and videos." },
    { question: "Is my data secure during the process?", answer: "Absolutely. All redaction happens locally, and no data is stored or accessible to third parties." },
    { question: "Can I control the level of redaction?", answer: "Yes! You can customize the degree of redaction from minimal to complete obfuscation using the gradation scale." },
    { question: "Is it easy to use?", answer: "Yes! The tool features a user-friendly interface designed for both technical and non-technical users." },
  ];

  return (
    <div className="max-w-lg mx-auto p-6 bg-none rounded-lg shadow-lg">
      <div className="flex flex-col space-y-4 overflow-y-auto h-[33rem] p-7 bg-n-8 rounded-lg shadow-inner">
        {faqs.map((faq, index) => (
          <div key={index} className="flex flex-col space-y-2">
            {/* Question */}
            <div className="flex justify-start">
              <div className="max-w-xs px-4 py-2 rounded-lg bg-blue-100 text-blue-800">
                Q: {faq.question}
              </div>
            </div>
            {/* Answer */}
            <div className="flex justify-end">
              <div className="max-w-xs px-4 py-2 rounded-lg bg-green-100 text-green-800">
                A: {faq.answer}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ChatFAQs;
