"""
Automated Metadata Generation System - Web Application
=====================================================

This is the main Streamlit web application that provides a user-friendly interface
for uploading documents and viewing extracted metadata.

Features:
- Upload PDF, DOCX, and TXT files
- Extract text using OCR when needed
- Generate metadata (title, author, dates, keywords, summary)
- Display results in a clean, organized format
- Download metadata as JSON

Author: Your Name
Date: June 2025
"""

import streamlit as st
import json
import logging
from datetime import datetime
import traceback
import streamlit as st

# --- Custom CSS to make uploader and sidebar text white ---
st.markdown("""
<style>
/* Make the 'Drag and drop file here' text white */
[data-testid="stFileUploaderDropzoneInstructions"] > div > span {
    color: #fff !important;
}
/* Make the 'Limit 200MB per file' and file types text white */
[data-testid="stFileDropzoneInstructions"] {
    color: #fff !important;
}
/* Make all sidebar text white */
section[data-testid="stSidebar"] * {
    color: #fff !important;
}
/* Hide the default file limit/type text */
div[data-testid="stFileUploaderDropzoneInstructions"] > div > small {
    visibility: hidden;
    height: 0;
    margin: 0;
    padding: 0;
}

/* Add your own white text after the drag-and-drop span */
div[data-testid="stFileUploaderDropzoneInstructions"] > div > span::after {
    content: "  |  Limit 200MB per file • PDF, DOCX, TXT";
    display: block;
    color: #fff !important;
    font-size: 0.9em;
    font-weight: normal;
    margin-top: 2px;
}
</style>
""", unsafe_allow_html=True)

# Import our custom modules
from document_processor import DocumentProcessor
from metadata_extractor import MetadataExtractor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Streamlit page
st.set_page_config(
    page_title="Metadata Generation System",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
    }
    .metadata-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #3498db;
        margin: 1rem 0;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #f5c6cb;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables."""
    if 'processed_text' not in st.session_state:
        st.session_state.processed_text = ""
    if 'metadata' not in st.session_state:
        st.session_state.metadata = {}
    if 'processing_complete' not in st.session_state:
        st.session_state.processing_complete = False

def display_header():
    """Display the application header."""
    st.markdown('<h1 class="main-header">📄 Automated Metadata Generation System</h1>', 
                unsafe_allow_html=True)

    st.markdown("""
    Welcome to the **Automated Metadata Generation System**! This tool helps you:

    🔍 **Extract text** from PDF, DOCX, and TXT files  
    🧠 **Analyze content** using NLP techniques  
    📋 **Generate metadata** including title, author, keywords, and summary  
    💾 **Export results** in JSON format  

    ---
    """)

def display_sidebar():
    """Display the sidebar with instructions and information."""
    with st.sidebar:
        st.header("📚 How to Use")
        st.markdown("""
        **Step 1:** Upload a document  
        **Step 2:** Wait for processing  
        **Step 3:** View extracted metadata  
        **Step 4:** Download results  

        ---

        **Supported Formats:**
        - 📄 PDF (with OCR support)
        - 📝 DOCX (Microsoft Word)
        - 📃 TXT (Plain text)

        ---

        **Features:**
        - ✅ Title extraction
        - ✅ Author detection  
        - ✅ Date identification
        - ✅ Keyword extraction
        - ✅ Text summarization
        - ✅ Word/character count

        ---

        **Tips:**
        - Larger files may take longer to process
        - OCR is used for image-based PDFs
        - Clean, well-formatted documents work best
        """)

def process_uploaded_file(uploaded_file):
    """
    Process the uploaded file and extract metadata.

    Args:
        uploaded_file: Streamlit uploaded file object

    Returns:
        tuple: (success: bool, message: str, metadata: dict)
    """
    try:
        # Show processing message
        with st.spinner('🔄 Processing your document...'):
            # Initialize processors
            doc_processor = DocumentProcessor()
            metadata_extractor = MetadataExtractor()

            # Get file details
            file_name = uploaded_file.name
            file_type = file_name.split('.')[-1].lower()
            file_content = uploaded_file.read()

            st.info(f"📁 Processing file: **{file_name}** ({file_type.upper()})")

            # Create progress bar
            progress_bar = st.progress(0)
            progress_text = st.empty()

            # Step 1: Extract text
            progress_text.text("Step 1/3: Extracting text from document...")
            progress_bar.progress(33)

            extracted_text = doc_processor.process_document(file_content, file_type)

            if not extracted_text or len(extracted_text.strip()) < 10:
                return False, "❌ Could not extract meaningful text from the document.", {}

            # Step 2: Process metadata
            progress_text.text("Step 2/3: Analyzing content and extracting metadata...")
            progress_bar.progress(66)

            metadata = metadata_extractor.extract_metadata(extracted_text)

            # Step 3: Finalize
            progress_text.text("Step 3/3: Finalizing results...")
            progress_bar.progress(100)

            # Store in session state
            st.session_state.processed_text = extracted_text
            st.session_state.metadata = metadata
            st.session_state.processing_complete = True

            # Clear progress indicators
            progress_bar.empty()
            progress_text.empty()

            return True, "✅ Document processed successfully!", metadata

    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        error_details = traceback.format_exc()
        return False, f"❌ Error processing document: {str(e)}", {}

