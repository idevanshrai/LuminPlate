import cv2
import torch
import re
from ultralytics import YOLO
import easyocr
from fuzzywuzzy import process  
import numpy as np

model_path = "license_plate_detector.pt"  
model = YOLO(model_path)

image_path = "images.jpeg"  
image = cv2.imread(image_path)

if image is None:
    print(f"❌ Error: Unable to read image at {image_path}. Check the path.")
    exit()

#YOLO Inference
results = model(image, conf=0.5)  # confidence threshold

US_STATES = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida",
    "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine",
    "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska",
    "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio",
    "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas",
    "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
]

MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

# Process
for result in results:
    for box in result.boxes.xyxy:
        x1, y1, x2, y2 = map(int, box)  
        license_plate_crop = image[y1:y2, x1:x2]  

        cropped_path = "cropped_plate.jpg"
        cv2.imwrite(cropped_path, license_plate_crop)
        print(f"✅ License plate saved at {cropped_path}")

        # === Preprocessing===
        gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)  

        kernel = np.ones((3, 3), np.uint8)
        morphed = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)  

        thresh = cv2.adaptiveThreshold(morphed, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)

        # OCR
        reader = easyocr.Reader(['en'])
        ocr_result = reader.readtext(thresh, detail=0)  

        raw_text = " ".join(ocr_result).strip()
        print(f"🔍 Raw OCR Output: {raw_text}")

        # ===(Cursive Fonts)===
        detected_state = None
        possible_states = [word for word in raw_text.split() if len(word) > 3]  
        for state in US_STATES:
            for word in possible_states:
                if process.fuzz.partial_ratio(word.lower(), state.lower()) > 75:  
                    detected_state = state
                    break
            if detected_state:
                break

        # ===Month===
        detected_month = None
        for month in MONTHS:
            if month in raw_text.upper():
                detected_month = month
                break

        # ===Year===
        detected_year = None
        current_year = 2025  

        year_matches = re.findall(r'\b(19\d{2}|20\d{2})\b', raw_text)
        if year_matches:
            detected_year = max(year_matches, key=int)  

        if not detected_year:
            two_digit_years = re.findall(r'\b\d{2}\b', raw_text)
            for year in two_digit_years:
                year_int = int(year)
                if 22 <= year_int <= 99:
                    detected_year = f"20{year}"  
                    break
                elif 0 <= year_int <= 21:
                    detected_year = f"20{year}"  
                    break

        # ===Plate Number=== 
        plate_candidates = re.findall(r'[A-Z0-9]{6,8}', raw_text)  
        detected_plate = plate_candidates[0] if plate_candidates else "None"

        print(f"✅ Detected State: {detected_state if detected_state else 'None'}")
        print(f"✅ Detected Month: {detected_month if detected_month else 'None'}")
        print(f"✅ Detected Year: {detected_year if detected_year else 'None'}")
        print(f"✅ Detected Plate Number: {detected_plate}")

#Print
cv2.imshow("License Plate", license_plate_crop)
cv2.waitKey(0)
cv2.destroyAllWindows()
