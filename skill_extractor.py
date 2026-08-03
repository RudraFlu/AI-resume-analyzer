import re
import os
import json
import pandas as pd
from google import genai
from dotenv import load_dotenv
class SkillExtractor:
    SECTION_HEADERS = [
    "contribution",
    "education",
    "experience",
    "work experience",
    "projects",
    "skills",
    "technical skills",
    "certifications",
    "achievements",
    "internships",
    "positions of responsibility"
]
    DEGREES = [
    "Bachelor of Technology",
    "B.Tech",
    "Bachelor of Engineering",
    "B.E.",
    "Master of Technology",
    "M.Tech",
    "Bachelor of Science",
    "B.Sc",
    "Master of Science",
    "M.Sc",
    "Bachelor of Computer Applications",
    "BCA",
    "Master of Computer Applications",
    "MCA",
    "Diploma"
]
    COLLEGE_KEYWORDS = [
    "university",
    "college",
    "institute",
    "school",
    "academy"
]
    BRANCHES = [
    "Computer Science and Engineering",
    "Computer Science",
    "Information Technology",
    "Artificial Intelligence",
    "Artificial Intelligence and Machine Learning",
    "Machine Learning",
    "Data Science",
    "Electronics and Communication Engineering",
    "Electronics Engineering",
    "Electrical Engineering",
    "Mechanical Engineering",
    "Civil Engineering",
    "Chemical Engineering",
    "Biotechnology",
    "Mathematics",
    "Physics",
    "Commerce",
    "Business Administration"
]
    def __init__(self, path="data/skill_dictionary.csv"):
        self.path = path
        self.skillDf = None
        
        self.patterns = None

        self.load_dictionary()

        self.expand_aliases()

        self.sort_dictionary()

        self.build_patterns()
        load_dotenv()
        self.client = genai.Client(
            api_key=os.getenv("GEMINI_API")
        )
        self.model = "gemini-3.1-flash-lite"
    def analyze_resume(self,text):
        prompt = f"""
            You are an AI resume analyzer.
            Analyze the resume below.
            Extract the following information:
            1. Education
               - Degree
               - Branch
               - Institution
               - Graduation Year
            2. Projects
               - Project Name
               - Description
               - Technologies Mentioned
            3. Experience
               - Company
               - Role
               - Duration
               - Responsibilities
            summarize the project description
            Extract ONLY information that is explicitly present in the resume.
            Do NOT infer technologies, programming languages, frameworks, dates, companies, or responsibilities.
            If a piece of information is not explicitly mentioned, return an empty string or an empty list.
            Preserve original wording as much as possible.
            Return ONLY valid JSON.
            Do not use markdown.
            Do not write explanations.
            Never guess.
            Never hallucinate.
            Never complete missing information.
            Do not wrap the JSON in ```.
            Resume:
            {text}
            """
        response = self.client.models.generate_content(
            model = self.model,
            contents=prompt)
        return json.loads(response.text)
    def review_resume(
        self,
        resume_text,
        target_role,
        match_score,
        found_skills,
        missing_skills
    ):
        prompt = f"""
        You are an experienced technical recruiter and ATS resume reviewer.
        Review the following resume for the target role.
        Target Role:
        {target_role}
        Current Match Score:
        {match_score}%
        Skills Found:
        {", ".join(sorted(found_skills))}
        Missing Skills:
        {", ".join(sorted(missing_skills))}
        Resume:
        {resume_text}
        Instructions:
        Provide feedback under EXACTLY these headings:
        ## Resume Strengths
        ## Areas to Improve
        ## ATS Optimization Tips
        ## Overall Recommendation

        Rules:
        - Be constructive and specific.
        - Do not invent experiences or skills.
        - Base comments only on the resume.
        - Mention missing skills only if they are relevant to the target role.
        - Keep the response concise.
        - Return Markdown only.
        """
        try:
            response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )
        except Exception as e:
            print(e)
        return response.text
            
    def load_dictionary(self):

        self.skill_df = pd.read_csv(self.path)

        self.skill_df["skill"] = self.skill_df["skill"].str.strip()

        self.skill_df["aliases"] = (
        self.skill_df["aliases"]
        .fillna("")
        .str.strip()
    )

        self.skill_df["category"] = (
        self.skill_df["category"]
        .str.strip()
    )
    def expand_aliases(self):
        expanded = []
        for _, row in self.skill_df.iterrows():
            expanded.append({
            "surface": row["skill"],

            "canonical": row["skill"],

            "category": row["category"]
        })
            aliases = row["aliases"]
            if aliases:
                for alias in aliases.split(","):

                    alias = alias.strip()

                    if alias:

                        expanded.append({

                        "surface": alias,

                        "canonical": row["skill"],

                        "category": row["category"]

                    })

        self.skill_df = pd.DataFrame(expanded)
    def sort_dictionary(self):
        self.skill_df = self.skill_df.sort_values(
        by="surface",
        key=lambda col: col.str.len(),
        ascending=False
    ).reset_index(drop=True)
    def build_patterns(self):
        self.patterns = []
        for _, row in self.skill_df.iterrows():
            escaped = re.escape(row["surface"])
            regex = re.compile(
            r"(?<![A-Za-z0-9_])"
            + escaped +
            r"(?![A-Za-z0-9_])",
            re.IGNORECASE
        )
            self.patterns.append({
            "surface": row["surface"],
            "canonical": row["canonical"],
            "category": row["category"],
            "regex": regex
        })
    def extract_skills(self, text):
        matched =[]
        detected =[]
        seen = set()
        
        for entry in self.patterns:
            match = entry["regex"].search(text)
            if not match:
                continue
            span=(match.start(),match.end())
            if self._overlaps(span,matched):
                continue
            matched.append(span)
            seen.add(entry["canonical"])

            detected.append({
            "skill": entry["canonical"],
            "category": entry["category"],
        })

        return pd.DataFrame(detected)
    @staticmethod
    def _overlaps(current_span, matched_spans):

        start, end = current_span

        for s, e in matched_spans:

            if start < e and s < end:
                return True

        return False

    def get_section(self,text,start_headers,stop_headers):
        lines = text.splitlines()
        collecting = False
        section = []
        start_headers = [h.lower() for h in start_headers]
        stop_headers = [h.lower() for h in stop_headers]
        for line in lines:
            current = line.strip().lower()
            if not collecting:
                if current in start_headers:
                    collecting = True
                continue
            if current in stop_headers:
                break
            if line.strip():
                section.append(line.strip())
        return section
    
    def extract(self, clean_text):
        return {
            "skills": self.extract_skills(clean_text),
        }