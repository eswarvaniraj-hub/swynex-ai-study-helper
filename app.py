"""
AI Study Helper - Main Streamlit Application
SWYNEX Internship Task 4 Final AI Project

A clean, responsive, and academic study companion that transforms lengthy study
notes into concise summaries, 5 key points, and 3 practice quiz questions using
a single structured call to Google Gemini.
"""

import os
import streamlit as st
from dotenv import load_dotenv

# Import our modular AI service and data models
from ai_service import (
    generate_study_materials,
    validate_notes,
    MAX_INPUT_CHARS,
    MIN_INPUT_CHARS,
    DEFAULT_MODEL,
    StudyHelperResponse,
    AIStudyHelperError,
    MissingAPIKeyError,
    InputValidationError,
    APIAuthenticationError,
    APIRateLimitError,
    MalformedResponseError,
    NetworkConnectionError,
)

# Load environment variables
load_dotenv()

# ==============================================================================
# SAMPLE STUDY NOTES PRESETS (FOR IMMEDIATE ONE-CLICK TESTING)
# ==============================================================================
SAMPLE_NOTES = {
    "Select a sample preset...": "",
    "🌿 Biology: Photosynthesis & Cellular Respiration": (
        "Photosynthesis is the biochemical process by which green plants, algae, and some bacteria "
        "convert light energy into chemical energy stored in glucose. The process takes place inside "
        "chloroplasts, primarily within the thylakoid membranes and stroma. The green pigment chlorophyll "
        "absorbs blue and red light while reflecting green light.\n\n"
        "The overall chemical equation is:\n"
        "6CO2 + 6H2O + light energy -> C6H12O6 + 6O2\n\n"
        "Photosynthesis occurs in two stages:\n"
        "1. Light-Dependent Reactions: Occur in the thylakoid membranes. Solar energy splits water molecules (photolysis), "
        "releasing oxygen as a byproduct and generating ATP and NADPH.\n"
        "2. Light-Independent Reactions (Calvin Cycle): Occur in the stroma. ATP and NADPH are consumed to fix carbon dioxide "
        "into glyceraldehyde-3-phosphate (G3P), which is subsequently synthesized into glucose.\n\n"
        "In contrast, cellular respiration is the complementary process occurring in mitochondria where glucose is broken down "
        "in the presence of oxygen to release ATP, carbon dioxide, and water. Together, photosynthesis and cellular respiration "
        "drive the planetary carbon and oxygen cycles."
    ),
    "💻 Computer Science: Operating Systems & CPU Scheduling": (
        "An Operating System (OS) is system software that manages computer hardware and software resources and provides common "
        "services for computer programs. A central responsibility of the OS kernel is Process Management.\n\n"
        "A process is a program in execution, consisting of program code, current activity, program counter, registers, stack, and heap. "
        "Processes transition through several distinct states during their life cycle: New, Ready, Running, Waiting (Blocked), and Terminated.\n\n"
        "CPU Scheduling is the process by which the OS scheduler allocates the CPU core among ready processes to maximize CPU utilization "
        "and minimize turnaround and waiting times. Major scheduling algorithms include:\n"
        "1. First-Come, First-Served (FCFS): Non-preemptive, simple, but suffers from the convoy effect.\n"
        "2. Shortest Job First (SJF): Optimal average waiting time, but difficult to predict future burst times and risks starvation.\n"
        "3. Round Robin (RR): Preemptive, assigns fixed time quanta to each process in circular order; ideal for interactive time-sharing systems.\n"
        "4. Priority Scheduling: Allocates CPU based on priority; susceptible to indefinite starvation, solved by aging techniques."
    ),
    "🏛️ History: The Industrial Revolution": (
        "The Industrial Revolution marked a profound transition from agrarian, handicraft economies to ones dominated by industry and "
        "machine manufacturing. It began in Great Britain during the mid-18th century (approximately 1760 to 1840) before spreading across "
        "Europe and North America.\n\n"
        "Key Catalysts:\n"
        "1. Abundant natural resources: Britain possessed vast reserves of coal and iron ore, alongside an extensive network of navigable rivers and canals.\n"
        "2. Technological breakthroughs: James Watt's improved steam engine provided reliable mechanical power. The spinning jenny and power loom "
        "revolutionized textile production.\n"
        "3. Capital and colonial trade: Expanding global trade networks provided raw materials (such as raw cotton) and captive markets for manufactured goods.\n\n"
        "Consequences:\n"
        "The revolution spurred rapid urbanization as millions migrated from rural villages into crowded industrial cities like Manchester and Birmingham. "
        "While it vastly increased productivity and long-term living standards, early decades brought harsh working conditions, 14-hour workdays, "
        "child labor, and severe environmental pollution, which eventually gave rise to trade unions and labor legislation."
    ),
}

