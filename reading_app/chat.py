import google.generativeai as genai
from typing import Optional
import os
from pathlib import Path
from dotenv import load_dotenv
import PyPDF2
from typing import Dict, List, Tuple

# Load environment variables from .env file
load_dotenv()

class ChatAssistant:
    def __init__(self):
        """Initialize the chat assistant with Gemini configuration."""
        # Get API key from environment variable
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set")
        # Configure Gemini
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')
        self.chat = None
        
        # Store document context
        self.current_document_text: Optional[str] = None
        self.current_document_path: Optional[str] = None

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text content from a PDF file.
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            str: Extracted text content
        """
        print(f"Attempting to extract text from PDF: {pdf_path}")
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = []
                for page in reader.pages:
                    text.append(page.extract_text())
                extracted_text = '\n'.join(text)
                print(f"Successfully extracted {len(extracted_text)} characters from PDF")
                return extracted_text
        except Exception as e:
            print(f"Error extracting text from PDF: {str(e)}")
            raise  # Re-raise the exception to handle it in the calling function

    def compose_prompt(self, user_message: str) -> str:
        """
        Compose a structured prompt combining document context and user query.
        
        Args:
            user_message (str): The user's question or request
            
        Returns:
            str: Structured prompt for the model
        """
        if not self.current_document_text:
            print("No document context available, using raw message")
            return user_message
            
        print(f"Composing prompt with document context ({len(self.current_document_text)} chars) and user message")
        prompt = f"""You are a helpful reading assistant analyzing a document. 
Below is the document content, followed by a user's question. 
Please provide a clear, accurate, and helpful response based on the document content.

DOCUMENT CONTENT:
{self.current_document_text}

USER QUESTION:
{user_message}

Please answer based on the document content above. If the question cannot be answered using only the document content, 
please say so clearly. If you need to quote from the document, use quotation marks and be precise."""

        return prompt

    def start_chat(self) -> None:
        """Start a new chat session."""
        print("Starting new chat session")
        self.chat = self.model.start_chat(history=[])
        
    def load_document(self, document_path: str) -> bool:
        """
        Load and store document content for the session.
        
        Args:
            document_path (str): Path to the document
            
        Returns:
            bool: True if document was loaded successfully
        """
        print(f"Loading document from path: {document_path}")
        try:
            if document_path != self.current_document_path:
                print("New document path detected, extracting text")
                self.current_document_text = self.extract_text_from_pdf(document_path)
                self.current_document_path = document_path
                return bool(self.current_document_text)
            print("Document already loaded")
            return True
        except Exception as e:
            print(f"Error loading document: {str(e)}")
            raise  # Re-raise the exception to handle it in the calling function

    def process_message(self, message: str, document_path: Optional[str] = None) -> str:
        """
        Process a user message and return the AI response.
        
        Args:
            message (str): The user's message
            document_path (Optional[str]): Path to the PDF document being discussed
            
        Returns:
            str: The AI's response
        """
        print(f"\nProcessing message: {message}")
        print(f"Document path: {document_path}")
        
        try:
            if not self.chat:
                self.start_chat()

            # Load document if provided and different from current
            if document_path:
                if not self.load_document(document_path):
                    return "I apologize, but I couldn't read the document. Please make sure it's a valid PDF file."

            # Compose the prompt with document context and user message
            structured_prompt = self.compose_prompt(message)
            print("Sending prompt to Gemini")

            # Get response from the model
            response = self.chat.send_message(structured_prompt)
            print("Received response from Gemini")
            return response.text

        except Exception as e:
            print(f"Error in chat processing: {str(e)}")
            raise  # Re-raise to be handled by the view

# Create a singleton instance
print("Creating ChatAssistant singleton instance")
assistant = ChatAssistant() 