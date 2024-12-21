import os
import cv2
import numpy as np
import subprocess
import logging
from flask import Flask, request, send_file, jsonify,send_from_directory
from werkzeug.utils import secure_filename
from imutils.object_detection import non_max_suppression
from ultralytics import YOLO
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Ensure upload and processing directories exist
UPLOAD_FOLDER = r"C:\Users\Swarnim Raj\Desktop\REDACT-TOOL\backend\uploads"
PROCESSED_FOLDER = r"C:\Users\Swarnim Raj\Desktop\REDACT-TOOL\backend\processed_videos"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Validate model paths
FACE_MODEL_PATH = 'yolov8n-face.pt'
TEXT_MODEL_PATH = 'frozen_east_text_detection.pb'

def validate_model_paths():
    """Validate that required model files exist"""
    if not os.path.exists(FACE_MODEL_PATH):
        logger.error(f"Face model not found at {FACE_MODEL_PATH}")
        raise FileNotFoundError(f"Face model not found at {FACE_MODEL_PATH}")
    
    if not os.path.exists(TEXT_MODEL_PATH):
        logger.error(f"Text detection model not found at {TEXT_MODEL_PATH}")
        raise FileNotFoundError(f"Text detection model not found at {TEXT_MODEL_PATH}")

try:
    # Load pre-trained models
    validate_model_paths()
    face_model = YOLO(FACE_MODEL_PATH)
    text_model = cv2.dnn.readNet(TEXT_MODEL_PATH)
except Exception as e:
    logger.error(f"Error loading models: {e}")
    raise

def process_video(input_video_path, output_video_path):
    """
    Process video to blur faces and text
    
    Args:
        input_video_path (str): Path to input video
        output_video_path (str): Path to save processed video
    """
    try:
        # Load the input video
        cap = cv2.VideoCapture(input_video_path)
        
        if not cap.isOpened():
            logger.error(f"Failed to open video file: {input_video_path}")
            raise ValueError(f"Could not open video file: {input_video_path}")

        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Initialize the VideoWriter for saving the output video
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1
            logger.debug(f"Processing frame {frame_count}")

            orig = frame.copy()
            (H, W) = frame.shape[:2]

            # Face Detection
            face_results = face_model.predict(frame, conf=0.40)
            for result in face_results:
                for box in result.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    # Extract the face region of interest (ROI)
                    face_roi = frame[y1:y2, x1:x2]

                    # Apply Gaussian blur to the face ROI
                    blurred_face = cv2.GaussianBlur(face_roi, (99, 99), 30)

                    # Replace the face region in the frame with the blurred version
                    frame[y1:y2, x1:x2] = blurred_face

            # Text Detection
            # Define new width and height for EAST model and calculate scale ratios
            (newW, newH) = (640, 320)
            rW = W / float(newW)
            rH = H / float(newH)

            # Resize the image for EAST processing
            resized_frame = cv2.resize(frame, (newW, newH))
            (H, W) = resized_frame.shape[:2]

            # Define the output layers for the EAST model
            layer_names = [
                "feature_fusion/Conv_7/Sigmoid",
                "feature_fusion/concat_3",
            ]

            # Create a blob from the resized frame
            blob = cv2.dnn.blobFromImage(resized_frame, 1.0, (W, H),
                                         (123.68, 116.78, 103.94), swapRB=True, crop=False)
            text_model.setInput(blob)
            (scores, geometry) = text_model.forward(layer_names)

            (numRows, numCols) = scores.shape[2:4]
            rects = []
            confidences = []

            # Loop over rows and columns of the score map
            for y in range(0, numRows):
                scores_data = scores[0, 0, y]
                xData0 = geometry[0, 0, y]
                xData1 = geometry[0, 1, y]
                xData2 = geometry[0, 2, y]
                xData3 = geometry[0, 3, y]
                anglesData = geometry[0, 4, y]

                for x in range(0, numCols):
                    if scores_data[x] < 0.5:
                        continue

                    (offsetX, offsetY) = (x * 4.0, y * 4.0)
                    angle = anglesData[x]
                    cos = np.cos(angle)
                    sin = np.sin(angle)

                    h = xData0[x] + xData2[x]
                    w = xData1[x] + xData3[x]

                    endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
                    endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
                    startX = int(endX - w)
                    startY = int(endY - h)

                    rects.append((startX, startY, endX, endY))
                    confidences.append(scores_data[x])

            # Apply non-maxima suppression for text boxes
            boxes = non_max_suppression(np.array(rects), probs=confidences)

            for (startX, startY, endX, endY) in boxes:
                # Scale box coordinates back to the original image size
                startX = int(startX * rW)
                startY = int(startY * rH)
                endX = int(endX * rW)
                endY = int(endY * rH)

                # Extract the text region of interest (ROI)
                text_roi = orig[startY:endY, startX:endX]

                # Apply Gaussian blur to the text ROI
                blurred_text = cv2.GaussianBlur(text_roi, (51, 51), 30)

                # Replace the text region in the frame with the blurred version
                frame[startY:endY, startX:endX] = blurred_text

            # Write the processed frame to the output video
            out.write(frame)

        # Release resources
        cap.release()
        out.release()
        
        logger.info(f"Video processing complete. Processed {frame_count} frames.")
        
    except Exception as e:
        logger.error(f"Error processing video: {e}")
        raise