def display_metadata(metadata):
    """
    Display the extracted metadata in a formatted way.

    Args:
        metadata (dict): The extracted metadata dictionary
    """
    st.markdown('<h2 class="section-header">📋 Extracted Metadata</h2>', 
                unsafe_allow_html=True)

    # Create columns for better layout
    col1, col2 = st.columns(2)

    with col1:
        # Title
        st.markdown("**📖 Title:**")
        st.markdown(f'<div class="metadata-box">{metadata.get("title", "N/A")}</div>', 
                   unsafe_allow_html=True)

        # Author
        st.markdown("**👤 Author:**")
        st.markdown(f'<div class="metadata-box">{metadata.get("author", "N/A")}</div>', 
                   unsafe_allow_html=True)

        # Dates
        st.markdown("**📅 Dates Found:**")
        dates = metadata.get("dates", [])
        if dates:
            dates_text = "<br>".join([f"• {date}" for date in dates])
        else:
            dates_text = "No dates found"
        st.markdown(f'<div class="metadata-box">{dates_text}</div>', 
                   unsafe_allow_html=True)

    with col2:
        # Statistics
        st.markdown("**📊 Document Statistics:**")
        stats_html = f"""
        • **Word Count:** {metadata.get("word_count", 0):,}<br>
        • **Character Count:** {metadata.get("character_count", 0):,}<br>
        • **Processed:** {metadata.get("extraction_date", "N/A")}
        """
        st.markdown(f'<div class="metadata-box">{stats_html}</div>', 
                   unsafe_allow_html=True)

        # Keywords
        st.markdown("**🔍 Keywords:**")
        keywords = metadata.get("keywords", [])
        if keywords:
            # Display keywords as tags
            keyword_tags = " ".join([f'`{keyword}`' for keyword in keywords[:10]])
            st.markdown(keyword_tags)
        else:
            st.markdown("No keywords extracted")

    # Summary (full width)
    st.markdown("**📝 Summary:**")
    summary = metadata.get("summary", "No summary available")
    st.markdown(f'<div class="metadata-box">{summary}</div>', 
               unsafe_allow_html=True)

def display_download_section(metadata):
    """
    Display the download section for exporting metadata.

    Args:
        metadata (dict): The metadata to export
    """
    st.markdown('<h2 class="section-header">💾 Export Data</h2>', 
                unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        # Download as JSON
        json_data = json.dumps(metadata, indent=2, ensure_ascii=False)
        st.download_button(
            label="📄 Download Metadata (JSON)",
            data=json_data,
            file_name=f"metadata_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

    with col2:
        # Download extracted text
        if st.session_state.processed_text:
            st.download_button(
                label="📃 Download Extracted Text",
                data=st.session_state.processed_text,
                file_name=f"extracted_text_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )

    with col3:
        # Clear session (reset)
        if st.button("🔄 Process New Document"):
            st.session_state.processed_text = ""
            st.session_state.metadata = {}
            st.session_state.processing_complete = False
            st.rerun()
()

def main():
    """Main application function."""
    # Initialize session state
    initialize_session_state()

    # Display header and sidebar
    display_header()
    display_sidebar()

    # File upload section
    st.markdown('<h2 class="section-header">📤 Upload Document</h2>', 
                unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Choose a file to process",
        type=['pdf', 'docx', 'txt'],
        help="Upload a PDF, DOCX, or TXT file to extract metadata"
    )

    if uploaded_file is not None:
        # Display file details
        file_details = {
            "Filename": uploaded_file.name,
            "File size": f"{uploaded_file.size:,} bytes",
            "File type": uploaded_file.type
        }

        st.json(file_details)

        # Process button
        if st.button("🚀 Extract Metadata", type="primary"):
            success, message, metadata = process_uploaded_file(uploaded_file)

            if success:
                st.markdown(f'<div class="success-message">{message}</div>', 
                           unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="error-message">{message}</div>', 
                           unsafe_allow_html=True)

    # Display results if processing is complete
    if st.session_state.processing_complete and st.session_state.metadata:
        display_metadata(st.session_state.metadata)
        display_download_section(st.session_state.metadata)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #7f8c8d; margin-top: 2rem;">
        <p>🛠️ Built with Streamlit • 📄 Powered by PyMuPDF & pytesseract</p>
        <p>Made with ❤️ for document processing automation</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()