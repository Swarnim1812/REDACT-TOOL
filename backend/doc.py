from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import json
from json import dump
import requests

from preprocessing import ImageProcessor # Import the ImageProcessor class from Python script
from docpreprocessing import DocumentProcessorFactory

import pandas as pd
import requests
import re
from collections import defaultdict

app = Flask(__name__) # Initialize Flask app
CORS(app) # Enable CORS for all routes
# Set upload folder and allowed extensions
UPLOAD_FOLDER = "./uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

#----------------------------------------------------------------------------------------------

@app.route("/redact-img", methods=["POST"])
def redact_document():
    if "file" not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"message": "No selected file"}), 400
    
    gradation = request.form.get("gradation", "default")  # Default value if not provided
    custom_gradation = request.form.get("custom_gradation", "[]")
    try:
        custom_gradation = json.loads(custom_gradation)  # Convert JSON string to Python list
    except json.JSONDecodeError:
        return jsonify({"message": "Invalid custom_gradation format"}), 400
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)
    print(file_path)
    try:
        processor = ImageProcessor() # Process the file using your ImageProcessor class
        processor.process_image(file_path)

        # Save output to a specific file and get the JSON data
        output_path = "output.json"
        output_data = processor.save_results(output_path)

        # Integrate gradation into the metadata of the output data
        output_data['metadata']['gradation'] = gradation
        output_data['metadata']['custom_tags'] = custom_gradation
        
        # Save the updated data to a new file
        combined_output_path = "combined_output.json"
        with open(combined_output_path, "w") as file:
            json.dump(output_data, file, indent=4)

        print(f"Gradation Level: {gradation}")
        print(f"Custom Tags: {custom_gradation}")
        print(f"Combined output saved to {combined_output_path}")

        # Optionally send the updated JSON to a notebook or another endpoint
        redaction_response = send_to_redaction_process(combined_output_path)

        # Save the redacted JSON received from the second API
        redacted_output_path = "output_redacted.json"
        with open(redacted_output_path, "w") as redacted_file:
            json.dump(redaction_response, redacted_file, indent=4)

        with open(redacted_output_path, "r") as redacted_file:
            redacted_obj = json.load(redacted_file)
            
        # Convert the redacted JSON back into a PDF (implementation needed)
        pdf_output_path = "final_output.pdf"
        processor.text_objects = redacted_obj['text']
        processor.reconstruct_pdf(pdf_output_path, "./telea_transparent.png")

        # return jsonify({"message": "File has been processed and redacted successfully!"}), 200
        return send_file(pdf_output_path, as_attachment=True, download_name="final_output.pdf")

    except Exception as e:
        return jsonify({"message": f"Error processing file: {e}"}), 500
    finally:
        os.remove(file_path)

def extract_unique_tokens_and_replace(input_csv, output_csv, service_url):
    """
    Process a CSV file to extract unique text tokens, send for replacement, and update the CSV.
    
    :param input_csv: Path to the input CSV file.
    :param output_csv: Path to save the updated CSV file.
    :param service_url: URL of the service providing replacement mapping.
    """
    # Step 1: Read the CSV file
    df = pd.read_csv(input_csv)
    
    # Step 2: Extract all unique text tokens
    unique_tokens = set()
    token_to_rows = defaultdict(list)  # Map to track where each token appears

    for col in df.columns:
        for idx, cell in df[col].items():
            if pd.notna(cell):  # Ignore NaN cells
                # Split cell into tokens using regex
                tokens = re.findall(r'\b\w+\b', str(cell))
                unique_tokens.update(tokens)
                for token in tokens:
                    token_to_rows[token].append((idx, col))  # Track occurrences

    # Step 3: Prepare JSON payload for the service
    json_payload = {"text": [{"content": token} for token in unique_tokens],"gradation_level" :4}

    # Step 4: Send tokens to the service
    response = requests.post(service_url, json=json_payload)
    if response.status_code != 200:
        raise ValueError(f"Error from service: {response.text}")
    replacement_map = response.json()  # Expected to be in format {"old_token": "new_token"}

    # Step 5: Replace tokens in the original dataframe
    for old_token, new_token in replacement_map.items():
        for idx, col in token_to_rows[old_token]:
            # Update the cell with the replacement
            cell_value = df.at[idx, col]
            df.at[idx, col] = re.sub(rf'\b{old_token}\b', new_token, str(cell_value))

    # Step 6: Save the updated DataFrame to a new CSV file
    df.to_csv(output_csv, index=False)

