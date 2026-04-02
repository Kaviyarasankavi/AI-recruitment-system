"""
Agent: Candidate Ranker
Scores and ranks candidates against a job description using AI.
"""

from src.models.schemas import CandidateScore, ParsedResume
from src.utils.claude_client import ClaudeClient

SYSTEM_PROMPT = """You are a senior HR hiring manager with 15+ years of experience.
Your task is to objectively evaluate a candidate against a job description.

Return ONLY a valid JSON object with these exact keys:
{
  "candidate_name": "Candidate's full name",
  "overall_score": 85,
  "skills_match": 90,
  "experience_match": 80,
  "education_match": 85,
  "strengths": ["strength 1", "strength 2", "strength 3"],
  "gaps": ["gap 1", "gap 2"],
  "recommendation": "Strong hire / Consider / Pass — with one sentence justification"
}

Scores are integers 0-100. Be fair and objective. Return ONLY the JSON object."""


class CandidateRanker:
    """Scores each candidate against a job description and sorts by score."""

    def __init__(self):
        self.client = ClaudeClient()

    def score(self, candidate: ParsedResume, job_description: str) -> CandidateScore:
        """
        Score a single candidate against a job description.

        Args:
            candidate: Parsed resume data.
            job_description: Full job posting text.

        Returns:
            CandidateScore: Scored evaluation.
        """
        prompt = f"""Job Description:
{job_description}

---

Candidate Profile:
Name: {candidate.name}
Skills: {', '.join(candidate.skills)}
Experience (years): {candidate.experience_years}
Experience:
{self._format_experience(candidate.experience)}
Education:
{self._format_education(candidate.education)}
Certifications: {', '.join(candidate.certifications)}
Summary: {candidate.summary}

Evaluate this candidate against the job description."""

        data = self.client.chat_json(system=SYSTEM_PROMPT, user=prompt)
        return CandidateScore(**data)

    def rank(
        self, candidates: list[ParsedResume], job_description: str
    ) -> list[CandidateScore]:
        """
        Score and rank all candidates, highest overall_score first.

        Args:
            candidates: List of parsed resumes.
            job_description: Full job posting text.

        Returns:
            Sorted list of CandidateScore objects.
        """
        scores = [self.score(c, job_description) for c in candidates]
        return sorted(scores, key=lambda s: s.overall_score, reverse=True)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _format_experience(experience: list[dict]) -> str:
        lines = []
        for exp in experience:
            lines.append(f"  - {exp.get('title')} at {exp.get('company')} ({exp.get('duration')})")
            for h in exp.get("highlights", []):
                lines.append(f"      • {h}")
        return "\n".join(lines) if lines else "  None listed"

    @staticmethod
    def _format_education(education: list[dict]) -> str:
        lines = []
        for edu in education:
            lines.append(f"  - {edu.get('degree')} — {edu.get('institution')} ({edu.get('year')})")
        return "\n".join(lines) if lines else "  None listed"
