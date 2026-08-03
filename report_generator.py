from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet


class ReportGenerator:

    def generate(self, analysis, filename="resume_report.pdf"):
        doc = SimpleDocTemplate(filename)
        styles = getSampleStyleSheet()
        story = []
        
        title = Paragraph(
            "AI Resume Analysis Report",
            styles["Title"]
        )
        story.append(title)
        story.append(Spacer(1,20))
        story.append(
            Paragraph(
                f"<b>Target Role:</b> {analysis['target_role']}",
                styles["Normal"]
            )
        )
        story.append(Spacer(1,10))
        story.append(
    Paragraph(
        f"<b>Resume Match Score:</b> {analysis['match_score']}%",
        styles["Heading2"]
    )
)
        story.append(Spacer(1, 15))
        self.add_skills(
            story,
            styles,
            analysis
)
        self.add_recommendations(
            story,
            styles,
            analysis
        )
        self.add_education(
            story,
            styles,
            analysis
        )
        self.add_projects(
            story,
            styles,
            analysis
        )
        self.add_experience(
            story,
            styles,
            analysis
)
        self.add_roadmap(
            story,
            styles,
            analysis
)
        self.add_feedback(
            story,
            styles,
            analysis
)
        doc.build(story)
        return filename
    def add_skills(self, story, styles, analysis):
            story.append(
                Paragraph(
                    "Skills Found",
                    styles["Heading2"]
        )
    )
            for skill in analysis["skills_found"]:
                story.append(
                    Paragraph(
                        f"• {skill}",
                        styles["Normal"]
            )
        )
            story.append(Spacer(1, 10))
            story.append(
                Paragraph(
                    "Missing Skills",
                    styles["Heading2"]
        )
    )
            for skill in analysis["missing_skills"]:
                story.append(
                    Paragraph(
                        f"• {skill}",
                        styles["Normal"]
            )
        )
            story.append(Spacer(1, 20))
    def add_recommendations(self, story, styles, analysis):
        story.append(
            Paragraph(
                "Recommended Roles",
                styles["Heading2"]
        )
    )
        recommendations = (
    analysis["recommendations"]
    .sort_values(
        by="Match Score",
        ascending=False
    )
).head(3)
        for _, row in recommendations.iterrows():
            story.append(
                Paragraph(
                    f"• {row['job']} ({row['Match Score']}%)",
                    styles["Normal"]
            )
        )
        story.append(Spacer(1, 20))
    def add_education(self, story, styles, analysis):
            story.append(
        Paragraph(
            "Education",
            styles["Heading2"]
        )
    )
            education = analysis["education"]
            if not education:
                story.append(
                    Paragraph(
                "No education information found.",
                styles["Normal"]
            )
        )
            else:
                for edu in education:

                    story.append(
                        Paragraph(
                    f"<b>Degree:</b> {edu.get('Degree','')}",
                    styles["Normal"]
                )
            )

                    story.append(
                Paragraph(
                    f"<b>Branch:</b> {edu.get('Branch','')}",
                    styles["Normal"]
                )
            )

                    story.append(
                        Paragraph(
                    f"<b>Institution:</b> {edu.get('Institution','')}",
                    styles["Normal"]
                )
            )
                    story.append(
                        Paragraph(
                    f"<b>Graduation Year:</b> {edu.get('Graduation Year','')}",
                    styles["Normal"]
                )
            )
                story.append(Spacer(1,10))
            story.append(Spacer(1,20))
    def add_projects(self, story, styles, analysis):
        story.append(
        Paragraph(
            "Projects",
            styles["Heading2"]
        )
    )
        projects = analysis["projects"]
        if not projects:
            story.append(
            Paragraph(
                "No projects found.",
                styles["Normal"]
            )
        )
        else:
            for project in projects:
                story.append(
                Paragraph(
                    f"<b>{project.get('Project Name','')}</b>",
                    styles["Heading3"]
                )
            )
                story.append(
                Paragraph(
                    project.get(
                        "Description",
                        "No description available."
                    ),
                    styles["Normal"]
                )
            )
                tech = project.get(
                "Technologies Mentioned",
                []
            )
                if tech:
                    story.append(
                    Paragraph(
                        "<b>Technologies Used:</b>",
                        styles["Normal"]
                    )
                )
                    story.append(
                    Paragraph(
                        ", ".join(tech),
                        styles["Normal"]
                    )
                )
                    story.append(
                Spacer(1,10)
            )
        story.append(
        Spacer(1,20)
    )
    def add_experience(self, story, styles, analysis):
        story.append(
        Paragraph(
            "Experience",
            styles["Heading2"]
        )
    )
        experience = analysis["experience"]
        if not experience:
            story.append(
            Paragraph(
                "No professional experience found.",
                styles["Normal"]
            )
        )
        else:
            for exp in experience:
                story.append(
                Paragraph(
                    f"<b>{exp.get('Role','')}</b>",
                    styles["Heading3"]
                )
            )
                story.append(
                 Paragraph(
                    exp.get(
                        "Company",
                        ""
                    ),
                    styles["Normal"]
                )
            )
                story.append(
                Paragraph(
                    exp.get(
                        "Duration",
                        ""
                    ),
                    styles["Normal"]
                )
            )
                responsibilities = exp.get(
                "Responsibilities",
                []
            )
                if responsibilities:
                    story.append(
                    Paragraph(
                        "<b>Responsibilities</b>",
                        styles["Normal"]
                    )
                )
                    for r in responsibilities:
                        story.append(
                        Paragraph(
                            f"• {r}",
                            styles["Normal"]
                        )
                    )
                story.append(
                Spacer(1,10)
            )

        story.append(
        Spacer(1,20)
    )
    def add_roadmap(self,
            story,
            styles,
            analysis
):
        roadmap = analysis["roadmap"]
        roadmap = roadmap.replace("#", "")
        roadmap = roadmap.replace("*", "")
        roadmap = roadmap.replace("**", "")
        story.append(
    Paragraph(
        roadmap
        ,styles["Normal"]
    )
)
    def add_feedback(
            self,
            story,
            styles,
            analysis
):
        story.append(
    Paragraph(
        analysis["resume_feedback"],
        styles["Normal"]
    )
)