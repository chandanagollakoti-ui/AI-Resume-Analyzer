import streamlit as st
import requests
from datetime import datetime

BACKEND_URL = "https://ai-resume-analyzer-ks1y.onrender.com/upload"

# ==================================
# PAGE CONFIG
# ==================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# ==================================
# CUSTOM CSS
# ==================================

st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

.hero {
    padding: 25px;
    border-radius: 15px;
    margin-bottom: 20px;
    border: 1px solid rgba(128,128,128,0.2);
}

.card {
    padding: 15px;
    border-radius: 12px;
    border: 1px solid rgba(128,128,128,0.2);
    margin-bottom: 10px;
}

div[data-testid="stMetric"] {
    border: 1px solid rgba(128,128,128,0.2);
    padding: 15px;
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

# ==================================
# SESSION STATE
# ==================================

if "history" not in st.session_state:
    st.session_state.history = []

# ==================================
# SIDEBAR
# ==================================

with st.sidebar:

    st.markdown("# 📄 AI Resume Analyzer")

    st.markdown("---")

    st.subheader("🚀 Navigation")

    st.write("🏠 Home")
    st.write("📄 Resume Analysis")
    st.write("📊 Reports")

    st.markdown("---")

    st.subheader("⚡ Quick Stats")

    st.metric(
        "📑 Analyses",
        len(st.session_state.history)
    )

    st.metric(
        "🤖 AI Model",
        "Gemini"
    )

    st.markdown("---")

    st.subheader("🕒 Recent Files")

    if st.session_state.history:

        for item in reversed(st.session_state.history[-5:]):

            st.info(
                f"📄 {item['filename']}"
            )

    else:

        st.caption(
            "No analysis yet"
        )

# ==================================
# HERO SECTION
# ==================================

st.markdown("""
<div class="hero">
<h1>📄 AI Resume Analyzer</h1>

<h4>
AI-Powered ATS Resume Screening using FastAPI & Google Gemini
</h4>

<p>
Upload your resume, compare it against a job description,
and receive intelligent AI-powered feedback.
</p>
</div>
""", unsafe_allow_html=True)

# ==================================
# INPUT SECTION
# ==================================

col1, col2 = st.columns(2)

with col1:

    uploaded_file = st.file_uploader(
        "📂 Upload Resume (PDF)",
        type=["pdf"]
    )

with col2:

    job_description = st.text_area(
        "💼 Paste Job Description",
        height=220,
        placeholder="Paste job description here..."
    )

# ==================================
# FILE DETAILS
# ==================================

if uploaded_file:

    file_size = uploaded_file.size / 1024

    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            "📄 File Name",
            uploaded_file.name
        )

    with c2:
        st.metric(
            "📦 File Size",
            f"{file_size:.2f} KB"
        )

# ==================================
# ANALYZE BUTTON
# ==================================

analyze = st.button(
    "🚀 Analyze Resume",
    use_container_width=True
)

# ==================================
# ANALYSIS SECTION
# ==================================

if analyze:

    if uploaded_file is None:

        st.error(
            "Please upload a PDF resume."
        )

    elif not job_description.strip():

        st.error(
            "Please enter a job description."
        )

    else:

        with st.spinner(
            "🔍 Analyzing Resume..."
        ):

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    "application/pdf"
                )
            }

            data = {
                "job_description": job_description
            }

            try:

                response = requests.post(
                    BACKEND_URL,
                    files=files,
                    data=data,
                    timeout=120
                )

                if response.status_code == 200:

                    result = response.json()

                    analysis_text = result["analysis"]

                    st.session_state.history.append(
                        {
                            "filename": uploaded_file.name,
                            "time": datetime.now().strftime(
                                "%d-%m-%Y %H:%M"
                            ),
                            "analysis": analysis_text
                        }
                    )

                    st.success(
                        "✅ Analysis Completed Successfully"
                    )

                    # ==========================
                    # METRICS
                    # ==========================

                    m1, m2, m3 = st.columns(3)

                    with m1:
                        st.metric(
                            "📄 Resume",
                            uploaded_file.name
                        )

                    with m2:
                        st.metric(
                            "🧠 Status",
                            "Completed"
                        )

                    with m3:
                        st.metric(
                            "⚡ AI",
                            "Gemini"
                        )

                    st.markdown("---")

                    # ==========================
                    # ANALYSIS DISPLAY
                    # ==========================

                    with st.expander(
                        "📊 View Full Analysis",
                        expanded=True
                    ):

                        st.markdown(
                            analysis_text
                        )

                    # ==========================
                    # DOWNLOAD
                    # ==========================

                    with st.expander(
                        "📥 Download Report"
                    ):

                        st.download_button(
                            label="📄 Download Analysis",
                            data=analysis_text,
                            file_name="resume_analysis.txt",
                            mime="text/plain"
                        )

                else:

                    st.error(
                        f"Server Error: {response.status_code}"
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "❌ Unable to connect to backend."
                )

            except Exception as e:

                st.error(
                    f"Error: {e}"
                )

# ==================================
# FOOTER
# ==================================

st.markdown("---")

st.caption(
    "🚀 Built with FastAPI • Streamlit • Google Gemini AI"
)