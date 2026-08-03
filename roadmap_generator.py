import os
from dotenv import load_dotenv
from google import genai

class RoadmapGenerator:
    def __init__(self):
        load_dotenv()
        self.client = genai.Client(
        api_key=os.getenv("GEMINI_API")
                )
        self.model = "gemini-3.1-flash-lite"
    def generate_roadmap(
        self,
        target_role,
        curr_skills,
        miss_skills
    ):
        prompt = f"""
        You are an expert career mentor.
        A student's resume has been analyzed.
        Target Role:
        {target_role}

        Current Skills:
        {", ".join(sorted(curr_skills))}
        Missing Skills:
        {", ".join(sorted(miss_skills))}
        Create a practical 4-week learning roadmap.
        Rules:
        - Focus primarily on the missing skills.
        - Give achievable weekly goals.
        - Include one small hands-on project or exercise each week.
        - Do not recommend paid resources.
        - Keep each week concise (3-5 bullet points).
        - Return ONLY Markdown.
        Format exactly like:
        ## Week 1
        - ...
        - ...
        ## Week 2
        - ...
        - ...
        ## Week 3
        - ...
        - ...
        ## Week 4
        - ...
        - ...
        """
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt)
        return response.text