# ==============================================================================
# STREAMLIT PAGE CONFIGURATION & ACADEMIC STYLING
# ==============================================================================
st.set_page_config(
    page_title="AI Study Helper | SWYNEX Final Task",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom styling for a clean, professional academic aesthetic
st.markdown(
    """
    <style>
    /* Main container clean spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }
    
    /* Academic header banner */
    .header-box {
        background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 50%, #3b82f6 100%);
        color: white;
        padding: 1.8rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .header-box h1 {
        color: #ffffff !important;
        margin: 0;
        font-size: 2.1rem;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    .header-box p {
        color: #e0e7ff !important;
        margin-top: 0.5rem;
        margin-bottom: 0;
        font-size: 1.05rem;
    }

    /* Subtitle and badge */
    .badge {
        display: inline-block;
        background-color: rgba(255, 255, 255, 0.2);
        color: #ffffff;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 0.2rem 0.6rem;
        border-radius: 9999px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }

    /* Academic card styling */
    .academic-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.3rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    /* Key points numbered cards */
    .point-card {
        background-color: #ffffff;
        border-left: 4px solid #2563eb;
        border-top: 1px solid #e2e8f0;
        border-right: 1px solid #e2e8f0;
        border-bottom: 1px solid #e2e8f0;
        border-radius: 6px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
    }

    /* Quiz card styling */
    .quiz-card {
        background-color: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 8px;
        padding: 1.2rem;
        margin-bottom: 1.2rem;
    }
    .quiz-title {
        font-weight: 700;
        font-size: 1.05rem;
        color: #1e293b;
        margin-bottom: 0.75rem;
    }

    /* Disclaimer alert */
    .disclaimer-box {
        background-color: #fffbeb;
        border-left: 4px solid #f59e0b;
        color: #92400e;
        padding: 0.75rem 1rem;
        border-radius: 4px;
        font-size: 0.88rem;
        margin-bottom: 1.2rem;
    }
    
    /* Footer */
    .footer-text {
        text-align: center;
        color: #64748b;
        font-size: 0.85rem;
        margin-top: 3rem;
        border-top: 1px solid #e2e8f0;
        padding-top: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==============================================================================
# SESSION STATE INITIALIZATION
# ==============================================================================
if "study_notes" not in st.session_state:
    st.session_state.study_notes = ""
if "study_results" not in st.session_state:
    st.session_state.study_results = None
if "selected_preset" not in st.session_state:
    st.session_state.selected_preset = "Select a sample preset..."


# ==============================================================================
# SIDEBAR: CONFIGURATION, PRIVACY & GUIDE
# ==============================================================================
with st.sidebar:
    st.markdown("### 🎓 Project Information")
    st.caption("**SWYNEX AI Internship — Task 4 Final Task**")
    st.caption("**Project:** AI Study Helper")
    st.caption("**Provider:** Google Gemini API (Free Tier)")

    st.markdown("---")
    st.markdown("### 🔑 API Configuration")

    env_api_key = os.getenv("GEMINI_API_KEY", "").strip()

    if env_api_key:
        st.success("API key loaded from `.env` file", icon="✅")
        active_api_key = env_api_key
    else:
        st.info("No API key detected in `.env`. Enter one below for this session:", icon="ℹ️")
        user_entered_key = st.text_input(
            "Gemini API Key",
            type="password",
            placeholder="AIzaSy...",
            help="Your key is never logged or saved to disk. It lives only in session memory.",
        )
        active_api_key = user_entered_key.strip()

    # Model selector
    selected_model = st.selectbox(
        "AI Model",
        options=["gemini-2.5-flash", "gemini-1.5-flash"],
        index=0,
        help="gemini-2.5-flash is Google's modern, ultra-fast model with generous free-tier quotas.",
    )

    with st.expander("❓ How to get a free Gemini API key"):
        st.markdown(
            """
            1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey).
            2. Sign in with your Google account.
            3. Click **Get API key** -> **Create API key**.
            4. Copy your key and either:
               - Paste it into the `.env` file (`GEMINI_API_KEY=your_key`)
               - Or paste it directly in the box above!
            *(100% Free: No credit card required!)*
            """
        )

    st.markdown("---")
    st.markdown("### 🔒 Privacy & Safety Notice")
    st.caption(
        "• Your notes are sent directly to the official Google Gemini API via encrypted HTTPS.\n"
        "• This application does not store, log, or database your study notes.\n"
        "• **Please avoid submitting confidential, proprietary, or personal private data.**"
    )

    st.markdown("---")
    st.markdown("### ⚖️ Academic Integrity")
    st.caption(
        "This tool is designed as an educational revision aid. It summarizes and creates quizzes "
        "based strictly on provided materials. Always cross-reference definitions and exam materials "
        "with your primary textbooks and instructor guidelines."
    )


# ==============================================================================
# MAIN PAGE HEADER
# ==============================================================================
st.markdown(
    """
    <div class="header-box">
        <span class="badge">SWYNEX Final AI Project</span>
        <h1>AI Study Helper</h1>
        <p>Transform lengthy study notes into concise summaries, 5 key points, and practice quizzes in seconds.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Disclaimer banner required by Core Feature 2 & 9
st.markdown(
    """
    <div class="disclaimer-box">
        ⚠️ <strong>Academic Notice:</strong> AI-generated summaries and quizzes are study aids. 
        While designed to be faithful to your input, they may occasionally contain inaccuracies. 
        Always verify critical exam formulas and concepts with course textbooks.
    </div>
    """,
    unsafe_allow_html=True,
)


# ==============================================================================
# INPUT SECTION
# ==============================================================================
st.markdown("### 📥 1. Provide Your Study Notes")

# Sample Preset Loader (Core Feature 1)
def on_preset_change():
    chosen = st.session_state.preset_selector
    if chosen and chosen in SAMPLE_NOTES and SAMPLE_NOTES[chosen]:
        st.session_state.study_notes = SAMPLE_NOTES[chosen]


selected_preset = st.selectbox(
    "💡 Want to test immediately? Load a sample topic:",
    options=list(SAMPLE_NOTES.keys()),
    index=0,
    key="preset_selector",
    on_change=on_preset_change,
)

# Text Area for Notes
notes_input = st.text_area(
    label="Paste your textbook excerpts, lecture notes, or study material below:",
    value=st.session_state.study_notes,
    height=240,
    placeholder="Paste up to 8,000 characters of lecture notes or textbook material here...",
    key="notes_text_area",
)

# Update session state with current text area value
st.session_state.study_notes = notes_input

# Live Character Counter (Core Feature 1: Max 8,000 chars)
char_count = len(notes_input)
is_over_limit = char_count > MAX_INPUT_CHARS

col_count, col_status = st.columns([1, 1])
with col_count:
    if is_over_limit:
        st.error(
            f"❌ **Character count:** {char_count:,} / {MAX_INPUT_CHARS:,} characters. "
            f"(Please shorten by {char_count - MAX_INPUT_CHARS:,} characters)"
        )
    else:
        st.caption(f"📊 **Character count:** {char_count:,} / {MAX_INPUT_CHARS:,} characters")

with col_status:
    if char_count > 0 and char_count < MIN_INPUT_CHARS:
        st.warning(f"⚠️ Minimum recommended: {MIN_INPUT_CHARS} characters for a useful summary.")
    elif char_count >= MIN_INPUT_CHARS and not is_over_limit:
        st.success("✅ Notes length is within acceptable bounds.", icon="✨")


# ==============================================================================
# ACTION BUTTONS (GENERATE & CLEAR)
# ==============================================================================
col_btn_generate, col_btn_clear, col_btn_spacer = st.columns([2, 1, 3])

with col_btn_generate:
    generate_clicked = st.button(
        "🚀 Generate Study Pack",
        type="primary",
        use_container_width=True,
        disabled=is_over_limit,
    )

with col_btn_clear:
    if st.button("🗑️ Clear All", use_container_width=True):
        st.session_state.study_notes = ""
        st.session_state.study_results = None
        st.rerun()


# ==============================================================================
# GENERATION PROCESSING
# ==============================================================================
if generate_clicked:
    # 1. Validate API Key Presence
    if not active_api_key:
        st.error(
            "🔑 **Gemini API Key Required:** Please configure `GEMINI_API_KEY` in your `.env` file, "
            "or enter your free key in the sidebar.",
            icon="🚨",
        )
    else:
        # 2. Validate input
        is_valid, validation_msg = validate_notes(notes_input)
        if not is_valid:
            st.error(f"⚠️ **Validation Error:** {validation_msg}", icon="❌")
        else:
            # 3. Call AI Service with spinner
            with st.spinner("🧠 Analyzing notes with Gemini AI... generating summary, 5 key points, and quiz..."):
                try:
                    result: StudyHelperResponse = generate_study_materials(
                        notes=notes_input,
                        api_key=active_api_key,
                        model_name=selected_model,
                    )
                    st.session_state.study_results = result
                    st.success("🎉 Study pack successfully generated!", icon="✅")

                except MissingAPIKeyError as e:
                    st.error(f"🔑 **Missing Credentials:** {str(e)}", icon="🚨")
                except InputValidationError as e:
                    st.error(f"⚠️ **Input Error:** {str(e)}", icon="❌")
                except APIAuthenticationError as e:
                    st.error(f"🔒 **Authentication Failed:** {str(e)}", icon="🚫")
                except APIRateLimitError as e:
                    st.warning(f"⏳ **Rate Limit Exceeded:** {str(e)}", icon="⏱️")
                except MalformedResponseError as e:
                    st.error(f"🧩 **Response Error:** {str(e)}", icon="⚠️")
                except NetworkConnectionError as e:
                    st.error(f"🌐 **Network Issue:** {str(e)}", icon="📡")
                except AIStudyHelperError as e:
                    st.error(f"❌ **Error:** {str(e)}")
                except Exception as e:
                    st.error(f"❌ **Unexpected Error:** {str(e)}")


# ==============================================================================
# RESULTS DISPLAY (TABS: SUMMARY, KEY POINTS, QUIZ)
# ==============================================================================
if st.session_state.study_results is not None:
    results: StudyHelperResponse = st.session_state.study_results

    st.markdown("---")
    st.markdown("### 📚 2. Your Generated Study Pack")

    tab_summary, tab_key_points, tab_quiz = st.tabs(
        ["📝 Summary", "💡 Key Points (5)", "🎯 Practice Quiz (3 Questions)"]
    )

    # --------------------------------------------------------------------------
    # TAB 1: SUMMARY
    # --------------------------------------------------------------------------
    with tab_summary:
        st.markdown("#### 📝 Concise Study Summary")
        st.markdown(
            f"""
            <div class="academic-card">
                <p style="font-size: 1.05rem; line-height: 1.7; color: #1e293b; margin: 0;">
                    {results.summary}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        word_count = len(results.summary.split())
        col_w, col_t = st.columns([1, 1])
        with col_w:
            st.caption(f"📏 **Summary length:** {word_count} words")
        with col_t:
            st.caption(f"⏱️ **Estimated reading time:** ~{max(1, word_count // 130)} min")

    # --------------------------------------------------------------------------
    # TAB 2: KEY POINTS
    # --------------------------------------------------------------------------
    with tab_key_points:
        st.markdown("#### 💡 5 Core Academic Points")
        st.caption("Extracted high-yield concepts to review before examinations:")

        for idx, point in enumerate(results.key_points, 1):
            st.markdown(
                f"""
                <div class="point-card">
                    <span style="font-weight: 700; color: #2563eb; margin-right: 8px;">Point {idx}:</span>
                    <span style="color: #1e293b; font-size: 0.98rem;">{point}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # --------------------------------------------------------------------------
    # TAB 3: PRACTICE QUIZ
    # --------------------------------------------------------------------------
    with tab_quiz:
        st.markdown("#### 🎯 Practice Quiz")
        st.caption("Test your conceptual understanding. Try answering each question before checking the solution:")

        for q_idx, q in enumerate(results.quiz, 1):
            with st.container():
                st.markdown(f"**Question {q_idx}: {q.question}**")

                # Interactive Option Radio Button for Self-Testing
                option_choice = st.radio(
                    label=f"Choose your answer for Question {q_idx}:",
                    options=q.options,
                    index=None,
                    key=f"quiz_radio_{q_idx}",
                    label_visibility="collapsed",
                )

                # Expandable Solution
                with st.expander(f"🔍 Reveal Answer & Explanation for Question {q_idx}"):
                    st.markdown(f"**Correct Answer:** `{q.correct_answer}`")
                    st.markdown(f"**Explanation:** {q.explanation}")

                st.markdown("---")

    # --------------------------------------------------------------------------
    # EXPORT STUDY PACK AS MARKDOWN
    # --------------------------------------------------------------------------
    export_markdown = f"""# AI Study Helper - Generated Study Pack

## Summary
{results.summary}

## 5 Key Points
"""
    for idx, pt in enumerate(results.key_points, 1):
        export_markdown += f"{idx}. {pt}\n"

    export_markdown += "\n## Practice Quiz\n"
    for idx, q in enumerate(results.quiz, 1):
        export_markdown += f"\n### Question {idx}: {q.question}\n"
        for opt in q.options:
            export_markdown += f"- {opt}\n"
        export_markdown += f"\n**Correct Answer:** {q.correct_answer}\n"
        export_markdown += f"**Explanation:** {q.explanation}\n"

    st.download_button(
        label="📥 Download Study Pack (.md)",
        data=export_markdown,
        file_name="study_pack.md",
        mime="text/markdown",
        help="Export this summary, key points, and quiz to an offline Markdown study file.",
    )


# ==============================================================================
# FOOTER
# ==============================================================================
st.markdown(
    """
    <div class="footer-text">
        AI Study Helper — Built with Streamlit & Google Gemini API for SWYNEX Internship Task 4 Final Task.
    </div>
    """,
    unsafe_allow_html=True,
)
