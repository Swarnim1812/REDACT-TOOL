import cv2
import numpy as np
from paddleocr import PaddleOCR
from PIL import Image
from fpdf import FPDF
import matplotlib.pyplot as plt
import os
import json
from PIL import ImageEnhance, ImageFilter

# Base class for document processing
class DocumentProcessor:
    def __init__(self):
        self.metadata = {}
        self.text_objects = []
        self.visual_elements = []


    def extract_metadata(self, image_path):
        # Read image with OpenCV to get pixel dimensions
        image = cv2.imread(image_path)
        height, width, _ = image.shape

        # Store metadata
        self.metadata = {
            "width": width,
            "height": height,
            "pages": 1
        }

    def save_results(self, output_path):
        grouped_data = {
            "metadata": self.metadata,
            "text": self.text_objects,
            "visual_elements": self.visual_elements,
        }
        with open(output_path, "w") as file:
            json.dump(grouped_data, file, indent=4)
        print(f"Results saved to {output_path}")
        return grouped_data

# Subclass for image-specific processing
class ImageProcessor(DocumentProcessor):
    def __init__(self, ocr_language="en"):
        super().__init__()
        self.ocr = PaddleOCR(use_angle_cls=True, lang=ocr_language)

    def process_image(self, image_path):
        # Load and preprocess image
        image = cv2.imread(image_path)
        if image.shape[2] == 3:  # Ensure alpha channel
            image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

        self.extract_metadata(image_path)

        # Perform OCR
        result = self.ocr.ocr(image_path, cls=True)
        self._process_text(image, result)

        # Detect shapes
        tp_image = cv2.imread("telea_transparent.png")
        thresh = self._preprocess_for_shapes(tp_image)
        self._detect_shapes(thresh, image)

        return image

    def _process_text(self, image, ocr_result):
        available_font = [8,14,18,24,32,40,48]
        for idx in range(len(ocr_result)):
            for line in ocr_result[idx]:
                # Extract bounding box and text
                box = np.array(line[0], dtype=np.int32)
                text = line[1][0]

                # Calculate the font size by the height of the bounding box
                x, y, w, h = cv2.boundingRect(box)
                font_size = int(0.5 * h)  # Approximation of font size
                font_size = min(available_font, key=lambda x: abs(x - font_size))
                # Crop the text region from the image
                text_region = image[y:y + h, x:x + w]
                text_region_gray = cv2.cvtColor(text_region, cv2.COLOR_BGRA2GRAY)

                # Threshold the text region to isolate text pixels
                _, binary_text = cv2.threshold(text_region_gray, 128, 255, cv2.THRESH_BINARY_INV)

                # Approximate font weight as the ratio of text pixels to total pixels
                text_pixels = np.sum(binary_text == 255)
                total_pixels = binary_text.size
                font_weight_ratio = text_pixels / total_pixels
                # Normalize coordinates and store text object
                self.text_objects.append({
                    "coordinates": (box / [self.metadata["width"], self.metadata["height"]]).tolist(),
                    "content": text,
                    "font_size": font_size,
                    "font_weight": font_weight_ratio,
                })

                # Make text region transparent
                pad = 1
                image[y-pad:y + h+pad, x-pad:x + w+pad, 3] = 0

        # Convert image from BGRA (OpenCV) to RGBA (Pillow)
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)

        # Convert to Pillow Image
        pil_image = Image.fromarray(image)
        image_np = np.array(pil_image)

        bgr = image_np[:, :, :3]  # BGR channels
        alpha = image_np[:, :, 3]
        # Create a mask where transparency exists
        mask = (alpha == 0).astype(np.uint8)

        # Apply inpainting using Telea
        inpainted_telea = cv2.inpaint(bgr, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)

        # Save the results
        inpainted_telea = cv2.cvtColor(inpainted_telea, cv2.COLOR_BGR2RGBA)
        cv2.imwrite("telea_transparent.png", inpainted_telea)

        # Save image (it should now have the correct colors)
        pil_image.save("transparent.png")
        return pil_image



    def _preprocess_for_shapes(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
        )
        return cv2.medianBlur(thresh, 5)

    def _detect_shapes(self, thresh, image):
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            # Approximate contour
            epsilon = 0.01 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            x, y, w, h = cv2.boundingRect(approx)

            if w * h < 1000:  # Filter small shapes
                continue

            # Classify shape
            shape = self._classify_shape(approx, contour)
            self.visual_elements.append({
                "bbox": [x / self.metadata["width"], y / self.metadata["height"],
                         w / self.metadata["width"], h / self.metadata["height"]],
                "shape": shape,
            })

    def _classify_shape(self, approx, contour):
        vertices = len(approx)
        if vertices == 3:
            return "Triangle"
        elif vertices == 4:
            aspect_ratio = float(cv2.boundingRect(approx)[2]) / cv2.boundingRect(approx)[3]
            return "Square" if 0.95 <= aspect_ratio <= 1.05 else "Rectangle"
        elif vertices > 4:
            area = cv2.contourArea(contour)
            perimeter = cv2.arcLength(contour, True)
            circularity = (4 * np.pi * area) / (perimeter ** 2) if perimeter > 0 else 0
            return "Circle" if 0.8 <= circularity <= 1.2 else "Polygon"
        return "Unknown"

    def reconstruct_pdf(self, output_pdf_path, original_image_path):
        
        original_image = Image.open(original_image_path)
        pdf_width, pdf_height = 595.28, 841.89  # A4 size in points
        scale_factor = min(pdf_width / self.metadata["width"], pdf_height / self.metadata["height"])
        print(scale_factor)
        pdf = FPDF(unit="pt", format=[pdf_width, pdf_height])
        pdf.add_page()

        # Draw visual elements
        for idx, element in enumerate(self.visual_elements):
            bbox = element["bbox"]
            x = bbox[0] * self.metadata["width"] * scale_factor
            y = bbox[1] * self.metadata["height"] * scale_factor
            w = bbox[2] * self.metadata["width"] * scale_factor
            h = bbox[3] * self.metadata["height"] * scale_factor

            # Crop, resize, and add to PDF
            crop_box = (int(bbox[0] * self.metadata["width"]),
                        int(bbox[1] * self.metadata["height"]),
                        int((bbox[0] + bbox[2]) * self.metadata["width"]),
                        int((bbox[1] + bbox[3]) * self.metadata["height"]))
            cropped = original_image.crop(crop_box)
            scaled = cropped.resize((max(1,int(w)), max(int(h),1)))

            temp_path = f"temp_{idx}.png"
            scaled.save(temp_path)
            pdf.image(temp_path, x, y, w, h)
            os.remove(temp_path)

        # Draw text
        for text in self.text_objects:
            box = text["coordinates"]
            x = box[0][0] * self.metadata["width"] * scale_factor
            y = box[0][1] * self.metadata["height"] * scale_factor
            pdf.set_xy(x, y)
            print(f"x={x} , y={y}")
            pdf.set_font("Arial", size=text["font_size"], style="B" if text["font_weight"] > 0.5 else "")
            pdf.multi_cell(0, 10, text["content"], border=0)

        pdf.output(output_pdf_path)
        print(f"PDF saved to {output_pdf_path}")


# # Example usage
# if __name__ == "__main__":
#     processor = ImageProcessor()
#     processed_image = processor.process_image("file.jpeg")
#     json = processor.save_results("output.json")
#     print(json)
#     processor.reconstruct_pdf("output.pdf", "telea_transparent.png")