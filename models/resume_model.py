"""Data models for resume structure."""
from typing import Any, Dict, List

from pydantic import BaseModel, Field


class PersonalInfo(BaseModel):
    name: str = ""
    email: str = ""
    phone: str = ""
    location: str = ""


class Experience(BaseModel):
    company: str = ""
    title: str = ""
    duration: str = ""
    description: List[str] = Field(default_factory=list)


class Education(BaseModel):
    school: str = ""
    degree: str = ""
    field: str = ""
    year: str = ""


class ResumeData(BaseModel):
    personal_info: PersonalInfo = Field(default_factory=PersonalInfo)
    summary: str = ""
    experience: List[Experience] = Field(default_factory=list)
    skills: List[str] = Field(default_factory=list)
    education: List[Education] = Field(default_factory=list)
    projects: List[Dict[str, Any]] = Field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()

    def to_text(self) -> str:
        lines: List[str] = []
        if self.personal_info.name:
            lines.extend(["=" * 50, self.personal_info.name.upper(), "=" * 50])
            contact = [
                x
                for x in [
                    self.personal_info.email,
                    self.personal_info.phone,
                    self.personal_info.location,
                ]
                if x
            ]
            if contact:
                lines.append(" | ".join(contact))

        if self.summary:
            lines.extend(["", "PROFESSIONAL SUMMARY", self.summary])

        if self.experience:
            lines.extend(["", "EXPERIENCE"])
            for exp in self.experience:
                lines.extend([f"{exp.title} at {exp.company}", exp.duration])
                for desc in exp.description:
                    lines.append(f"  - {desc}")

        if self.skills:
            lines.extend(["", "SKILLS", ", ".join(self.skills)])

        if self.education:
            lines.extend(["", "EDUCATION"])
            for edu in self.education:
                lines.append(f"{edu.degree} in {edu.field} - {edu.school} ({edu.year})")

        return "\n".join(lines)
