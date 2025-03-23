# LuminPlate

LuminPlate is an OCR-based license plate recognition system designed to extract state and registration details from U.S. license plates. The project leverages a YOLO-based detection model and an optimized OCR system to accurately recognize license plate numbers and associated details.

## Features
- **License Plate Detection**: Uses a pre-trained YOLO model to detect U.S. license plates.
- **Text Recognition**: Employs an optimized OCR system for extracting license plate numbers, state, and registration details.
- **Post-Processing**: Intelligent post-processing for enhanced accuracy and error correction.
- **Easy Integration**: Simple CLI-based interface for quick testing and deployment.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/LuminPlate.git
   cd LuminPlate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Ensure you have the model file (`license_plate_detector.pt`) in the project directory.

## Usage

To detect and recognize license plates from an image, run:

```bash
python app.py --image images.jpeg
```

### Input Requirements
- Input image should contain a visible U.S. license plate (e.g., `images.jpeg`).

### Output
- Recognized license plate details are printed on the console.
- The processed image is saved with bounding boxes around detected plates.

## Model Details
- The project uses a YOLO-based model (`license_plate_detector.pt`) for detecting U.S. license plates.
- The OCR system extracts the plate number, state, and registration details.

## Contributing
Contributions are welcome! Feel free to submit pull requests or report issues to improve the project.

## License
This project is licensed under the **MIT License**. 

