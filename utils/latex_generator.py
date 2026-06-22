"""LaTeX resume generation and PDF compilation."""
import os
import re
import subprocess
from typing import Any, Dict, List, Tuple

from config import LATEX_OUTPUT_DIR


class LaTeXGenerator:
    LATEX_TEMPLATE = r"""
\documentclass[11pt,letterpaper]{article}
\usepackage[utf-8]{inputenc}
\usepackage[margin=0.5in]{geometry}
\usepackage{hyperref}
\usepackage{enumitem}
\hypersetup{colorlinks=true, urlcolor=blue}
\pagestyle{empty}
\newcommand{\sectionheader}[1]{\vspace{6pt}\textbf{\large #1}\vspace{-8pt}\hrule\vspace{6pt}}
\begin{document}
%(resume_content)s
\end{document}
"""

    @staticmethod
    def _escape(text: str) -> str:
        replacements = {
            "\\": r"\textbackslash{}",
            "&": r"\&",
            "%": r"\%",
            "$": r"\$",
            "#": r"\#",
            "_": r"\_",
            "{": r"\{",
            "}": r"\}",
        }
        result = text
        for char, escaped in replacements.items():
            result = result.replace(char, escaped)
        return result

    @staticmethod
    def generate_latex(resume_data: Dict[str, Any]) -> str:
        content: List[str] = []
        personal = resume_data.get("personal_info", {})

        name = personal.get("name") or "Professional Resume"
        content.append(f"\\textbf{{\\Large {LaTeXGenerator._escape(name)}}}\\\\")
        contact = [
            personal.get("email", ""),
            personal.get("phone", ""),
            personal.get("location", ""),
        ]
        contact = [LaTeXGenerator._escape(c) for c in contact if c]
        if contact:
            content.append(" | ".join(contact) + "\\\\")
        content.append("\\vspace{8pt}")

        summary = resume_data.get("summary", "")
        if summary:
            content.append("\\sectionheader{Professional Summary}")
            content.append(LaTeXGenerator._escape(summary))
            content.append("\\vspace{6pt}")

        experience = resume_data.get("experience", [])
        if experience:
            content.append("\\sectionheader{Experience}")
            for job in experience:
                title = LaTeXGenerator._escape(job.get("title", ""))
                company = LaTeXGenerator._escape(job.get("company", ""))
                duration = LaTeXGenerator._escape(job.get("duration", ""))
                content.append(f"\\textbf{{{title}}} \\hfill {duration}\\\\")
                content.append(f"\\textit{{{company}}}\\\\")
                bullets = job.get("description", [])
                if isinstance(bullets, str):
                    bullets = [line.strip("-• ") for line in bullets.split("\n") if line.strip()]
                if bullets:
                    content.append("\\begin{itemize}[leftmargin=*]")
                    for bullet in bullets:
                        content.append(f"  \\item {LaTeXGenerator._escape(str(bullet))}")
                    content.append("\\end{itemize}")

        skills = resume_data.get("skills", [])
        if skills:
            content.append("\\sectionheader{Skills}")
            content.append(LaTeXGenerator._escape(", ".join(str(s) for s in skills)))

        education = resume_data.get("education", [])
        if education:
            content.append("\\sectionheader{Education}")
            for edu in education:
                degree = LaTeXGenerator._escape(edu.get("degree", ""))
                field = LaTeXGenerator._escape(edu.get("field", ""))
                school = LaTeXGenerator._escape(edu.get("school", ""))
                year = LaTeXGenerator._escape(edu.get("year", ""))
                content.append(f"\\textbf{{{degree}}} in {field}\\\\")
                content.append(f"{school} | {year}\\\\")

        return LaTeXGenerator.LATEX_TEMPLATE.replace(
            "%(resume_content)s",
            "\n".join(content),
        )

    @staticmethod
    def generate_latex_from_text(resume_text: str, name: str = "Candidate") -> str:
        safe = LaTeXGenerator._escape(resume_text)
        body = safe.replace("\n", "\\\\\n")
        data = {
            "personal_info": {"name": name},
            "summary": resume_text[:500],
            "experience": [],
            "skills": [],
            "education": [],
        }
        return LaTeXGenerator.generate_latex(data) if not resume_text else (
            LaTeXGenerator.LATEX_TEMPLATE.replace(
                "%(resume_content)s",
                f"\\textbf{{\\Large {LaTeXGenerator._escape(name)}}}\\\\\\vspace{{8pt}}\n{body}",
            )
        )

    @staticmethod
    def compile_pdf(latex_code: str, output_name: str = "resume") -> Tuple[bool, str]:
        try:
            os.makedirs(LATEX_OUTPUT_DIR, exist_ok=True)
            tex_file = os.path.join(LATEX_OUTPUT_DIR, f"{output_name}.tex")
            with open(tex_file, "w", encoding="utf-8") as handle:
                handle.write(latex_code)

            try:
                result = subprocess.run(
                    [
                        "pdflatex",
                        "-interaction=nonstopmode",
                        f"-output-directory={LATEX_OUTPUT_DIR}",
                        tex_file,
                    ],
                    capture_output=True,
                    timeout=30,
                    text=True,
                )
                pdf_path = os.path.join(LATEX_OUTPUT_DIR, f"{output_name}.pdf")
                if result.returncode == 0 and os.path.exists(pdf_path):
                    return True, pdf_path
            except (FileNotFoundError, subprocess.TimeoutExpired):
                pass

            return False, tex_file
        except Exception as exc:
            return False, f"Error: {exc}"
