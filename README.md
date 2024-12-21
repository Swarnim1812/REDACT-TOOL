# RE-DACT: Secure Redaction and Anonymization Tool

RE-DACT is a powerful tool designed for secure redaction, masking, and anonymization of sensitive data. The project leverages Machine Learning, Python and Cybersecurity principles to ensure data security and integrity across various input formats.

---

## 🖥 Project Overview

RE-DACT enables the redaction of sensitive data while maintaining the structural and logical integrity of the input. It offers customizable redaction levels and advanced features like generating synthetic data for learning and sharing purposes. The tool is designed with an easy-to-use GUI.

### Features:
- Redacts and anonymizes sensitive content in text, images, docx, CSVs, PPTs, PDFs, and videos.
- Supports gradational redaction in various levels as well as user customizable anonymization.
- Ensures data security without storing or exposing input data.
- Generates realistic synthetic data for non-sensitive sharing.
- Provides a flexible and user-friendly GUI.
- Video redaction focuses specifically on face and text redaction.

### Use Cases:
- Privacy compliance in data sharing and processing.
- Data preparation for machine learning and analytics.
- Anonymizing sensitive information for secure sharing.
- Legal document and video redaction.
---

## 🚀 How to Run Locally

Follow these steps to clone and run the RE-DACT project on your local machine:

### Prerequisites:
- Python 3.8 or higher installed.
- Node.js installed (for the frontend).
- `pip` and `npm` package managers.

### Steps:

#### Backend Setup:
1. Clone the repository and navigate to the `backend` directory:

   ```bash
   git clone https://github.com/yourusername/re-dact.git
   cd re-dact/backend
   ```
3. Install the required dependencies:
   
   ```bash
   pip install flask flask-cors werkzeug pandas requests cryptography spacy PyPDF2 opencv-python imutils ultralytics paddleocr python-docx openpyxl matplotlib faker fpdf
   ```
  ##### Key dependencies used in the project:

  - Flask: For backend API development.
  - Flask-CORS: For handling cross-origin requests.
  - Werkzeug: For file handling.
  - pandas: For data manipulation.
  - requests: For HTTP requests.
  - cryptography: For data encryption and hashing.
  - spacy: For entity recognition and NLP tasks.
  - PyPDF2: For PDF processing.
  - opencv-python: For image and video processing.
  - imutils: For image utilities.
  - ultralytics: For YOLO-based object detection.
  - paddleocr: For OCR tasks.
  - python-docx: For Word document processing.
  - openpyxl: For Excel file processing.
  - matplotlib: For data visualization.
  - faker: For generating synthetic data.
  - fpdf: For generating PDF files.

3. Start the backend by running the following commands in separate terminals, all within the backend directory:
   - Terminal 1:

       ```
       python doc.py
       ```
   - Terminal 2:

       ```
       python final_model_full_code.py
       ```
   - Terminal 3:

       ```
       python freetext_code.py
       ```
#### Frontend Setup:

1. Navigate to the frontend directory:
  
  ```
  cd ../frontend
  ```
2. Install the frontend dependencies:
  
  ```
  npm i -y
  ```
3. Start the frontend server:
  
  ```
  npm run dev
  ```
4. Access the application on your browser at:
  
  ```
  http://localhost:5173
  ```

# 🙋🏻‍♂️ ENJOY! 