# extract_unique_tokens_and_replace(, output_csv_path, replacement_service_url)       
def send_to_redaction_process(json_path):
    """Send the combined JSON data to the redaction API."""
    redaction_url = "http://127.0.0.1:8000/redactionprocess"
    with open(json_path, "rb") as json_file:
        try:
            response = requests.post(redaction_url, files={"file": json_file})
            response.raise_for_status()
            return response.json()  # assuming the second API returns JSON
        except requests.RequestException as e:
            print(e)
            raise Exception(f"Error in redaction process: {e}")


# ----------------------------------------------------------------------------------------------


# # Set upload folder and allowed extensions
UPLOAD_FOLDER2 = os.path.join(os.getcwd(), "uploads2")
OUTPUT_FOLDER2 = os.path.join(os.getcwd(), "outputs2")
os.makedirs(UPLOAD_FOLDER2, exist_ok=True)
os.makedirs(OUTPUT_FOLDER2, exist_ok=True)

app.config["UPLOAD_FOLDER2"] = UPLOAD_FOLDER2
app.config["OUTPUT_FOLDER2"] = OUTPUT_FOLDER2


@app.route("/redact-document", methods=["POST"])
def redact_document_all():
    if "file" not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files["file"]
    gradation = request.form.get("gradation", "default")
    custom_gradation = request.form.get("custom_gradation", "[]")

    file_type = file.content_type  # Store the file type
    print(file_type)
    print(gradation)
    print(custom_gradation)
    
    if file.filename == "":
        return jsonify({"message": "No selected file"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER2"], filename)
    file.save(file_path)
            
    replacement_map = request.form.get("replacement_map", "{}")
    try:
        replacement_map = json.loads(replacement_map)  # Convert JSON string to Python dict
    except json.JSONDecodeError:
        return jsonify({"message": "Invalid replacement_map format"}), 400

    
    try:
        processor = DocumentProcessorFactory.create_processor(file_path)
        extracted_text = processor.extract_text()
        external_api_url = "http://127.0.0.1:8001/redactionprocess-doc"
        payload = {
            "text": extracted_text,
            "gradation_level": gradation,
            "custom_tags": custom_gradation
        }
        try:
            response = requests.post(external_api_url, json=payload, headers={"Content-Type": "application/json"})
            replacement_map = response.json() if isinstance(response.json(), dict) else {}  # Ensure it's a dict

        except requests.RequestException as e:
            return jsonify({"message": f"Error communicating with external API: {e}"}), 500

        # Perform redaction and reconstruct the document
        redacted_output_path = os.path.join(OUTPUT_FOLDER2, f"redacted_{filename}")
        processor.replace_text(replacement_map, output_path=redacted_output_path)
                
        from mimetypes import guess_type
        file_mimetype, _ = guess_type(redacted_output_path) # Dynamically determine MIME type based on the file extension

        return send_file(
            redacted_output_path,
            as_attachment=True,
            download_name=f"redacted_{filename}",
            mimetype=file_mimetype,
        )
    except requests.RequestException as e:
        print(f"Error communicating with the redaction API: {e}")
        return jsonify({"message": f"Error communicating with the redaction API: {e}"}), 500

    except Exception as e:
        print(f"Error processing file: {e}")
        return jsonify({"message": f"Error processing file: {e}"}), 500

    finally:
        if os.path.exists(file_path):
            os.remove(file_path) # Cleanup uploaded file


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)