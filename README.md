📄 Automated Metadata Generation System
A beginner-friendly Python project that automatically extracts text from documents and generates structured metadata using Natural Language Processing techniques.

🎯 What This Project Does
This system takes unstructured documents (PDF, DOCX, TXT) and automatically:

Extracts text from various document formats

Uses OCR for image-based PDFs

Identifies key information like title, author, and dates

Extracts important keywords from the content

Generates summaries of the document

Provides a web interface for easy use

Exports results in JSON format

🌟 Key Features
✅ Multi-format support: PDF, DOCX, and TXT files

✅ OCR capabilities: Handles image-based PDFs

✅ Smart metadata extraction: Title, author, dates, keywords

✅ Text summarization: Automatic content summarization

✅ Web interface: User-friendly Streamlit app

✅ Export functionality: Download results as JSON

✅ Beginner-friendly: Well-commented, modular code

🛠️ Technology Stack
Python 3.8+: Main programming language

Streamlit: Web application framework

PyMuPDF: PDF text extraction and processing

pytesseract: OCR for image-based text

python-docx: Microsoft Word document processing

PIL (Pillow): Image processing for OCR

📁 Project Structure
text
automated-metadata-system/
├── app.py                      # Main Streamlit web application
├── document_processor.py       # Text extraction from documents
├── metadata_extractor.py       # NLP and metadata generation
├── notebook.ipynb             # Jupyter notebook with examples
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── demo_script.md             # Demo video script
└── sample_documents/           # Sample files for testing
    ├── sample.pdf
    ├── sample.docx
    └── sample.txt
🚀 How to Run the Project
Step 1: Set Up Your Environment
Create a virtual environment (recommended):

bash
python -m venv metadata_env
Activate the virtual environment:

Windows: metadata_env\Scripts\activate

Mac/Linux: source metadata_env/bin/activate

Install dependencies:

bash
pip install -r requirements.txt
Step 2: Install Tesseract OCR
For Windows:

Download Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki

Install it (remember the installation path)

Add Tesseract to your system PATH

For Mac:

bash
brew install tesseract
For Linux (Ubuntu/Debian):

bash
sudo apt update
sudo apt install tesseract-ocr
Step 3: Run the Application
Start the Streamlit web app:

bash
streamlit run app.py
Open your browser to http://localhost:8501

Upload a document and click "Extract Metadata"

View the results and download if needed

💻 Using the Jupyter Notebook
Start Jupyter:

bash
jupyter notebook
Open notebook.ipynb

Run the cells to see step-by-step examples

📖 How It Works
1. Document Processing (document_processor.py)
PDF Files: Uses PyMuPDF to extract text directly

Image-based PDFs: Falls back to OCR using pytesseract

DOCX Files: Extracts text from paragraphs and tables

TXT Files: Handles various text encodings

2. Metadata Extraction (metadata_extractor.py)
Title Detection: Finds the first meaningful line or title patterns

Author Extraction: Looks for "by [name]" or "author: [name]" patterns

Date Finding: Uses regex to find various date formats

Keyword Extraction: Frequency analysis of important terms

Summarization: Scores sentences based on keyword presence

3. Web Interface (app.py)
File Upload: Drag-and-drop interface for documents

Progress Tracking: Real-time processing status

Results Display: Clean, organized metadata presentation

Export Options: Download JSON and extracted text

🔧 Customization
Adding New File Types
Extend DocumentProcessor:

python
def extract_text_from_new_format(self, file_content):
    # Your extraction logic here
    return extracted_text
Update the process_document method:

python
elif file_type.lower() == 'new_format':
    return self.extract_text_from_new_format(file_content)
Improving Metadata Extraction
Add new patterns in MetadataExtractor:

python
new_patterns = [
    r'your_regex_pattern_here',
    r'another_pattern'
]
Enhance keyword extraction with domain-specific terms:

python
domain_keywords = ['specific', 'terms', 'for', 'your', 'domain']
🌐 Deployment Options
Option 1: Streamlit Community Cloud (Free)
Push your code to GitHub

Visit share.streamlit.io

Connect your repository

Deploy with one click

Option 2: Local Network
Run with external access:

bash
streamlit run app.py --server.address 0.0.0.0
Access from other devices on your network

Option 3: Docker (Advanced)
Create Dockerfile:

text
FROM python:3.9-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
🐛 Troubleshooting
Common Issues
Tesseract not found:

Make sure Tesseract is installed and in your PATH

On Windows, you might need to specify the path in your code

Memory issues with large PDFs:

Try processing smaller files first

Consider splitting large documents

Poor OCR results:

Ensure images are high quality

Try preprocessing images (contrast, brightness)

Dependencies not installing:

Make sure you're using Python 3.8+

Try upgrading pip: pip install --upgrade pip

📊 Example Input/Output
Input Document:
text
The Art of Machine Learning
By Dr. Sarah Johnson
Published: March 15, 2024

Machine learning is a subset of artificial intelligence that enables
computers to learn and improve from experience without being explicitly
programmed. This field has revolutionized how we approach data analysis
and prediction tasks across various industries.
Generated Metadata:
json
{
  "title": "The Art of Machine Learning",
  "author": "Dr. Sarah Johnson",
  "dates": ["March 15, 2024"],
  "keywords": ["machine", "learning", "artificial", "intelligence", "data"],
  "summary": "Machine learning is a subset of artificial intelligence that enables computers to learn and improve from experience. This field has revolutionized data analysis and prediction tasks across industries.",
  "word_count": 45,
  "character_count": 287,
  "extraction_date": "2024-06-22 10:30:45"
}
🤝 Contributing
This is a learning project! Feel free to:

Add new features (better NLP, more file formats)

Improve the UI (better styling, new components)

Fix bugs (error handling, edge cases)

Add tests (unit tests, integration tests)

📝 License
This project is open source and available under the MIT License.

🙋‍♀️ Getting Help
If you run into issues:

Check the troubleshooting section above

Look at the code comments for explanations

Try the sample documents to test functionality

Start with simpler documents before complex ones

🎓 Learning Outcomes
After completing this project, you'll understand:

✅ Document processing and text extraction

✅ Basic Natural Language Processing techniques

✅ Web application development with Streamlit

✅ Error handling and logging in Python

✅ Project structure and modular programming

✅ Working with external libraries and APIs