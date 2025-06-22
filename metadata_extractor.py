


"""
Metadata Extractor Module
=========================

This module analyzes extracted text and generates structured metadata:
- Title extraction (first significant line or from patterns)
- Author detection (using common patterns)
- Date extraction (various date formats)
- Keyword extraction (important terms)
- Text summarization (short summary of content)

Author: Your Name
Date: June 2025
"""

import logging
import re
from typing import List, Dict, Any, Optional
from collections import Counter
import string
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MetadataExtractor:
    """
    A class to extract metadata from text documents.

    This class uses rule-based methods and simple NLP techniques
    to extract meaningful metadata from document text.
    """

    def __init__(self):
        """Initialize the MetadataExtractor."""
        self.stop_words = set([
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
            'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
            'to', 'was', 'will', 'with', 'but', 'or', 'not', 'this', 'can',
            'have', 'had', 'been', 'their', 'said', 'each', 'which', 'do',
            'how', 'if', 'who', 'what', 'where', 'when', 'why', 'all', 'any',
            'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such'
        ])
        logger.info("MetadataExtractor initialized")

    def extract_title(self, text: str) -> str:
        """
        Extract the title from the document text.

        This method looks for the first meaningful line that could be a title,
        or uses common title patterns.

        Args:
            text (str): The document text

        Returns:
            str: The extracted title or a default title
        """
        try:
            lines = text.split('\n')

            # Remove empty lines and very short lines
            meaningful_lines = [line.strip() for line in lines 
                              if len(line.strip()) > 10 and len(line.strip()) < 200]

            if not meaningful_lines:
                return "Untitled Document"

            # Check for common title patterns
            title_patterns = [
                r'^title[:\s]+(.+)$',  # Title: Something
                r'^(.+)\s*[-—]\s*(.+)$',  # Something - Subtitle
                r'^\s*([A-Z][^.!?]*[^.!?\s])\s*$'  # All caps or sentence case
            ]

            for line in meaningful_lines[:5]:  # Check first 5 meaningful lines
                for pattern in title_patterns:
                    match = re.search(pattern, line, re.IGNORECASE)
                    if match:
                        title = match.group(1).strip()
                        if len(title) > 5:  # Must be at least 5 characters
                            logger.info(f"Title extracted using pattern: {title}")
                            return title

            # If no pattern matches, use the first meaningful line
            first_line = meaningful_lines[0]
            # Remove common document artifacts
            first_line = re.sub(r'^(page\s*\d+|chapter\s*\d+)', '', first_line, flags=re.IGNORECASE)
            first_line = first_line.strip()

            if len(first_line) > 5:
                logger.info(f"Title extracted from first line: {first_line}")
                return first_line

            return "Untitled Document"

        except Exception as e:
            logger.error(f"Error extracting title: {str(e)}")
            return "Untitled Document"

    def extract_author(self, text: str) -> str:
        """
        Extract the author from the document text.

        This method looks for common author patterns in the text.

        Args:
            text (str): The document text

        Returns:
            str: The extracted author or "Unknown Author"
        """
        try:
            # Common author patterns
            author_patterns = [
                r'author[:\s]+([^\n]+)',  # Author: John Doe
                r'by\s+([A-Z][a-z]+\s+[A-Z][a-z]+)',  # by John Doe
                r'written\s+by\s+([^\n]+)',  # written by John Doe
                r'^([A-Z][a-z]+\s+[A-Z][a-z]+)\s*$',  # John Doe (on its own line)
            ]

            for pattern in author_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
                if matches:
                    author = matches[0].strip()
                    # Clean up the author name
                    author = re.sub(r'[^a-zA-Z\s.]', '', author)
                    if len(author) > 3 and len(author) < 50:
                        logger.info(f"Author extracted: {author}")
                        return author

            logger.info("No author found")
            return "Unknown Author"

        except Exception as e:
            logger.error(f"Error extracting author: {str(e)}")
            return "Unknown Author"

    def extract_dates(self, text: str) -> List[str]:
        """
        Extract dates from the document text.

        This method finds various date formats in the text.

        Args:
            text (str): The document text

        Returns:
            List[str]: List of found dates
        """
        try:
            date_patterns = [
                r'\b\d{4}-\d{2}-\d{2}\b',  # YYYY-MM-DD
                r'\b\d{2}/\d{2}/\d{4}\b',  # MM/DD/YYYY
                r'\b\d{2}-\d{2}-\d{4}\b',  # MM-DD-YYYY
                r'\b\d{1,2}\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b',  # DD Month YYYY
                r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',  # Month DD, YYYY
            ]

            found_dates = []
            for pattern in date_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                found_dates.extend(matches)

            # Remove duplicates and limit to first 5 dates
            unique_dates = list(dict.fromkeys(found_dates))[:5]

            if unique_dates:
                logger.info(f"Dates extracted: {unique_dates}")
            else:
                logger.info("No dates found")

            return unique_dates

        except Exception as e:
            logger.error(f"Error extracting dates: {str(e)}")
            return []

    def extract_keywords(self, text: str, max_keywords: int = 10) -> List[str]:
        """
        Extract important keywords from the text.

        This method uses simple frequency analysis to find important terms.

        Args:
            text (str): The document text
            max_keywords (int): Maximum number of keywords to return

        Returns:
            List[str]: List of important keywords
        """
        try:
            # Clean the text
            text = text.lower()
            # Remove punctuation except spaces and periods
            text = re.sub(r'[^\w\s.]', ' ', text)

            # Split into words
            words = text.split()

            # Filter out stop words, very short words, and numbers
            filtered_words = []
            for word in words:
                if (len(word) > 3 and 
                    word not in self.stop_words and 
                    not word.isdigit() and
                    word.isalpha()):
                    filtered_words.append(word)

            # Count word frequencies
            word_counts = Counter(filtered_words)

            # Get the most common words
            common_words = word_counts.most_common(max_keywords)
            keywords = [word for word, count in common_words if count > 1]

            logger.info(f"Keywords extracted: {keywords}")
            return keywords

        except Exception as e:
            logger.error(f"Error extracting keywords: {str(e)}")
            return []

    def generate_summary(self, text: str, max_sentences: int = 3) -> str:
        """
        Generate a simple summary of the text.

        This method uses sentence scoring based on keyword frequency
        to select the most important sentences.

        Args:
            text (str): The document text
            max_sentences (int): Maximum number of sentences in summary

        Returns:
            str: Generated summary
        """
        try:
            # Split text into sentences
            sentences = re.split(r'[.!?]+', text)
            sentences = [s.strip() for s in sentences if len(s.strip()) > 20]

            if len(sentences) <= max_sentences:
                summary = '. '.join(sentences)
                logger.info("Summary generated (all sentences)")
                return summary + '.'

            # Get keywords for scoring
            keywords = self.extract_keywords(text, max_keywords=20)
            keyword_set = set(keywords)

            # Score sentences based on keyword presence
            sentence_scores = []
            for sentence in sentences:
                words = sentence.lower().split()
                score = sum(1 for word in words if word in keyword_set)
                sentence_scores.append((sentence, score))

            # Sort by score and get top sentences
            sentence_scores.sort(key=lambda x: x[1], reverse=True)
            top_sentences = [s[0] for s in sentence_scores[:max_sentences]]

            # Maintain original order
            summary_sentences = []
            for sentence in sentences:
                if sentence in top_sentences:
                    summary_sentences.append(sentence)
                if len(summary_sentences) >= max_sentences:
                    break

            summary = '. '.join(summary_sentences)
            logger.info("Summary generated using keyword scoring")
            return summary + '.'

        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
            # Fallback to first few sentences
            sentences = re.split(r'[.!?]+', text)
            sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
            if sentences:
                summary = '. '.join(sentences[:max_sentences])
                return summary + '.'
            return "Summary not available."

    def extract_metadata(self, text: str) -> Dict[str, Any]:
        """
        Extract all metadata from the text.

        Args:
            text (str): The document text

        Returns:
            Dict[str, Any]: Dictionary containing all extracted metadata
        """
        logger.info("Starting metadata extraction")

        metadata = {
            'title': self.extract_title(text),
            'author': self.extract_author(text),
            'dates': self.extract_dates(text),
            'keywords': self.extract_keywords(text),
            'summary': self.generate_summary(text),
            'word_count': len(text.split()),
            'character_count': len(text),
            'extraction_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        logger.info("Metadata extraction completed")
        return metadata

# Test the module if run directly
if __name__ == "__main__":
    extractor = MetadataExtractor()
    sample_text = """
    The Art of Programming
    By John Smith
    Published on March 15, 2024

    Programming is the process of creating computer software using programming languages. 
    It involves designing, writing, testing, and maintaining code. Good programming practices 
    include writing clean, readable code and proper documentation. Modern software development 
    relies heavily on collaboration and version control systems.
    """

    metadata = extractor.extract_metadata(sample_text)
    print("Sample metadata extraction:")
    for key, value in metadata.items():
        print(f"{key}: {value}")