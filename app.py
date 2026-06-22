"""Streamlit UI for AutoThink Resume Generator v2."""
import os
import sys
from datetime import datetime

import streamlit as st

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from config import GEMINI_API_KEY, ROLE_TEMPLATES, USE_CREWAI
from data.mock_data import get_mock_job_description, get_mock_resume
from orchestrator.crewai_orchestrator import create_orchestrator
from templates.role_templates import get_role_descriptions
from templates.styles import get_brand_footer, get_css_styles
from utils.api_key_manager import is_demo_mode, resolve_api_key, save_api_key_locally
from utils.diff_utils import generate_diff_html
from utils.pdf_parser import PDFParser

st.set_page_config(
    page_title="AutoThink AI Career Strategist",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(get_css_styles(), unsafe_allow_html=True)


def init_session_state() -> None:
    defaults = {
        "api_key": "",
        "resume_text": "",
        "job_description": "",
        "results": None,
        "logs": [],
        "use_crewai": USE_CREWAI,
        "force_demo": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def render_header() -> None:
    st.markdown(
        """
        <div class="header-brand">
            <h1>🚀 AutoThink AI Career Strategist</h1>
            <p>Intelligent Resume Analysis &amp; Optimization Powered by AI</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar():
    with st.sidebar:
        st.header("⚙️ Configuration")

        st.subheader("🔐 Gemini API Key")
        resolved = resolve_api_key(st.session_state.get("api_key"))
        if resolved and not st.session_state.get("api_key"):
            st.session_state.api_key = resolved

        api_key_input = st.text_input(
            "Enter Gemini API Key",
            value=st.session_state.api_key,
            type="password",
            placeholder="AIza...",
        )
        save_local = st.checkbox("Save locally", value=False)
        session_only = st.checkbox("Session only", value=True)

        if api_key_input:
            st.session_state.api_key = api_key_input
            if save_local and not session_only:
                save_api_key_locally(api_key_input)
                st.success("API key saved locally")
            st.success("API key configured")
        elif not resolve_api_key():
            st.warning("No API key found — Demo Mode active")

        st.subheader("🎯 Target Role")
        target_role = st.selectbox(
            "Select role",
            options=list(ROLE_TEMPLATES.keys()),
            format_func=lambda r: f"{r} — {get_role_descriptions()[r]}",
        )

        st.subheader("🧱 Framework")
        use_crewai = st.toggle(
            "Use CrewAI (else LangChain)",
            value=st.session_state.use_crewai,
        )
        st.session_state.use_crewai = use_crewai
        st.caption("LangChain" if not use_crewai else "CrewAI orchestrator")

        st.subheader("🧪 Demo")
        force_demo = st.checkbox("Force demo mode (mock AI)", value=False)
        use_mock_data = st.checkbox("Load mock resume/JD buttons", value=True)

        return {
            "api_key": resolve_api_key(st.session_state.api_key),
            "target_role": target_role,
            "use_crewai": use_crewai,
            "force_demo": force_demo,
            "use_mock_data": use_mock_data,
        }


def render_input_section(config: dict) -> None:
    st.header("📄 Input Data")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Resume")
        source = st.radio("Resume source", ["Upload PDF", "Paste Text"], horizontal=True)

        if source == "Upload PDF":
            pdf_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
            if pdf_file is not None:
                content = pdf_file.getvalue()
                if PDFParser.is_valid_pdf(content):
                    st.session_state.resume_text = PDFParser.extract_text(content)
                    st.success("PDF parsed successfully")
                else:
                    st.error("Invalid PDF file")
        else:
            st.session_state.resume_text = st.text_area(
                "Paste resume text",
                value=st.session_state.resume_text,
                height=260,
                label_visibility="collapsed",
            )

        if config["use_mock_data"]:
            if st.button("📋 Load Mock Resume"):
                st.session_state.resume_text = get_mock_resume()
                st.rerun()

    with col2:
        st.subheader("Job Description (optional)")
        st.session_state.job_description = st.text_area(
            "Job description",
            value=st.session_state.job_description,
            height=260,
            placeholder="Paste job description for tailored optimization...",
            label_visibility="collapsed",
        )
        if config["use_mock_data"]:
            if st.button("📋 Load Mock Job Description"):
                st.session_state.job_description = get_mock_job_description()
                st.rerun()

    if st.session_state.resume_text:
        with st.expander("📝 Extracted / Entered Resume Text"):
            st.text(st.session_state.resume_text[:4000])


def render_processing_section(config: dict) -> None:
    st.header("🚀 Process Resume")
    c1, c2, c3 = st.columns(3)

    with c1:
        process = st.button("🔄 Analyze & Optimize", use_container_width=True, type="primary")
    with c2:
        clear = st.button("🗑️ Clear All", use_container_width=True)
    with c3:
        demo_mode = is_demo_mode(config["api_key"], config["force_demo"])
        st.info("Demo Mode" if demo_mode else "Live Gemini Mode")

    if clear:
        st.session_state.resume_text = ""
        st.session_state.job_description = ""
        st.session_state.results = None
        st.session_state.logs = []
        st.rerun()

    if process:
        if not st.session_state.resume_text.strip():
            st.error("Please provide a resume")
            return

        with st.spinner("Running multi-agent pipeline..."):
            orchestrator = create_orchestrator(
                api_key=config["api_key"],
                demo_mode=demo_mode,
                use_crewai=config["use_crewai"],
            )
            results = orchestrator.process_resume(
                resume_text=st.session_state.resume_text,
                job_description=st.session_state.job_description,
                target_role=config["target_role"],
            )
            st.session_state.results = results
            st.session_state.logs = results.get("logs", [])
        st.success("Processing complete!")


def render_ats_dashboard(results: dict) -> None:
    st.subheader("ATS Compatibility Dashboard")
    ats = results.get("results", {}).get("ats", {})
    if ats.get("status") != "success":
        st.error("ATS analysis unavailable")
        return

    score = ats.get("ats_score", 0)
    breakdown = ats.get("breakdown", {})
    section_scores = ats.get("section_scores", {})

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            f'<div class="metric-card"><div class="ats-score">{score}</div>'
            f'<div style="text-align:center;color:#666;">Overall Score</div></div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.metric("Format", breakdown.get("format", 0))
    with c3:
        st.metric("Keywords", breakdown.get("keywords", 0))
    with c4:
        st.metric("Structure", breakdown.get("structure", 0))

    st.markdown("#### Section Breakdown")
    for section, value in section_scores.items():
        st.write(f"**{section.title()}**")
        st.progress(min(value, 100) / 100.0)
        st.caption(f"{value}/100")

    st.markdown("#### Recommendations")
    for rec in ats.get("recommendations", []):
        st.write(f"- {rec}")

    with st.expander("Detailed ATS Analysis"):
        st.write(ats.get("detailed_analysis", ""))


def render_agent_logs(results: dict) -> None:
    st.subheader("Live Agent Logs")
    logs = st.session_state.logs or results.get("logs", [])
    if not logs:
        st.info("No logs yet")
        return

    log_html = '<div class="agent-log">'
    for entry in logs:
        log_html += f"[{entry['timestamp']}] {entry['agent']}: {entry['message']}<br>"
    log_html += "</div>"
    st.markdown(log_html, unsafe_allow_html=True)

    times = results.get("execution_times", {})
    if times:
        st.markdown("#### Execution Summary")
        t1, t2, t3 = st.columns(3)
        t1.metric("Agents Run", len(times))
        t2.metric("Total Time", f"{sum(times.values()):.2f}s")
        t3.metric("Avg Time", f"{sum(times.values()) / len(times):.2f}s")
        for agent, duration in times.items():
            st.write(f"- **{agent}**: {duration:.2f}s")


def render_recruiter_feedback(results: dict) -> None:
    st.subheader("Recruiter Feedback")
    data = results.get("results", {}).get("recruiter", {})
    if data.get("status") != "success":
        st.error("Recruiter feedback unavailable")
        return

    likelihood = data.get("callback_likelihood", 0)
    c1, c2 = st.columns([1, 3])
    c1.metric("Callback Likelihood", f"{likelihood}%")
    c2.progress(likelihood / 100.0)
    st.info(data.get("feedback", ""))


def render_career_coaching(results: dict) -> None:
    st.subheader("Career Coach")
    data = results.get("results", {}).get("career_coach", {})
    if data.get("status") != "success":
        st.error("Career coaching unavailable")
        return

    c1, c2 = st.columns(2)
    with c1:
        st.write(f"**Target Role:** {data.get('target_role', '')}")
        st.write("**Missing Skills:**")
        for skill in data.get("skill_gaps", []):
            st.write(f"- {skill}")
    with c2:
        st.write("**Suggested Projects:**")
        for project in data.get("project_suggestions", []):
            st.write(f"- {project}")

    with st.expander("Detailed Guidance"):
        st.write(data.get("guidance", ""))


def render_diff_viewer(results: dict) -> None:
    st.subheader("Before vs After Diff Viewer")
    before = results.get("original_resume", st.session_state.resume_text)
    after = results.get("final_resume", "")
    if not after:
        finalizer = results.get("results", {}).get("finalizer", {})
        after = finalizer.get("final_resume", "")

    if not before or not after:
        st.info("Run analysis to see before/after comparison")
        return

    st.markdown(generate_diff_html(before, after), unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Original")
        st.text_area("before", before, height=300, label_visibility="collapsed")
    with c2:
        st.markdown("#### Optimized")
        st.text_area("after", after, height=300, label_visibility="collapsed")


def render_output_section(results: dict) -> None:
    st.subheader("Final Resume & Downloads")
    finalizer = results.get("results", {}).get("finalizer", {})
    solver = results.get("results", {}).get("solver", {})
    final_text = results.get("final_resume") or finalizer.get("final_resume", "")

    if final_text:
        st.text_area("Final optimized resume", final_text, height=320)
        st.download_button(
            "Download Final Resume (.txt)",
            data=final_text,
            file_name=f"resume_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
        )

    if solver.get("status") == "success":
        latex_code = solver.get("latex_code", "")
        if latex_code:
            st.download_button(
                "Download LaTeX (.tex)",
                data=latex_code,
                file_name=f"resume_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tex",
                mime="text/plain",
            )
        if solver.get("pdf_available"):
            pdf_path = solver.get("output_path", "")
            try:
                with open(pdf_path, "rb") as handle:
                    st.download_button(
                        "Download PDF",
                        data=handle.read(),
                        file_name=f"resume_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf",
                    )
            except OSError:
                st.info("PDF not found — download .tex and compile with pdflatex")
        else:
            st.info("pdflatex unavailable — .tex file ready for local compilation")


def render_results_section() -> None:
    if not st.session_state.results:
        st.info("Upload a resume and click Analyze & Optimize to get started")
        return

    results = st.session_state.results
    tabs = st.tabs(
        [
            "📊 ATS Dashboard",
            "🔍 Agent Logs",
            "💬 Recruiter",
            "🎯 Career Coach",
            "🔀 Diff Viewer",
            "📄 Output",
        ]
    )
    with tabs[0]:
        render_ats_dashboard(results)
    with tabs[1]:
        render_agent_logs(results)
    with tabs[2]:
        render_recruiter_feedback(results)
    with tabs[3]:
        render_career_coaching(results)
    with tabs[4]:
        render_diff_viewer(results)
    with tabs[5]:
        render_output_section(results)


def main() -> None:
    init_session_state()
    render_header()
    config = render_sidebar()
    st.divider()
    render_input_section(config)
    st.divider()
    render_processing_section(config)
    st.divider()
    render_results_section()
    st.divider()
    st.markdown(get_brand_footer(), unsafe_allow_html=True)


if __name__ == "__main__":
    main()
