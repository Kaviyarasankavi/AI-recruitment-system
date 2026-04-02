"""
Agent: Interview Question Generator
Creates tailored interview questions based on job description and candidate profile.
"""

from src.models.schemas import CandidateScore, InterviewQuestion, ParsedResume
from src.utils.claude_client import ClaudeClient

SYSTEM_PROMPT = """You are an expert technical interviewer and people manager.
Generate a set of 8 tailored interview questions for a specific candidate.

The questions should be personalised — referencing the candidate's background,
skill gaps, and the job requirements.

Return ONLY a valid JSON array with this structure:
[
  {
    "category": "Technical | Behavioural | Situational | Cultural Fit",
    "question": "The full interview question",
    "rationale": "Why this question is relevant for this candidate",
    "difficulty": "Easy | Medium | Hard"
  }
]

Include a mix of: 3 Technical, 2 Behavioural, 2 Situational, 1 Cultural Fit.
Return ONLY the JSON array."""


class InterviewGenerator:
    """Generates tailored interview questions for each shortlisted candidate."""

    def __init__(self):
        self.client = ClaudeClient()

    def generate(
        self,
        candidate: ParsedResume,
        score: CandidateScore,
        job_description: str,
    ) -> list[InterviewQuestion]:
        """
        Generate interview questions for a candidate.

        Args:
            candidate: Parsed resume data.
            score: The candidate's evaluation scores.
            job_description: Full job posting text.

        Returns:
            List of InterviewQuestion objects.
        """
        prompt = f"""Job Description:
{job_description}

---

Candidate: {candidate.name}
Skills: {', '.join(candidate.skills)}
Experience: {candidate.experience_years} years
Strengths: {', '.join(score.strengths)}
Gaps identified: {', '.join(score.gaps)}
Overall Score: {score.overall_score}/100

Generate 8 tailored interview questions for this candidate."""

        data = self.client.chat_json(system=SYSTEM_PROMPT, user=prompt)
        return [InterviewQuestion(**q) for q in data]
