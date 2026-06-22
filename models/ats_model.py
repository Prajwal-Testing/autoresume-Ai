"""ATS analysis model."""
from typing import List

from pydantic import BaseModel


class ATSResult(BaseModel):
    overall_score: int
    format_score: int
    keywords_score: int
    structure_score: int
    clarity_score: int
    blockers_score: int
    recommendations: List[str]
    keywords_found: List[str] = []
    missing_keywords: List[str] = []

    def summary(self) -> str:
        return f"ATS Score: {self.overall_score}/100"
