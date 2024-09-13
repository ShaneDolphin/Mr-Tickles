# MR TICKLES
### Multi-source Reporting for Total Income and Credit Knowledge via Loan Eligibility System

**Overview**
MR TICKLES is a document scanning and ingestion application designed to assist underwriters in determining loan eligibility. It processes various financial documents—such as bank statements, utility bills, W2 statements, paycheck stubs, and more—by extracting essential information using OCR (Optical Character Recognition) and NLP (Natural Language Processing) techniques. The application then presents a consolidated view of a client's debts and incomes, including data from co-signers or spouses.

##### Features
- Multi-format Document Upload: Supports uploading multiple PDFs and images (PNG, JPG, JPEG) for both primary applicants and co-signers/spouses.
- OCR Processing: Extracts text from scanned documents using Tesseract OCR.
- NLP Analysis: Utilizes spaCy to extract key financial entities like names, organizations, monetary amounts, dates, and locations.
- Data Categorization: Categorizes extracted monetary amounts into debts or incomes based on contextual keywords.
- Cloud Storage: Stores original documents securely in Google Cloud Storage.
- Data Visualization: Displays a comprehensive debt-to-income chart, including total debt, total income, and debt-to-income ratio.
- User Interface: Provides an intuitive Streamlit interface with real-time feedback on uploaded documents.
- Containerization: Easily deployable using Docker and Docker Compose.

##### Technology Stack
- Programming Language: Python 3.8+
- Web Framework: Streamlit
- OCR Tool: Tesseract OCR with Pytesseract
- NLP Library: spaCy
- Cloud Storage: Google Cloud Storage
- Containerization: Docker and Docker Compose

#####Prerequisites
- Docker and Docker Compose installed on your machine.
- A Google Cloud account with a service account key JSON file.
- Python 3.8+ (if running without Docker).
- Git (to clone the repository).

## Installation
**1. Clone the Repository**
```bash
git clone https://github.com/yourusername/mr-tickles.git
cd mr-tickles
```
**2. Set Up Google Cloud Credentials**
1. Create a Service Account: In the Google Cloud Console, create a service account with the necessary permissions for Google Cloud Storage.
2. Download the Key File: Download the JSON key file and place it in the project root directory.
3. Rename the Key File: Rename the file to `service-account-file.json` or update the Docker environment variable accordingly.

#### SERIOUSLY READ THIS DAMNIT: Never commit your service-account-file.json to a public repository. Add it to your .gitignore file.

**3. Update Environment Variables**
In the `docker-compose.yml` file, update the `GOOGLE_APPLICATION_CREDENTIALS` environment variable path if necessary.

**4. Update Google Cloud Storage Bucket Name**
In the `app.py` file, replace `'your-bucket-name' `with the name of your actual Google Cloud Storage bucket.

```python
bucket_name = 'your-bucket-name'  # Replace with your bucket name

```
**5. Build and Run with Docker Compose**
```bash
# Build the Docker image
docker-compose build

# Run the Docker container
docker-compose up -d
```
**6. Access the Application**
Navigate to `http://localhost:8501` in your web browser to access the Streamlit application.


------------

## Usage

1. Upload Documents:
- Primary Applicant: Use the "Upload Documents for Primary Applicant" section to upload multiple financial documents.
- Co-signer/Spouse: Use the "Upload Documents for Co-signer/Spouse" section to upload documents for the co-applicant.

2. Verify the Documents:
- The application will display the names of the uploaded files to confirm successful uploads.

3. Process Documents:
- Click the "Process Documents" button to start OCR and NLP processing.
- The application will extract text from the documents, analyze financial entities, and categorize monetary amounts.

4. View Extracted Data:
- For each document, the extracted entities, income amounts, and debt amounts will be displayed.

5. Review Summary Metrics:
- The "Summary" section will show the total income, total debt, and the calculated debt-to-income ratio.

## Directory Structure
```bash
mr-tickles/
├── app.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── service-account-file.json    # (Not included in the repository)
├── README.md
├── .gitignore
└── (additional modules and files)
```

