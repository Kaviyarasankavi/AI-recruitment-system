"""
Utility: Report Generator
Renders a beautiful terminal recruitment report using Rich.
"""

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from src.models.schemas import (
    BiasReport,
    CandidateScore,
    InterviewQuestion,
    ParsedResume,
)

console = Console()


def print_header(title: str) -> None:
    console.print()
    console.rule(f"[bold cyan]{title}[/bold cyan]")
    console.print()


def print_parsed_resume(resume: ParsedResume) -> None:
    print_header(f"📄 Parsed Resume — {resume.name}")

    info = Table.grid(padding=(0, 2))
    info.add_column(style="bold green")
    info.add_column()
    info.add_row("Email", resume.email or "—")
    info.add_row("Phone", resume.phone or "—")
    info.add_row("Location", resume.location or "—")
    info.add_row("Experience", f"{resume.experience_years} years")
    info.add_row("Skills", ", ".join(resume.skills) if resume.skills else "—")
    info.add_row("Certifications", ", ".join(resume.certifications) if resume.certifications else "—")
    console.print(Panel(info, title="[bold]Contact & Skills[/bold]", border_style="blue"))

    if resume.summary:
        console.print(Panel(resume.summary, title="Summary", border_style="dim"))


def print_ranking_table(scores: list[CandidateScore]) -> None:
    print_header("🏆 Candidate Rankings")

    table = Table(box=box.ROUNDED, show_header=True, header_style="bold magenta")
    table.add_column("Rank", justify="center", width=6)
    table.add_column("Candidate", style="bold")
    table.add_column("Overall", justify="center")
    table.add_column("Skills", justify="center")
    table.add_column("Experience", justify="center")
    table.add_column("Education", justify="center")
    table.add_column("Recommendation")

    for i, s in enumerate(scores, 1):
        colour = "green" if s.overall_score >= 75 else ("yellow" if s.overall_score >= 55 else "red")
        table.add_row(
            str(i),
            s.candidate_name,
            f"[{colour}]{s.overall_score}[/{colour}]",
            str(s.skills_match),
            str(s.experience_match),
            str(s.education_match),
            s.recommendation,
        )

    console.print(table)

    # Detailed breakdown for top candidate
    top = scores[0]
    console.print(
        Panel(
            f"[bold green]Strengths:[/bold green] {', '.join(top.strengths)}\n"
            f"[bold red]Gaps:[/bold red] {', '.join(top.gaps) or 'None identified'}",
            title=f"[bold]Top Candidate Breakdown — {top.candidate_name}[/bold]",
            border_style="green",
        )
    )


def print_bias_report(report: BiasReport) -> None:
    print_header("⚖️  Bias Analysis")

    score_colour = "green" if report.overall_bias_score < 3 else ("yellow" if report.overall_bias_score < 6 else "red")
    console.print(
        f"  Bias Score: [{score_colour}]{report.overall_bias_score}/10[/{score_colour}]  "
        f"({'Low' if report.overall_bias_score < 3 else 'Moderate' if report.overall_bias_score < 6 else 'High'} bias detected)"
    )
    console.print()

    if report.biased_phrases:
        table = Table(box=box.SIMPLE, show_header=True, header_style="bold yellow")
        table.add_column("Phrase", style="bold red")
        table.add_column("Type")
        table.add_column("Explanation")
        for bp in report.biased_phrases:
            table.add_row(bp["phrase"], bp["type"], bp["explanation"])
        console.print(table)

    if report.suggestions:
        console.print("[bold]Suggestions:[/bold]")
        for s in report.suggestions:
            console.print(f"  • {s}")

    console.print()
    console.print(
        Panel(
            report.improved_description,
            title="[bold green]✅ Improved Job Description[/bold green]",
            border_style="green",
        )
    )


def print_interview_questions(
    candidate_name: str, questions: list[InterviewQuestion]
) -> None:
    print_header(f"🎤 Interview Questions — {candidate_name}")

    category_colours = {
        "Technical": "cyan",
        "Behavioural": "magenta",
        "Situational": "yellow",
        "Cultural Fit": "green",
    }

    for i, q in enumerate(questions, 1):
        colour = category_colours.get(q.category, "white")
        difficulty_colour = {"Easy": "green", "Medium": "yellow", "Hard": "red"}.get(
            q.difficulty, "white"
        )
        console.print(
            Panel(
                f"[bold]{q.question}[/bold]\n\n"
                f"[dim]Rationale: {q.rationale}[/dim]",
                title=f"[{colour}]Q{i}: {q.category}[/{colour}]  "
                f"[{difficulty_colour}]{q.difficulty}[/{difficulty_colour}]",
                border_style=colour,
            )
        )


def print_final_summary(
    job_title: str,
    scores: list[CandidateScore],
    shortlist_threshold: int = 65,
) -> None:
    print_header("📊 Final Recruitment Summary")

    shortlisted = [s for s in scores if s.overall_score >= shortlist_threshold]
    passed = [s for s in scores if s.overall_score < shortlist_threshold]

    table = Table.grid(padding=(0, 2))
    table.add_column(style="bold green")
    table.add_column()
    table.add_row("Job Title", job_title)
    table.add_row("Total Candidates", str(len(scores)))
    table.add_row("Shortlisted", str(len(shortlisted)))
    table.add_row("Not Shortlisted", str(len(passed)))
    table.add_row(
        "Top Candidate",
        f"[bold green]{scores[0].candidate_name}[/bold green] ({scores[0].overall_score}/100)"
        if scores
        else "—",
    )

    console.print(Panel(table, title="Summary", border_style="cyan"))

    if shortlisted:
        console.print("\n[bold green]✅ Shortlisted Candidates:[/bold green]")
        for s in shortlisted:
            console.print(f"   • {s.candidate_name} — Score: {s.overall_score}/100")

    if passed:
        console.print("\n[bold red]❌ Not Shortlisted:[/bold red]")
        for s in passed:
            console.print(f"   • {s.candidate_name} — Score: {s.overall_score}/100")

    console.print()
    console.rule("[dim]End of Report[/dim]")
