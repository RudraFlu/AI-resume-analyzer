import re

import pandas as pd


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
    def extract_education(self, text):
        education_lines = self.get_section(
            text,
            start_headers=["education"],
            stop_headers=[
            h for h in self.SECTION_HEADERS
            if h != "education"])

        return {
                "section":education_lines,
                }

    def extract_projects(self, text):
        ...

    def extract_experience(self, text):
        ...

    def extract(self, raw_text,clean_text):
        return {
            "skills": self.extract_skills(clean_text),
            "education": self.extract_education(raw_text),
            "projects": self.extract_projects(raw_text),
            "experience": self.extract_experience(raw_text)
        }