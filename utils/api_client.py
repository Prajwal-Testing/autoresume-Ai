"""Gemini API client with LangChain integration and demo mode."""
from typing import Optional

from config import GEMINI_MODEL, MAX_TOKENS

try:
    import google.generativeai as genai
except ImportError:
    genai = None

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.messages import HumanMessage
except ImportError:
    ChatGoogleGenerativeAI = None
    HumanMessage = None


class GeminiClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        demo_mode: bool = False,
        use_langchain: bool = True,
    ):
        self.api_key = api_key or ""
        self.model_name = GEMINI_MODEL
        self.demo_mode = demo_mode or not bool(self.api_key)
        self.use_langchain = use_langchain and not self.demo_mode
        self.model = None
        self.langchain_model = None

        if not self.demo_mode and self.api_key:
            if self.use_langchain and ChatGoogleGenerativeAI is not None:
                self.langchain_model = ChatGoogleGenerativeAI(
                    model=self.model_name,
                    google_api_key=self.api_key,
                    temperature=0.7,
                    max_output_tokens=MAX_TOKENS,
                )
            elif genai is not None:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel(self.model_name)

    def generate(self, prompt: str, max_tokens: int = MAX_TOKENS) -> str:
        if self.demo_mode:
            return self._get_mock_response(prompt)

        try:
            if self.langchain_model is not None and HumanMessage is not None:
                response = self.langchain_model.invoke([HumanMessage(content=prompt)])
                return response.content

            if self.model is not None and genai is not None:
                response = self.model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        max_output_tokens=max_tokens,
                        temperature=0.7,
                    ),
                )
                return response.text

            return self._get_mock_response(prompt)
        except Exception as exc:
            return f"Error: {exc}"

    def _get_mock_response(self, prompt: str) -> str:
        lower = prompt.lower()
        if "parser" in lower or "extract" in lower:
            return (
                "PARSED RESUME DATA:\n"
                "Name: John Doe\nEmail: john@example.com\n"
                "SKILLS: Python, TensorFlow, PyTorch, SQL, AWS"
            )
        if "analyzer" in lower or "analyze" in lower:
            return (
                "ANALYSIS COMPLETE:\n"
                "Keywords Found: 15 technical keywords\n"
                "Alignment Score: 72%\n"
                "Recommendations: Add metrics and cloud experience."
            )
        if "ats" in lower:
            return "ATS SCORE: 78/100. Add quantifiable metrics."
        if "recruiter" in lower:
            return (
                "Strong first impression. Clear metrics and progression. "
                "Callback likelihood: 8/10."
            )
        if "critic" in lower or "critical" in lower:
            return "Main weakness: passive language. Fix metrics in experience bullets."
        if "improve" in lower:
            return (
                "Before: Managed team\n"
                "After: Led cross-functional team of 8 engineers, delivering 3 releases\n"
                "Why: Stronger action verb and quantifiable impact."
            )
        if "career coach" in lower or "career" in lower:
            return (
                "Missing skills: Kubernetes, MLOps.\n"
                "Suggested projects: RAG system, LLM fine-tuning pipeline."
            )
        if "finalizer" in lower or "finalize" in lower:
            return (
                "FINAL RESUME:\n"
                "JOHN DOE\n"
                "Senior ML Engineer with 5+ years building production AI systems.\n"
                "- Improved model accuracy by 23% using transformer architecture\n"
                "- Reduced inference latency 50% via quantization"
            )
        if "latex" in lower or "solver" in lower:
            return (
                "Improved resume with stronger bullets, ATS keywords, "
                "and quantified achievements throughout."
            )
        return "Mock response generated. Demo mode active (no API key)."

    def is_available(self) -> bool:
        return bool(self.api_key) and not self.demo_mode
