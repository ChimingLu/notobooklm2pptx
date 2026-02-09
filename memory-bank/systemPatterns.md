# System Patterns

## Architecture
The application follows a modular architecture, separating the core processing logic from the user interfaces.

```mermaid
flowchart TD
    User -->|Interacts| CLI[CLI (main.py / convert_ultimate.py)]
    User -->|Interacts| GUI[GUI (gui.py)]
    
    CLI --> Core[Core Logic (lib/)]
    GUI --> Core
    
    subgraph Core Logic
        PDF[pdf_processor.py]
        OCR[ocr_opensource.py]
        Clean[image_cleaner_lama.py]
        PPTX[pptx_generator.py]
    end
    
    Core -->|Uses| EasyOCR[EasyOCR Model]
    Core -->|Uses| Lama[Lama Cleaner Model]
    Core -->|Uses| PDFium[pypdfium2]
    Core -->|Uses| PyPPTX[python-pptx]
```

## Key Components

### 1. Interface Layer
- **CLI (`main.py`, `convert_ultimate.py`)**: Provides command-line access with rich output. `convert_ultimate.py` is the primary entry point for high-quality local conversion.
- **GUI (`gui.py`)**: A Flet-based desktop application for user-friendly interaction.

### 2. Processing Layer (`lib/`)
- **PDF Processor (`pdf_processor.py`)**: Converts PDF pages to high-quality images using `pypdfium2`.
- **OCR Engine (`ocr_opensource.py`)**: Uses **EasyOCR** locally to detect and extract text, recognizing layout and font sizes.
- **Image Cleaner (`image_cleaner_lama.py`)**: Uses **Lama Cleaner (IOPaint)** to intelligently remove text from images, restoring the original background.
- **PPTX Generator (`pptx_generator.py`)**: Synthesizes the text and cleaned background into a native `.pptx` file.

## Design Patterns
- **Strategy Pattern**: Different conversion strategies (Ultimate/Free/Legacy) can be swapped easily.
- **Asynchronous Processing**: Ensures UI responsiveness during heavy AI model inference.
- **Local-First Architecture**: Prioritizes local execution for privacy and reliability.
