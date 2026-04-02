"""
AI Recruitment System — Main CLI Entry Point

Usage:
    python main.py                         # Run the full pipeline
    python main.py --mode parse            # Parse sample resumes only
    python main.py --mode rank             # Score & rank candidates
    python main.py --mode bias             # Detect bias in job description
    python main.py --mode interview        # Generate interview questions (top candidate)
"""

import argparse
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel

# ── Project imports ────────────────────────────────────────────────────────────
from src.agents.bias_detector import BiasDetector
from src.agents.candidate_ranker import CandidateRanker
from src.agents.interview_generator import InterviewGenerator
from src.agents.resume_parser import ResumeParser
from src.utils.report_generator import (
    print_bias_report,
    print_final_summary,
    print_interview_questions,
    print_parsed_resume,
    print_ranking_table,
)

console = Console()

# ── Sample Job Description ─────────────────────────────────────────────────────
JOB_DESCRIPTION = """
Job Title: Senior Backend Engineer

About the Role:
We are looking for a rockstar senior backend engineer to join our high-energy young team.
You must be a ninja coder who can work independently and move fast.

Responsibilities:
- Design and build scalable distributed backend services using Python or Go
- Own the full software development lifecycle from design to production deployment
- Collaborate with product managers, frontend engineers, and data scientists
- Mentor junior developers and promote engineering best practices
- Drive technical decisions and contribute to architecture discussions

Requirements:
- 5+ years of professional software engineering experience
- Strong proficiency in Python (FastAPI, Django) or Go
- Experience with cloud platforms (AWS, GCP, or Azure)
- Deep knowledge of relational databases (PostgreSQL) and caching (Redis)
- Familiarity with containerisation (Docker, Kubernetes)
- Excellent communication skills; must be a native English speaker
- Degree in Computer Science or related field from a top university

Nice to Have:
- Experience with Kafka or other message brokers
- Knowledge of Terraform / Infrastructure as Code
- Open-source contributions

What We Offer:
- Competitive salary ($150k–$200k)
- Flexible remote work
- Equity package
- Health, dental & vision insurance
"""

RESUME_DIR = Path("data/sample_resumes")


def load_resumes() -> list[str]:
    resumes = []
    for path in sorted(RESUME_DIR.glob("*.txt")):
        resumes.append(path.read_text(encoding="utf-8"))
    if not resumes:
        console.print("[red]No resume .txt files found in data/sample_resumes/[/red]")
        sys.exit(1)
    return resumes


# ── Pipeline steps ─────────────────────────────────────────────────────────────

def run_parse() -> list:
    console.print("[bold cyan]Step 1/4 — Parsing resumes...[/bold cyan]")
    raw_resumes = load_resumes()
    parser = ResumeParser()
    parsed = parser.parse_batch(raw_resumes)
    for p in parsed:
        print_parsed_resume(p)
    return parsed


def run_bias():
    console.print("[bold cyan]Analysing job description for bias...[/bold cyan]")
    detector = BiasDetector()
    report = detector.analyse(JOB_DESCRIPTION)
    print_bias_report(report)
    return report


def run_rank(parsed):
    console.print("[bold cyan]Step 2/4 — Scoring & ranking candidates...[/bold cyan]")
    ranker = CandidateRanker()
    scores = ranker.rank(parsed, JOB_DESCRIPTION)
    print_ranking_table(scores)
    return scores


def run_interview(parsed, scores):
    console.print("[bold cyan]Step 3/4 — Generating interview questions for top candidate...[/bold cyan]")
    top_score = scores[0]
    top_candidate = next(p for p in parsed if p.name == top_score.candidate_name)
    generator = InterviewGenerator()
    questions = generator.generate(top_candidate, top_score, JOB_DESCRIPTION)
    print_interview_questions(top_candidate.name, questions)
    return questions


def run_full_pipeline():
    console.print(
        Panel(
            "[bold white]AI Recruitment System[/bold white]\n"
            "[dim]Powered by Anthropic Claude[/dim]",
            style="bold blue",
        )
    )

    parsed = run_parse()

    console.print()
    bias_report = run_bias()

    console.print()
    scores = run_rank(parsed)

    console.print()
    run_interview(parsed, scores)

    console.print()
    print_final_summary(
        job_title="Senior Backend Engineer",
        scores=scores,
        shortlist_threshold=65,
    )


# ── CLI ────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="AI Recruitment System — powered by Claude",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--mode",
        choices=["full", "parse", "rank", "bias", "interview"],
        default="full",
        help="Which part of the pipeline to run (default: full)",
    )
    args = parser.parse_args()

    mode = args.mode

    try:
        if mode == "full":
            run_full_pipeline()
        elif mode == "parse":
            run_parse()
        elif mode == "bias":
            run_bias()
        elif mode == "rank":
            parsed = run_parse()
            run_rank(parsed)
        elif mode == "interview":
            parsed = run_parse()
            scores = run_rank(parsed)
            run_interview(parsed, scores)
    except EnvironmentError as e:
        console.print(f"[red]Configuration error:[/red] {e}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Unexpected error:[/red] {e}")
        raise


if __name__ == "__main__":
    main()
