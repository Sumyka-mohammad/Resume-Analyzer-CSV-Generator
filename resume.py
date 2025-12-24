import os
import zipfile
import tempfile
from typing import List, Optional

import streamlit as st
import pandas as pd
import pdfplumber
from docx import Document
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

load_dotenv()

class ResumeSchema(BaseModel):
    name: str = Field(description="Full name of the candidate")
    email: str = Field(description="Email address")
    phone: Optional[str] = Field(default=None)
    linkedin: Optional[str] = Field(default=None)
    github: Optional[str] = Field(default=None)
    years_of_experience: Optional[float] = Field(default=None)
    skills: List[str] = Field(description="List of technical skills")
    current_role: Optional[str] = Field(default=None)
    summary: str = Field(description="Professional summary")

parser = PydanticOutputParser(pydantic_object=ResumeSchema)

prompt = PromptTemplate(
    template="""
You are an expert HR resume analyzer.

Extract structured candidate information from the resume text below.

{format_instructions}

Resume Text:
{text}
""",
    input_variables=["text"],
    partial_variables={
        "format_instructions": parser.get_format_instructions()
    }
)

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

chain = prompt | llm | parser

def extract_pdf_text(file_path: str) -> str:
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


def extract_docx_text(file_path: str) -> str:
    doc = Document(file_path)
    return "\n".join(p.text for p in doc.paragraphs)

def process_zip(zip_file) -> List[dict]:
    results = []

    with tempfile.TemporaryDirectory() as tmpdir:
        with zipfile.ZipFile(zip_file, "r") as zip_ref:
            zip_ref.extractall(tmpdir)

        for root, _, files in os.walk(tmpdir):
            for file in files:
                path = os.path.join(root, file)

                if file.lower().endswith(".pdf"):
                    text = extract_pdf_text(path)
                elif file.lower().endswith(".docx"):
                    text = extract_docx_text(path)
                else:
                    continue

                if len(text.strip()) < 100:
                    continue

                try:
                    parsed = chain.invoke({"text": text})
                    results.append(parsed.model_dump())
                except Exception as e:
                    print(f"Failed to parse {file}: {e}")

    return results

st.set_page_config(
    page_title="AI Resume Analyzer",
    layout="wide"
)

st.title("📄 AI-Powered Resume Analyzer & CSV Generator")

st.markdown(
    """
Upload a **ZIP file containing resumes (PDF or DOCX)**.
The app will extract structured candidate data using AI
and allow you to download a CSV.
"""
)

uploaded_zip = st.file_uploader(
    "Upload ZIP of resumes",
    type=["zip"]
)

if uploaded_zip:
    with st.spinner("Analyzing resumes..."):
        resume_data = process_zip(uploaded_zip)

    if resume_data:
        df = pd.DataFrame(resume_data)

        st.success(f"Processed {len(df)} resumes")
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="⬇️ Download CSV",
            data=csv,
            file_name="resume_analysis.csv",
            mime="text/csv"
        )
    else:
        st.error("No valid resumes found in the ZIP file.")
