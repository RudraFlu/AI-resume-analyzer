# AI Resume Analyzer

An AI-powered Resume Analyzer that extracts information from resumes, compares them against job requirements, identifies skill gaps, recommends suitable job roles, and generates personalized learning roadmaps and resume feedback using Google's Gemini LLM.

---

## Features

### Resume Parsing
- Supports PDF resumes
- Extracts raw text from resumes
- Handles multiple resume formats

### Skill Extraction
- Rule-based NLP skill extraction
- Dictionary-based matching
- Categorizes technical skills
- Easily extendable skill dictionary

### Education Extraction
- Extracts:
  - Degree
  - Branch
  - Institution
  - Graduation Year
  - CGPA (if available)

### AI-powered Information Extraction
Using Google Gemini:
- Project Extraction
- Experience Extraction
- Education Validation

The prompts are controlled to minimize hallucinations by extracting only explicitly mentioned information.

### Job Matching
- TF-IDF Vectorization
- Cosine Similarity
- Resume Match Score
- Role-based comparison

### Skill Gap Analysis
- Skills already present
- Missing skills
- Comparison with target job

### Recommended Roles
Ranks the top matching job roles based on similarity score.

### AI Learning Roadmap
Generates a personalized 4-week roadmap based on:
- Target Role
- Existing Skills
- Missing Skills

### AI Resume Review
Provides:
- Resume Strengths
- Areas of Improvement
- ATS Optimization Tips
- Overall Recommendation

### Report Generation
Exports a complete Resume Analysis Report in PDF format.

---

# Tech Stack

## Programming Language
- Python

## Frontend
- Streamlit

## Backend
- Python

## NLP
- Regular Expressions
- Rule-Based Information Extraction
- TF-IDF
- Cosine Similarity

## AI
- Google Gemini API

## Machine Learning
- Scikit-Learn

## PDF Processing
- PyMuPDF (fitz)

## Report Generation
- ReportLab

## Containerization
- Docker

---

# Project Architecture

```text
                    Resume (PDF)
                          │
                          ▼
                 Resume Text Extractor
                          │
                          ▼
                 Text Preprocessing
                          │
        ┌─────────────────┴─────────────────┐
        │                                   │
        ▼                                   ▼
  Rule-Based NLP                     Gemini LLM
        │                                   │
        │                                   ├── Education Extraction
        │                                   ├── Project Extraction
        │                                   └── Experience Extraction
        │
        ▼
   Skill Dictionary
        │
        ▼
   Skill Extraction
        │
        ├───────────────┐
        │               │
        ▼               ▼
 Resume Skills     Custom Job Description
        │               │
        │         Skill Extraction
        │               │
        └───────┬───────┘
                │
                ▼
        Job Matching Engine
      (TF-IDF + Cosine Similarity)
                │
      ┌─────────┴─────────┐
      │                   │
      ▼                   ▼
Role Recommendation   Skill Gap Analysis
      │                   │
      └─────────┬─────────┘
                │
                ▼
      Gemini Roadmap Generator
                │
                ▼
      Gemini Resume Reviewer
                │
                ▼
        PDF Report Generator
                │
                ▼
           Streamlit Interface
```
---

# Folder Structure

```
AI-resume-analyzer/
│
├── app.py
├── resume_parser.py
├── skill_extractor.py
├── job_matcher.py
├── roadmap_generator.py
├── resume_reviewer.py
├── report_generator.py
│
├── data/
│   ├── jobs.csv
│   └── skill_dictionary.csv
│
├── sample_resumes/
│   ├── nlp_engineer.pdf
│   ├── data_analyst.pdf
│   └── ml_engineer.pdf
├── Dockerfile
├── requirements.txt
├── test_cases.csv
└── README.md
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/AI-resume-analyzer.git

cd AI-resume-analyzer
```

---

## Create Virtual Environment

Windows

```bash
python -m venv venv

venv\Scripts\activate
```

Linux/Mac

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file.

```
GOOGLE_API_KEY=YOUR_API_KEY
```

---

## Run Application

```bash
streamlit run app.py
```

---

# Docker

## Build Image

```bash
docker build -t ai-resume-analyzer .
```

## Run Container

```bash
docker run -p 8501:8501 --env-file .env ai-resume-analyzer
```

Open

```
http://localhost:8501
```

---

# Usage

1. Upload a Resume
2. Select a Target Job Role
3. Click Analyze
4. View
   - Extracted Skills
   - Match Score
   - Skill Gap
   - Recommended Roles
   - Education
   - Projects
   - Experience
   - AI Roadmap
   - AI Resume Feedback
5. Download PDF Report

---

# NLP Techniques Used

## Rule-Based NLP
- Text Cleaning
- Regular Expressions
- Section Detection
- Skill Dictionary Matching
- Information Extraction

## Statistical NLP
- TF-IDF Vectorization
- Cosine Similarity

## Generative AI
- Education Extraction
- Project Extraction
- Experience Extraction
- Resume Feedback
- Learning Roadmap Generation

---

# Sample Output

### Resume Match Score

```
Target Role:
Machine Learning Engineer

Resume Match Score:
74%
```

### Skills Found

```
Python
Pandas
NumPy
SQL
Scikit-learn
```

### Missing Skills

```
Docker
FastAPI
MLflow
Cloud Deployment
```

### Recommended Roles

```
Data Analyst
Machine Learning Engineer
Python Developer
```

### AI Roadmap

```
Week 1
Learn FastAPI

Week 2
Deploy an ML Model

Week 3
Docker Fundamentals

Week 4
MLflow & Cloud Deployment
```

---

# Future Improvements

- Support DOCX resumes
- OCR for scanned resumes
- ATS Score Prediction
- Resume Ranking
- Cover Letter Generation
- Multi-language Resume Support
- Resume History
- Cloud Deployment

---

# Screenshots

Add screenshots here.

- Home Page
- Resume Upload
- Skill Extraction
- Job Matching
- Roadmap
- Resume Feedback
- PDF Report

---

# Dependencies

- Streamlit
- Scikit-Learn
- Pandas
- PyMuPDF
- Google GenAI
- ReportLab
- python-dotenv

---

# License

This project is developed for educational purposes.

---

# Authors

Developed by **Rudra Kumar Singh**

---

# Acknowledgements

- Google Gemini API
- Streamlit
- Scikit-Learn
- ReportLab
- PyMuPDF