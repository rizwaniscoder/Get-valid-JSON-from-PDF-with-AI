import streamlit as st
import pdfplumber
import os
from openai import OpenAI
from json import JSONDecodeError

def extract_text_from_pdf(file):
    """
    Function to extract text from a PDF.
    Now handles files that can't be opened.
    """
    extracted_text = ""
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or " "
                extracted_text += page_text
    except Exception as e:
        st.error(f"Failed to read the PDF. Error details: {str(e)}")
        return None
    return extracted_text

def generate_ai_response(input_text, api_key):
    """
    Function to interact with OpenAI API and get a response.
    Handles exceptions for a smoother user experience.
    """
    try:
        client = OpenAI(api_key=api_key)
        input_messages = [
            {"role": "system", "content": "Please output a valid JSON"},
            {"role": "user", "content": input_text},
        ]
        response_from_ai, *_ = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=input_messages,
            response_format={"type": "json_object"}
        ).choices
        if response_from_ai:
            return response_from_ai.message.content
        else:
            return {"error": "No response from AI."}
    except Exception as e:
        st.error(f"Failed to get an AI response. Error details: {str(e)}")
        return {"error": "Failed to get an AI response."}

def main():
    """
    Main function to control the flow
    """
    st.title('Get valid JSON from PDF with AI')

    api_key = st.text_input("Enter your OpenAI API key:", type="password")


    # Upload a PDF file
    pdf_file = st.file_uploader("Please upload a PDF file", type=['pdf'])

    # A button to start the analysis
    if st.button("Start Analysis"):
        if pdf_file is not None:
            with st.spinner("Analyzing the content in the PDF..."):
                extracted_text = extract_text_from_pdf(pdf_file)
                if extracted_text:
                    ai_response = generate_ai_response(extracted_text, api_key)
                    if ai_response:
                        try:
                            st.json(ai_response)
                            # Download JSON response
                            st.download_button(
                                label="Download JSON response",
                                data=ai_response,
                                file_name='ai_response.json',
                                key='download_json'
                            )
                        except JSONDecodeError as e:
                            st.error(f"Failed to convert AI response to JSON. Error details: {str(e)}")
                else:
                    st.warning("No readable text found in the uploaded PDF. Consider uploading a different file.")
        else:
            st.warning("No file uploaded. Please upload a PDF file.")

if __name__ == '__main__':
    main()
