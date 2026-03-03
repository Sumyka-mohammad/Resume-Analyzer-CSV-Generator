# 🤖AI Resume Analyzer & CSV Generator
An AI-powered Resume Analyzer built using Streamlit + LangChain + OpenAI that processes multiple resumes (PDF/DOCX) from a ZIP file, extracts structured candidate data, and generates a downloadable CSV file.

# 🚀 Project Overview
Recruiters and HR teams often receive resumes in bulk—commonly as ZIP files containing PDFs and DOCX documents. Manually reviewing and extracting information from each resume is time-consuming, inconsistent, and error-prone.
This project solves that problem by using Large Language Models (LLMs) to automatically analyze resumes and generate a clean, structured CSV that can be easily filtered, searched, and analyzed.

## ✨ Features
- 📂 Upload ZIP file of resumes
- 📄 Supports PDF and DOCX formats
- 🧠 AI-powered structured data extraction
- 📊 Converts resumes into structured tabular format
- ⬇️ Download results as CSV
- ⚡ Clean Streamlit UI
- 🔒 Deterministic extraction (temperature=0)

## 🧠 Extracted Resume Information
- Each resume is converted into structured fields such as:
- Professional Summary
- Total Experience (text-based)
- Skills (list format)
- Links (LinkedIn, GitHub, Portfolio)

## 🏗️ System Architecture
 . ZIP File (PDF / DOCX)
        ↓
 . File Extraction
        ↓
 . Text Extraction (PDF & DOCX)
        ↓
 . Gemini + LangChain
        ↓
 . Structured Resume Data
        ↓
  . CSV Generation
        ↓
 . Download via Streamlit

## 🛠 Tech Stack
- Frontend: Streamlit
- LLM Framework: LangChain
- Model: OpenAI (gpt-4o-mini)
- Parsing: Pydantic Output Parser
- File Processing: pdfplumber, python-docx
- Data Handling: pandas
- Environment Management: python-dotenv

## 🚀 How to Run Locally
- pip install -r requirements.txt
# 1 Set up environment variables:
- Create a .env file:
- GOOGLE_API_KEY=your_gemini_api_key
# 2 Run the application
- streamlit run app.py

## 💼 Use Cases
- HR resume screening automation
- Bulk resume parsing
- Candidate data standardization
- Resume analytics & filtering
- ATS-style preprocessing
