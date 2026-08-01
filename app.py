import streamlit as st
import os

from resume_parser import ResumeParser
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)
left, centre, right = st.columns([1,2,1])
with centre:
    st.title("AI Resume Analyser")
    st.write("Upload your resume to get started")
    

left,right = st.columns(2)
with left:
    resume=st.file_uploader(
        label="your resume goes here",
        type=["pdf","docx"],
        accept_multiple_files=False
    )
if resume is not None:
    parser = ResumeParser()
    
    resume_text = parser.extract(resume)

    st.success("Resume uploaded successfully!")

    col1, col2 = st.columns(2)

    with col1:
        st.write("Filename:\n", resume.name)

    with col2:
        st.write(
            "Size:\n",
            f"{resume.size / 1024:.2f} KB"
        )
        
    st.subheader("Extracted Resume Text")

    st.text_area(
        "Resume",
        resume_text,
        height=400
    )