def merge_audio_video(input_video, input_audio, output_video):
    """
    Merge processed video with original audio
    
    Args:
        input_video (str): Path to processed video without audio
        input_audio (str): Path to original audio file
        output_video (str): Path to save final video with audio
    """
    try:
        subprocess.run([
            "ffmpeg", "-y", "-i", input_video, "-i", input_audio, 
            "-c:v", "copy", "-c:a", "aac", "-strict", "experimental", 
            output_video
        ], check=True, capture_output=True, text=True)
        logger.info(f"Audio merged successfully to {output_video}")
    except subprocess.CalledProcessError as e:
        logger.error(f"FFmpeg error: {e.stderr}")
        raise RuntimeError(f"Failed to merge audio: {e.stderr}")

@app.route('/upload-video', methods=['POST'])
def redact_video():
    """
    API endpoint for video redaction
    """
    print("we are")
    try:
        if 'video' not in request.files:
            logger.warning("No video file uploaded")
            return jsonify({"error": "No video file uploaded"}), 400
        
        video = request.files['video']
        
        # Secure filename and create full paths
        filename = secure_filename(video.filename)
        input_video_path = os.path.join(UPLOAD_FOLDER, filename)
        
        print("input_video_path", input_video_path)
        
        processed_video_path = os.path.join(PROCESSED_FOLDER, f"processed_{filename}")
        print("processed_video_path", processed_video_path)
        
        final_output_path = os.path.join(PROCESSED_FOLDER, f"final_{filename}")
        print("final_output_path", final_output_path)
        
        audio_path = os.path.join(UPLOAD_FOLDER, f"audio_{filename.split('.')[0]}.aac")
        print("audio_path", audio_path)

        # Save uploaded video
        video.save(input_video_path)
        logger.info(f"Video saved to {input_video_path}")

        # Extract audio from original video
        subprocess.run([
            "ffmpeg", "-i", input_video_path, "-vn", "-acodec", "copy", audio_path
        ], check=True)
        print("hhhhhhhh")
        logger.info(f"Audio extracted to {audio_path}")  #yaha error ara
        print("we are here1")
        # Process video
        process_video(input_video_path, processed_video_path)
        print("vid process ho gya hai")
        # Merge processed video with original audio
        merge_audio_video(processed_video_path, audio_path, final_output_path)
        print("heheheh123")
         # Return the processed video file path
        return jsonify({
            "message": "Video processed successfully", 
            "output_video": os.path.basename(final_output_path)
        }), 200


    except Exception as e:
        logger.error(f"Unexpected error in video redaction: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
    finally:
        # Clean up files (optional, but recommended)
        for file_path in [input_video_path, processed_video_path, audio_path]:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    logger.info(f"Removed temporary file: {file_path}")
            except Exception as cleanup_error:
                logger.warning(f"Error cleaning up {file_path}: {cleanup_error}")
                
@app.route('/download-video/<filename>')
def download_video(filename):
    """
    Endpoint to download processed video
    """
    try:
        full_path = os.path.join(PROCESSED_FOLDER, filename)
        
        # Additional logging and error checking
        if not os.path.exists(full_path):
            logger.error(f"File not found: {full_path}")
            return jsonify({"error": "File not found"}), 404

        return send_file(
            full_path, 
            mimetype='video/mp4',
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        logger.error(f"Error downloading video: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8004)

