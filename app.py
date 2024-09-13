import streamlit as st
import pytesseract
from PIL import Image
import spacy
from google.cloud import storage
import os
import io

# Load NLP model
nlp = spacy.load('en_core_web_sm')

# Set up Google Cloud credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'service-account-file.json'

def perform_ocr(file_bytes, file_type):
    # Handle different file types
    if file_type == 'pdf':
        # Convert PDF bytes to images
        from pdf2image import convert_from_bytes
        images = convert_from_bytes(file_bytes.read())
        text = ''
        for image in images:
            text += pytesseract.image_to_string(image)
    else:
        image = Image.open(file_bytes)
        text = pytesseract.image_to_string(image)
    return text

def extract_financial_entities(text):
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        entities.append((ent.text, ent.label_))
    return entities

def upload_to_gcs(bucket_name, file_bytes, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_file(file_bytes)
    print(f"File uploaded to {destination_blob_name}.")

def categorize_entities(entities):
    income_keywords = ['income', 'salary', 'wages', 'payment', 'pay', 'earnings']
    debt_keywords = ['debt', 'loan', 'credit', 'mortgage', 'bill', 'balance', 'due', 'owed']

    income_amounts = []
    debt_amounts = []

    for text, label in entities:
        if label == 'MONEY':
            lower_text = text.lower()
            if any(keyword in lower_text for keyword in income_keywords):
                amount = extract_amount(text)
                if amount:
                    income_amounts.append(amount)
            elif any(keyword in lower_text for keyword in debt_keywords):
                amount = extract_amount(text)
                if amount:
                    debt_amounts.append(amount)
            else:
                # Additional logic can be added here
                pass
    return income_amounts, debt_amounts

def extract_amount(text):
    # Simple function to extract numerical amount from text
    import re
    match = re.search(r'([\$£€]?[\d,]+\.?\d{0,2})', text.replace(',', ''))
    if match:
        amount_str = match.group(1).replace('$', '').replace('€', '').replace('£', '')
        try:
            amount = float(amount_str)
            return amount
        except ValueError:
            return None
    return None

def calculate_total_income(income_amounts):
    return sum(income_amounts)

def calculate_total_debt(debt_amounts):
    return sum(debt_amounts)

def main():
    st.title("MR TICKLES: Client Debt To Income Chart Application")

    st.write("""
        **MR TICKLES** (**M**ulti-source **R**eporting for **T**otal **I**ncome and **C**redit **K**nowledge via **L**oan **E**ligibility **S**ystem) is a document scanning and ingestion tool designed to assist underwriters in determining loan eligibility.
    """)

    # Initialize session state variables to store uploaded file names
    if 'uploaded_primary_files' not in st.session_state:
        st.session_state['uploaded_primary_files'] = []
    if 'uploaded_cosigner_files' not in st.session_state:
        st.session_state['uploaded_cosigner_files'] = []

    # File uploader for primary applicant
    st.header("Primary Applicant Documents")
    uploaded_files_primary = st.file_uploader(
        "Upload Documents for Primary Applicant",
        accept_multiple_files=True,
        type=['png', 'jpg', 'jpeg', 'pdf'],
        key='primary'
    )

    # Display uploaded primary applicant documents
    if uploaded_files_primary:
        st.session_state['uploaded_primary_files'] = [file.name for file in uploaded_files_primary]
        st.write("Uploaded Primary Applicant Documents:")
        for file_name in st.session_state['uploaded_primary_files']:
            st.write(f"- {file_name}")

    # File uploader for co-signer/spouse
    st.header("Co-signer/Spouse Documents")
    uploaded_files_cosigner = st.file_uploader(
        "Upload Documents for Co-signer/Spouse",
        accept_multiple_files=True,
        type=['png', 'jpg', 'jpeg', 'pdf'],
        key='cosigner'
    )

    # Display uploaded co-signer/spouse documents
    if uploaded_files_cosigner:
        st.session_state['uploaded_cosigner_files'] = [file.name for file in uploaded_files_cosigner]
        st.write("Uploaded Co-signer/Spouse Documents:")
        for file_name in st.session_state['uploaded_cosigner_files']:
            st.write(f"- {file_name}")

    bucket_name = 'your-bucket-name'  # Replace with your bucket name

    total_income = 0
    total_debt = 0

    process_documents = st.button("Process Documents")

    if process_documents:
        # Process files for primary applicant
        if uploaded_files_primary:
            st.subheader("Processing Primary Applicant Documents")
            for uploaded_file in uploaded_files_primary:
                file_type = uploaded_file.type.split('/')[-1].lower()
                if file_type == 'jpeg':
                    file_type = 'jpg'  # Handle 'jpeg' as 'jpg'
                file_bytes = io.BytesIO(uploaded_file.getbuffer())
                # Perform OCR
                text = perform_ocr(file_bytes, file_type)
                # Extract Entities
                entities = extract_financial_entities(text)
                # Upload to GCS
                file_bytes.seek(0)  # Reset the file pointer
                upload_to_gcs(bucket_name, file_bytes, f"primary/{uploaded_file.name}")
                # Categorize and calculate amounts
                income_amounts, debt_amounts = categorize_entities(entities)
                total_income += calculate_total_income(income_amounts)
                total_debt += calculate_total_debt(debt_amounts)
                # Display Extracted Information
                st.write(f"**{uploaded_file.name}**")
                st.write("Extracted Entities:")
                st.write(entities)
                st.write(f"Income Amounts: {income_amounts}")
                st.write(f"Debt Amounts: {debt_amounts}")

        # Process files for co-signer/spouse
        if uploaded_files_cosigner:
            st.subheader("Processing Co-signer/Spouse Documents")
            for uploaded_file in uploaded_files_cosigner:
                file_type = uploaded_file.type.split('/')[-1].lower()
                if file_type == 'jpeg':
                    file_type = 'jpg'  # Handle 'jpeg' as 'jpg'
                file_bytes = io.BytesIO(uploaded_file.getbuffer())
                # Perform OCR
                text = perform_ocr(file_bytes, file_type)
                # Extract Entities
                entities = extract_financial_entities(text)
                # Upload to GCS
                file_bytes.seek(0)  # Reset the file pointer
                upload_to_gcs(bucket_name, file_bytes, f"cosigner/{uploaded_file.name}")
                # Categorize and calculate amounts
                income_amounts, debt_amounts = categorize_entities(entities)
                total_income += calculate_total_income(income_amounts)
                total_debt += calculate_total_debt(debt_amounts)
                # Display Extracted Information
                st.write(f"**{uploaded_file.name}**")
                st.write("Extracted Entities:")
                st.write(entities)
                st.write(f"Income Amounts: {income_amounts}")
                st.write(f"Debt Amounts: {debt_amounts}")

        # Display Summary
        if (uploaded_files_primary or uploaded_files_cosigner):
            st.header("Summary")
            st.metric("Total Income", f"${total_income:,.2f}")
            st.metric("Total Debt", f"${total_debt:,.2f}")
            if total_income > 0:
                debt_to_income_ratio = (total_debt / total_income) * 100
                st.metric("Debt-to-Income Ratio", f"{debt_to_income_ratio:.2f}%")
            else:
                st.write("Total income is zero or undefined, cannot calculate Debt-to-Income Ratio.")

if __name__ == "__main__":
    main()
