"""
Data models / schemas for the AI Recruitment System.
"""

from pydantic import BaseModel, Field
from typing import Optional


class ParsedResume(BaseModel):
    name: str = ""
    email: str = ""
    phone: str = ""
    location: str = ""
    summary: str = ""
    skills: list[str] = Field(default_factory=list)
    experience_years: float = 0.0
    experience: list[dict] = Field(default_factory=list)
    education: list[dict] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    languages: list[str] = Field(default_factory=list)


class CandidateScore(BaseModel):
    candidate_name: str
    overall_score: float = Field(ge=0, le=100)
    skills_match: float = Field(ge=0, le=100)
    experience_match: float = Field(ge=0, le=100)
    education_match: float = Field(ge=0, le=100)
    strengths: list[str] = Field(default_factory=list)
    gaps: list[str] = Field(default_factory=list)
    recommendation: str = ""


class BiasReport(BaseModel):
    overall_bias_score: float = Field(ge=0, le=10)
    biased_phrases: list[dict] = Field(default_factory=list)
    suggestions: list[str] = Field(default_factory=list)
    improved_description: str = ""


class InterviewQuestion(BaseModel):
    category: str
    question: str
    rationale: str
    difficulty: str


class RecruitmentReport(BaseModel):
    job_title: str
    total_candidates: int
    shortlisted: list[str]
    top_candidate: str
    bias_summary: str
    interview_ready: bool
    notes: str
