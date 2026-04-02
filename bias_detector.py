"""
Agent: Bias Detector
Analyses job descriptions for biased language and suggests improvements.
"""

from src.models.schemas import BiasReport
from src.utils.claude_client import ClaudeClient

SYSTEM_PROMPT = """You are a Diversity, Equity & Inclusion (DEI) specialist.
Analyse job descriptions for potentially biased, exclusive, or non-inclusive language.

Look for:
- Gender-coded language (e.g., "rockstar", "ninja", "aggressive", "nurturing")
- Age bias ("young and energetic", "recent graduate only", "digital native")
- Unnecessarily exclusive requirements (e.g., "must have X years" when experience level isn't critical)
- Cultural bias or assumptions
- Ableist language

Return ONLY a valid JSON object:
{
  "overall_bias_score": 3.5,
  "biased_phrases": [
    {
      "phrase": "the exact biased phrase",
      "type": "Gender-coded | Age bias | Exclusive requirement | Cultural bias | Ableist",
      "explanation": "Why this is problematic"
    }
  ],
  "suggestions": [
    "Actionable suggestion to improve the JD"
  ],
  "improved_description": "The full rewritten job description with bias removed"
}

overall_bias_score is a float from 0 (no bias) to 10 (highly biased).
Return ONLY the JSON object."""


class BiasDetector:
    """Detects bias in job descriptions and proposes improvements."""

    def __init__(self):
        self.client = ClaudeClient()

    def analyse(self, job_description: str) -> BiasReport:
        """
        Analyse a job description for biased language.

        Args:
            job_description: Full text of the job posting.

        Returns:
            BiasReport with findings and an improved description.
        """
        data = self.client.chat_json(
            system=SYSTEM_PROMPT,
            user=f"Analyse this job description for bias:\n\n{job_description}",
            max_tokens=3000,
        )
        return BiasReport(**data)
