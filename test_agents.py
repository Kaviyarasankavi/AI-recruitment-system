"""
Unit tests for AI Recruitment System agents.
Uses mocking so no real API calls are made.
"""

import json
import unittest
from unittest.mock import MagicMock, patch

from src.agents.bias_detector import BiasDetector
from src.agents.candidate_ranker import CandidateRanker
from src.agents.interview_generator import InterviewGenerator
from src.agents.resume_parser import ResumeParser
from src.models.schemas import CandidateScore, ParsedResume


SAMPLE_RESUME_TEXT = """
Jane Doe | jane@example.com | New York, NY
Skills: Python, AWS, Docker
5 years experience as a Software Engineer at Acme Corp.
B.Sc. Computer Science, Columbia University (2018)
"""

MOCK_PARSED = {
    "name": "Jane Doe",
    "email": "jane@example.com",
    "phone": "",
    "location": "New York, NY",
    "summary": "Experienced software engineer.",
    "skills": ["Python", "AWS", "Docker"],
    "experience_years": 5.0,
    "experience": [{"title": "SWE", "company": "Acme", "duration": "2019-2024", "highlights": []}],
    "education": [{"degree": "B.Sc. CS", "institution": "Columbia", "year": "2018"}],
    "certifications": [],
    "languages": ["English"],
}

MOCK_SCORE = {
    "candidate_name": "Jane Doe",
    "overall_score": 82,
    "skills_match": 88,
    "experience_match": 80,
    "education_match": 78,
    "strengths": ["Strong Python skills", "Cloud expertise"],
    "gaps": ["No Kubernetes experience"],
    "recommendation": "Strong hire — well-matched technical profile.",
}

MOCK_BIAS = {
    "overall_bias_score": 2.5,
    "biased_phrases": [
        {"phrase": "rockstar developer", "type": "Gender-coded", "explanation": "Masculine-coded language."}
    ],
    "suggestions": ["Replace 'rockstar' with 'skilled' or 'experienced'."],
    "improved_description": "We are looking for a skilled backend engineer...",
}

MOCK_QUESTIONS = [
    {
        "category": "Technical",
        "question": "How do you manage AWS IAM permissions in a multi-team environment?",
        "rationale": "Tests cloud expertise.",
        "difficulty": "Medium",
    }
]


class TestResumeParser(unittest.TestCase):
    @patch("src.agents.resume_parser.ClaudeClient")
    def test_parse_returns_parsed_resume(self, MockClient):
        mock_instance = MagicMock()
        mock_instance.chat_json.return_value = MOCK_PARSED
        MockClient.return_value = mock_instance

        parser = ResumeParser()
        result = parser.parse(SAMPLE_RESUME_TEXT)

        self.assertIsInstance(result, ParsedResume)
        self.assertEqual(result.name, "Jane Doe")
        self.assertIn("Python", result.skills)
        self.assertEqual(result.experience_years, 5.0)

    @patch("src.agents.resume_parser.ClaudeClient")
    def test_parse_batch(self, MockClient):
        mock_instance = MagicMock()
        mock_instance.chat_json.return_value = MOCK_PARSED
        MockClient.return_value = mock_instance

        parser = ResumeParser()
        results = parser.parse_batch([SAMPLE_RESUME_TEXT, SAMPLE_RESUME_TEXT])

        self.assertEqual(len(results), 2)
        self.assertTrue(all(isinstance(r, ParsedResume) for r in results))


class TestCandidateRanker(unittest.TestCase):
    @patch("src.agents.candidate_ranker.ClaudeClient")
    def test_score_returns_candidate_score(self, MockClient):
        mock_instance = MagicMock()
        mock_instance.chat_json.return_value = MOCK_SCORE
        MockClient.return_value = mock_instance

        ranker = CandidateRanker()
        candidate = ParsedResume(**MOCK_PARSED)
        result = ranker.score(candidate, "Backend engineer needed.")

        self.assertIsInstance(result, CandidateScore)
        self.assertEqual(result.overall_score, 82)
        self.assertIn("Python", " ".join(result.strengths))

    @patch("src.agents.candidate_ranker.ClaudeClient")
    def test_rank_sorts_by_score(self, MockClient):
        scores = [
            {**MOCK_SCORE, "candidate_name": "Alice", "overall_score": 90},
            {**MOCK_SCORE, "candidate_name": "Bob", "overall_score": 60},
            {**MOCK_SCORE, "candidate_name": "Carol", "overall_score": 80},
        ]
        mock_instance = MagicMock()
        mock_instance.chat_json.side_effect = scores
        MockClient.return_value = mock_instance

        ranker = CandidateRanker()
        candidates = [ParsedResume(**MOCK_PARSED)] * 3
        ranked = ranker.rank(candidates, "Backend engineer needed.")

        self.assertEqual(ranked[0].overall_score, 90)
        self.assertEqual(ranked[-1].overall_score, 60)


class TestBiasDetector(unittest.TestCase):
    @patch("src.agents.bias_detector.ClaudeClient")
    def test_analyse_returns_bias_report(self, MockClient):
        mock_instance = MagicMock()
        mock_instance.chat_json.return_value = MOCK_BIAS
        MockClient.return_value = mock_instance

        detector = BiasDetector()
        result = detector.analyse("We want a rockstar developer!")

        self.assertEqual(result.overall_bias_score, 2.5)
        self.assertEqual(len(result.biased_phrases), 1)
        self.assertIn("rockstar", result.biased_phrases[0]["phrase"])


class TestInterviewGenerator(unittest.TestCase):
    @patch("src.agents.interview_generator.ClaudeClient")
    def test_generate_returns_questions(self, MockClient):
        mock_instance = MagicMock()
        mock_instance.chat_json.return_value = MOCK_QUESTIONS
        MockClient.return_value = mock_instance

        generator = InterviewGenerator()
        candidate = ParsedResume(**MOCK_PARSED)
        score = CandidateScore(**MOCK_SCORE)
        result = generator.generate(candidate, score, "Backend engineer needed.")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].category, "Technical")
        self.assertEqual(result[0].difficulty, "Medium")


if __name__ == "__main__":
    unittest.main()
