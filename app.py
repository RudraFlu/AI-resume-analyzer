import streamlit as st
import pandas as pd
import os
from text_cleaner import TextCleaner
from resume_parser import ResumeParser
from skill_extractor import SkillExtractor
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)
left, centre, right = st.columns([1,2,1])
with centre:
    st.title("AI Resume Analyser")
    st.write("Upload your resume to get started")
    
resume=st.file_uploader(
        label="your resume goes here",
        type=["pdf","docx"],
        accept_multiple_files=False
    )
if resume is not None:
    parser = ResumeParser()
    
    resume_text = parser.extract(resume)
    
    cleaner = TextCleaner()
    clean_text = cleaner.clean(resume_text)
    st.success("Resume uploaded successfully!")

    col1, col2 = st.columns(2)

    with col1:
        st.write("Filename:\n", resume.name)

    with col2:
        st.write(
                "Size:\n",
                f"{resume.size / 1024:.2f} KB"
            )
left,right = st.columns(2)
with left:
    if(resume is not None):
            extractor = SkillExtractor()
            resume_data = extractor.extract(resume_text,clean_text)
            skills_df = resume_data["skills"]
            st.subheader("Current skills")
            st.dataframe(
                    skills_df,
                    use_container_width=True,
                    hide_index=True
                )

with right:
    if(resume is not None):
       
        edu_df = resume_data["education"]
        st.subheader("Education")
        st.code("\n".join(edu_df["section"]))
