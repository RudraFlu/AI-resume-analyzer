import streamlit as st
from job_matcher import JobMatcher
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
if(resume is not None):
    left,right = st.columns(2)
    with left:
        extractor = SkillExtractor()
        resume_data = extractor.extract(clean_text)
        skills_df = resume_data["skills"]
        llm_data = extractor.analyze_resume(resume_text)
        st.subheader("Current skills")
        st.dataframe(
                    skills_df,
                    use_container_width=True,
                    hide_index=True
                )
        st.subheader("Education")
        for edu in llm_data["Education"]:
            st.write(f"**Degree:** {edu['Degree']}")
            st.write(f"**Branch:** {edu['Branch']}")
            st.write(f"**Institution:** {edu['Institution']}")
            st.write(f"**Graduation Year:** {edu['Graduation Year']}")
        st.subheader("Projects")
        for project in llm_data["Projects"]:
            with st.container(border=True):
                st.write(project['Project Name'])
            st.write(project["Description"])
            if project["Technologies Mentioned"]:
                st.write("**Technologies:**")
                st.write(", ".join(project["Technologies Mentioned"]))
        st.subheader("Experience")
        if not llm_data["Experience"]:
            st.info("No experience found.")
        else:
            for exp in llm_data["Experience"]:
                st.markdown(f"### {exp['Role']}")
                st.write(exp["Company"])
                st.write(exp["Duration"])
                for r in exp["Responsibilities"]:
                    st.write(f"• {r}")
    with right:
        matcher = JobMatcher()
        selected_job=st.selectbox(
            "Select target role",
            matcher.jobs_df['job'].tolist()
        )
        st.write("Selected role: ", selected_job)
        skills_list = matcher.prepare_skills(skills_df)
        recommendations = matcher.recommendation(skills_list)
        top_roles = matcher.top_roles(recommendations)
        match_score = matcher.calc_score(recommendations,selected_job)
        res_skill = matcher.get_res_skills(resume_data['skills'])
        job_skill=matcher.get_job_skills(selected_job)
        found, missing = matcher.comp_skills(
            res_skill,job_skill
        )
        st.metric(
    label="Resume Match Score",
    value=f"{match_score}%"
)
        st.subheader("Skills found")
        for skill in sorted(found):
            st.write(f"""
                     -{skill}
                     """)
        st.subheader("Missing skills")
        for skill in sorted(missing):
                    st.write(f"""
                             -{skill}
                             """)
        st.subheader("Recommended Roles")
        st.dataframe(
        top_roles[
        ["job", "Match Score"]
    ],
        hide_index=True,
        use_container_width=True
)