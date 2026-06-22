"""CLI entry point for AutoThink Resume Generator."""
import argparse
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from config import USE_CREWAI
from data.mock_data import get_mock_job_description, get_mock_resume
from orchestrator.crewai_orchestrator import create_orchestrator
from utils.pdf_parser import PDFParser


def process_resume_cli(resume_path: str, job_desc_path: str = None, api_key: str = None):
    if resume_path.endswith(".pdf"):
        resume_text = PDFParser.extract_text_from_path(resume_path)
    else:
        with open(resume_path, "r", encoding="utf-8") as handle:
            resume_text = handle.read()

    job_description = None
    if job_desc_path:
        with open(job_desc_path, "r", encoding="utf-8") as handle:
            job_description = handle.read()

    demo_mode = not bool(api_key)
    orchestrator = create_orchestrator(
        api_key=api_key,
        demo_mode=demo_mode,
        use_crewai=USE_CREWAI,
    )

    print("Starting AutoThink resume processing...")
    results = orchestrator.process_resume(
        resume_text=resume_text,
        job_description=job_description,
        target_role="AI Engineer",
    )

    print("\n" + "=" * 60)
    print("AGENT LOGS")
    print("=" * 60)
    for log in results.get("logs", []):
        print(f"[{log['timestamp']}] {log['agent']}: {log['message']}")

    ats = results.get("results", {}).get("ats", {})
    if ats.get("status") == "success":
        print(f"\nATS Score: {ats.get('ats_score')}/100")

    print("\nProcessing complete.")


def main():
    parser = argparse.ArgumentParser(description="AutoThink Resume Generator")
    parser.add_argument("--resume", "-r", help="Path to resume file (PDF or TXT)")
    parser.add_argument("--job-desc", "-j", help="Path to job description file")
    parser.add_argument("--api-key", "-k", help="Gemini API key")
    parser.add_argument("--demo", action="store_true", help="Run demo with mock data")
    args = parser.parse_args()

    if args.demo or not args.resume:
        orchestrator = create_orchestrator(
            api_key=args.api_key,
            demo_mode=True,
            use_crewai=USE_CREWAI,
        )
        results = orchestrator.process_resume(
            resume_text=get_mock_resume(),
            job_description=get_mock_job_description(),
            target_role="AI Engineer",
        )
        print(f"Demo complete. ATS: {results['results']['ats'].get('ats_score')}/100")
        return

    process_resume_cli(args.resume, args.job_desc, args.api_key)


if __name__ == "__main__":
    main()
