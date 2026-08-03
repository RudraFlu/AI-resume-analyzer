import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
class JobMatcher:
    def __init__(self,path = "data/job_roles.csv"):
        self.path = path
        self.jobs_df=self.load_jobs()
    def load_jobs(self):
        jobs = pd.read_csv(self.path)
        jobs['job'] = jobs['job'].str.strip()
        jobs['skills']=jobs['skills'].fillna("").str.strip()
        return jobs
    def prepare_skills(self, skills):
        skills = [
        skill.replace(" ", "_")
        for skill in skills["skill"]
    ]
        return " ".join(skills)
    def prepare_doc(self,skills_list):
        doc = [skills_list]
        doc.extend(
            self.jobs_df['skills'].tolist()
        )
        return doc
    def vectorize_doc(self,doc):
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform(doc)
        return vectors
    def get_job_doc(self, job):
        job = self.jobs_df[
            self.jobs_df['job'] == job
        ]
        if job.empty:
            return ""
        return job.iloc[0]["skills"]
    def normalize(skill):
        return skill.replace(" ", "_")
    def calc_similarity(self, vectors):
        res_vec=vectors[0]
        job_vec = vectors[1:]
        sim_score = cosine_similarity(
            res_vec,job_vec
        )[0]
        return sim_score
    def calc_custom_score(self,res_doc,jd_doc):
        doc =[
            res_doc,
            jd_doc
        ]
        vector = self.vectorize_doc(doc)
        score = cosine_similarity(
    vector[0],
    vector[1]
)[0][0]

        return round(score * 100, 2)
    def calc_score(self,recommendation,job):
        sim_score = recommendation.loc[
            recommendation["job"] == job,
            "Match Score"
        ]
        if sim_score.empty:
            return 0
        return sim_score.iloc[0]
    def get_job_skills(self, job):
        job = self.jobs_df[
            self.jobs_df["job"] == job
        ]
        if job.empty:
            return set()
        skills = job.iloc[0]['skills']
        return set(skills.split())
    def comp_skills(self,res,job):
        res = {skill.replace(" ", "_") for skill in res}
        job = {skill.replace(" ", "_") for skill in job}
        found = res & job
        missing = job - res
        found = {
        skill.replace("_", " ")
        for skill in found
}

        missing = {
        skill.replace("_", " ")
    for skill in missing
}
        return found, missing
    def recommendation(self,res_doc):
        doc = self.prepare_doc(res_doc)
        vectors = self.vectorize_doc(doc)
        scores = self.calc_similarity(vectors)
        recommendations = self.jobs_df.copy()
        recommendations["Match Score"] = (
        scores * 100
        ).round(2)
        return recommendations
    def top_roles(self,recommendations, n=3):
        return recommendations.sort_values(
        by="Match Score",
        ascending=False
    ).head(n)