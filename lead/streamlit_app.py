import streamlit as st
import asyncio
import threading
from datetime import datetime
import time
from crew import LeadGeneration
from dotenv import load_dotenv
import os
import re

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Lead Generation AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for improved contrast and modern look
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .subtitle {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .input-section {
        background: none !important;
        padding: 1.5rem 0 1.5rem 0;
        border-radius: 0;
        margin-bottom: 2rem;
        box-shadow: none !important;
        border: none !important;
    }
    .results-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-top: 2rem;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    }
    .metric-card {
        background: none !important;
        padding: 1.5rem 0 1.5rem 0;
        border-radius: 0;
        text-align: center;
        box-shadow: none !important;
        backdrop-filter: none !important;
    }
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    .block-container {
        padding-top: 2rem;
    }
    /* DARK THEME for text inputs and text areas */
    .stTextInput > div > div > input {
        background: #222 !important;
        color: #fff !important;
        border: 2px solid rgba(102, 126, 234, 0.25);
        border-radius: 10px;
        padding: 0.75rem;
        transition: all 0.3s ease;
        font-size: 1.05rem;
    }
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.18);
        color: #fff !important;
    }
    .stTextArea > div > div > textarea {
        background: #222 !important;
        color: #fff !important;
        border: 2px solid rgba(102, 126, 234, 0.25);
        border-radius: 10px;
        font-size: 1.05rem;
        backdrop-filter: none;
    }
    /* Hide Streamlit's default white card backgrounds */
    section[data-testid="stSidebar"] > div:first-child {
        background: none !important;
    }
    .main .block-container {
        background: none !important;
    }
