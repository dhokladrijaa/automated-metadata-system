# Automated Metadata Generation System

> **Automatically extract text and generate metadata from your documents with a simple web interface.**

---

## 📄 Project Overview

This project is an **Automated Metadata Generation System** that extracts text from unstructured documents (PDF, DOCX, TXT) and generates structured metadata such as **title, author, date, keywords, and summary**. It provides a user-friendly web interface for uploading documents and viewing the generated metadata.

---

## ✨ Features

- Extract text from PDF, DOCX, and TXT files
- OCR support for image-based PDFs using pytesseract
- Metadata extraction using rule-based and basic NLP techniques
- Web interface built with Streamlit for easy document upload and metadata display
- Export metadata as JSON

---
##  Live Demo
> [https://automated-metadata-system-zfz298g5zoexhtpo9qhh8d.streamlit.app/](https://automated-metadata-system-zfz298g5zoexhtpo9qhh8d.streamlit.app/)

## 📁 Project Structure

```
automated-metadata-system/
├── app.py # Main Streamlit application
├── document_processor.py # Text extraction module
├── metadata_extractor.py # Metadata generation module
├── notebook.ipynb # Jupyter notebook with examples
├── requirements.txt # Python dependencies
├── README.md # Project documentation
├── demo_script.md # Demo video script
└── sample_documents/ # Test files
    ├── sample.pdf
    ├── sample.docx
    └── sample.txt
```

---

## ⚙️ Installation

1. **Clone the repository:**
    ```
    git clone https://github.com/yourusername/automated-metadata-system.git
    cd automated-metadata-system
    ```

2. **Create and activate a virtual environment:**
    ```
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3. **Install dependencies:**
    ```
    pip install -r requirements.txt
    ```

---

## 🚀 Usage

Run the Streamlit app:

`streamlit run app.py`


Upload PDF, DOCX, or TXT files through the web interface to extract metadata.

---

## Video Demonstration Drive link- 
https://drive.google.com/file/d/13EYJuQ2rbbdkwwDndNpoZCB5kBwOWXQ6/view?usp=sharing
