"""
Agent: Resume Parser
Extracts structured candidate information from raw resume text.
"""

from src.models.schemas import ParsedResume
from src.utils.claude_client import ClaudeClient

SYSTEM_PROMPT = """You are an expert HR resume parser.
Your job is to extract structured information from resumes.

Return ONLY a valid JSON object with these exact keys:
{
  "name": "Full Name",
  "email": "email@example.com",
  "phone": "+1-xxx-xxx-xxxx",
  "location": "City, Country",
  "summary": "Brief professional summary",
  "skills": ["skill1", "skill2"],
  "experience_years": 5.0,
  "experience": [
    {
      "title": "Job Title",
      "company": "Company Name",
      "duration": "2020 - 2023",
      "highlights": ["achievement 1", "achievement 2"]
    }
  ],
  "education": [
    {
      "degree": "B.Sc Computer Science",
      "institution": "University Name",
      "year": "2018"
    }
  ],
  "certifications": ["AWS Certified", "PMP"],
  "languages": ["English", "Spanish"]
}

Return ONLY the JSON object. No explanation, no markdown fences."""


class ResumeParser:
    """Parses raw resume text into a structured ParsedResume object."""

    def __init__(self):
        self.client = ClaudeClient()

    def parse(self, resume_text: str) -> ParsedResume:
        """
        Args:
            resume_text: Raw plaintext content of a resume.

        Returns:
            ParsedResume: Validated structured resume data.
        """
        data = self.client.chat_json(
            system=SYSTEM_PROMPT,
            user=f"Parse this resume:\n\n{resume_text}",
        )
        return ParsedResume(**data)

    def parse_batch(self, resumes: list[str]) -> list[ParsedResume]:
        """Parse multiple resumes and return a list of ParsedResume objects."""
        return [self.parse(r) for r in resumes]