</style>
""", unsafe_allow_html=True)

def check_api_keys():
    serper_key = os.getenv("SERPER_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")
    missing_keys = []
    if not serper_key:
        missing_keys.append("SERPER_API_KEY")
    if not gemini_key:
        missing_keys.append("GEMINI_API_KEY")
    return missing_keys

def run_crew_analysis(customer_name, target_industry):
    try:
        inputs = {
            'customer_name_or_business': customer_name,
            'target_industry': target_industry
        }
        lead_gen = LeadGeneration()
        results = lead_gen.crew().kickoff(inputs=inputs)
        return results, None
    except Exception as e:
        return None, str(e)

def extract_fit_score_from_results(results):
    if not results:
        return None, None
    text = results.raw if hasattr(results, 'raw') else str(results)
    match = re.search(r'Fit Score:\s*(\d+)\s*\((\w+)\)', text)
    if match:
        return int(match.group(1)), match.group(2).capitalize()
    match2 = re.search(r'"score"\s*:\s*(\d+)[^\n]+"fit"\s*:\s*"(\w+)"', text)
    if match2:
        return int(match2.group(1)), match2.group(2).capitalize()
    return None, None

def main():
    st.markdown('<h1 class="subtitle">Powered by CrewAI - Intelligent Lead Discovery & Analysis</h1>', unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("### 🔧 Configuration")
        missing_keys = check_api_keys()
        if missing_keys:
            st.error(f"⚠️ Missing API Keys: {', '.join(missing_keys)}")
            st.markdown("""
            **Setup Required:**
            1. Create a `.env` file in your project directory
            2. Add your API keys:
               - `SERPER_API_KEY=your_key_here`
               - `GEMINI_API_KEY=your_key_here`
            """)
        else:
            st.success("✅ All API keys configured")
        st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown('<div class="input-section">', unsafe_allow_html=True)
        st.markdown("### 🔍 Lead Search Parameters")
        customer_name = st.text_input(
            "Customer Name or Business",
            placeholder="e.g., John Smith, Acme Corporation, TechStart Inc.",
            help="Enter the name of the person or company you want to research"
        )
        target_industry = st.text_input(
            "Target Industry",
            value=st.session_state.get('target_industry', ''),
            placeholder="e.g., Technology, Healthcare, Finance",
            help="Specify the industry you're targeting for lead qualification"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            analyze_button = st.button(
                "🚀 Start Lead Analysis",
                disabled=not customer_name or not target_industry or bool(missing_keys),
                use_container_width=True
            )
    with col2:
        # Make Analysis Process a heading, not a box
        st.markdown("<h2 style='color:#764ba2;font-weight:800;letter-spacing:1px;text-align:left;margin-bottom:1rem;'>Analysis Process</h2>", unsafe_allow_html=True)
        process_steps = [
            "🔍 Search public information",
            "📊 Extract key details",
            "⚖️ Evaluate lead potential",
            "📝 Generate summary report"
        ]
        for step in process_steps:
            st.markdown(f"- {step}")
        st.markdown("---")
        st.markdown("### ⏱️ Estimated Time")
        st.info("2-3 minutes per analysis")
    if analyze_button and customer_name and target_industry:
        if missing_keys:
            st.error("Please configure your API keys before running the analysis.")
            return
        st.markdown("---")
        st.markdown("## 🔄 Analysis in Progress")
        progress_bar = st.progress(0)
        status_text = st.empty()
        progress_steps = [
            (25, "🔍 Searching for public information..."),
            (50, "📊 Extracting key details..."),
            (75, "⚖️ Evaluating lead potential..."),
            (90, "📝 Generating summary report..."),
            (100, "✅ Analysis complete!")
        ]
        results_placeholder = st.empty()
        with st.spinner("Initializing AI agents..."):
            time.sleep(1)
        for progress, message in progress_steps:
            status_text.text(message)
            progress_bar.progress(progress)
            time.sleep(0.5)
        with st.spinner("Running CrewAI analysis..."):
            results, error = run_crew_analysis(customer_name, target_industry)
        if error:
            st.error(f"❌ Analysis failed: {error}")
        else:
            progress_bar.empty()
            status_text.empty()
            st.markdown('<div class="results-section">', unsafe_allow_html=True)
            st.markdown("## 📊 Lead Analysis Results")
            fit_score, fit_level = extract_fit_score_from_results(results)
            if fit_score is not None and fit_level is not None:
                fit_color = {
                    "High": "#43e97b",
                    "Medium": "#ffbe30",
                    "Low": "#ff3576"
                }.get(fit_level, "#888")
                fit_bg = {
                    "High": "linear-gradient(90deg, #11998e 0%, #38ef7d 100%)",
                    "Medium": "linear-gradient(90deg, #ffb347 0%, #ffcc33 100%)",
                    "Low": "linear-gradient(90deg, #ff3576 0%, #ff6036 100%)"
                }.get(fit_level, "#333")
                st.markdown(f"""
                <div style='display: flex; align-items: center; justify-content: center; margin-bottom: 1.5rem;'>
                    <div style='background: {fit_bg}; color: #fff; border-radius: 2rem; padding: 1.5rem 3.5rem; box-shadow: 0 4px 24px rgba(0,0,0,0.12); font-size: 2.3rem; font-weight: 800; letter-spacing: 2px; text-shadow: 0 2px 8px rgba(0,0,0,0.15);'>
                        Fit Score: <span style='color: #fff;'>{fit_score} ({fit_level})</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            tab1, tab2, tab3 = st.tabs(["📋 Summary", "📄 Full Report", "📁 Export"])
            with tab1:
                st.markdown("### Lead Summary")
                if hasattr(results, 'raw'):
                    st.text_area("Results", results.raw, height=300, key="summary_results")
                else:
                    st.text_area("Results", str(results), height=300, key="summary_results")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                    st.metric("Analysis Date", datetime.now().strftime("%Y-%m-%d"))
                    st.markdown('</div>', unsafe_allow_html=True)
                with col2:
                    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                    st.metric("Target Industry", target_industry)
                    st.markdown('</div>', unsafe_allow_html=True)
                with col3:
                    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
                    st.metric("Status", "✅ Complete")
                    st.markdown('</div>', unsafe_allow_html=True)
            with tab2:
                st.markdown("### Detailed Report")
                try:
                    with open("lead_report.md", "r") as f:
                        report_content = f.read()
                    st.markdown(report_content)
                except FileNotFoundError:
                    st.info("Detailed report file not found. Showing raw results:")
                    if hasattr(results, 'raw'):
                        st.code(results.raw, language='markdown')
                    else:
                        st.code(str(results), language='markdown')
            with tab3:
                st.markdown("### Export Options")
                if hasattr(results, 'raw'):
                    result_text = results.raw
                else:
                    result_text = str(results)
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        label="📥 Download as Text",
                        data=result_text,
                        file_name=f"lead_analysis_{customer_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                with col2:
                    try:
                        with open("lead_report.md", "r") as f:
                            report_content = f.read()
                        st.download_button(
                            label="📥 Download Report (MD)",
                            data=report_content,
                            file_name=f"lead_report_{customer_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                            mime="text/markdown",
                            use_container_width=True
                        )
                    except FileNotFoundError:
                        st.info("Markdown report not available")
            st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; padding: 2rem;'>
            🤖 Powered by CrewAI | 🎯 Lead Generation AI Assistant<br>
            <small>Built with Streamlit • Enhanced with AI Agents</small>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    if 'target_industry' not in st.session_state:
        st.session_state.target_industry = ''
    main()
