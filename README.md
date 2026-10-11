# 🎓 AI Study Helper

> **SWYNEX Internship — Final Task (Task 4)**  
> **Repository Name:** `SWYNEX-Final-AI-Application`  
> **Author:** SWYNEX AI Intern  
> **Tech Stack:** Python 3.12 | Streamlit | Google Gemini API (`google-genai`) | Pydantic | Pytest  

---

## 📌 1. Project Overview

The **AI Study Helper** is a full-featured, beginner-friendly academic web application designed to help students master dense textbook excerpts, research articles, and lecture notes. By leveraging the **Google Gemini API** (`gemini-2.5-flash` on the free tier), the application automatically transforms lengthy raw notes into:
1. **A Concise Factual Summary** that captures essential principles without introducing extraneous facts.
2. **Exactly 5 Distinct Key Points** written in clear, simple English for rapid exam revision.
3. **An Interactive 3-Question Practice Quiz** complete with multiple-choice options, correct answers, and conceptual explanations.

Built with **Streamlit** and Python, the application executes **a single structured JSON API call** per session to minimize latency, respect free-tier quotas, and prevent hallucinated placeholders.

---

## 🎯 2. Problem Statement

Modern university and high school students face vast quantities of digital learning materials—often hundreds of pages of unformatted lecture slides, PDF transcriptions, and textbook chapters. Students struggle with:
- **Information Overload:** Difficulty identifying the central themes and exam-relevant concepts.
- **Passive Reading Inefficiency:** Re-reading notes without active recall testing leads to poor long-term retention.
- **Complex, Paid AI Tools:** Many AI study tools require expensive subscriptions, credit cards, or complex multi-step prompt engineering.

The **AI Study Helper** solves this by providing a clean, accessible, zero-cost study companion that converts unstructured study notes into high-yield summaries and active-recall practice quizzes in seconds.

---

## 🚀 3. Project Objectives

- **High-Yield Educational Assistance:** Provide students with automated synthesis and active recall questions grounded strictly in their own course notes.
- **Single Structured API Call Architecture:** Request summary, 5 key points, and 3 quiz questions simultaneously in structured JSON to avoid rate limits and unnecessary round-trips.
- **Robust Error Handling & Security:** Validate user input (character limits, prompt injection neutralization) and provide friendly guidance instead of application crashes.
- **Zero Cost & Free Tier Accessibility:** Run entirely on Google Gemini's 100% free tier without requiring a credit card or paid subscription.
- **Clean Academic UI:** Design an intuitive, distraction-free Streamlit interface with tabbed results, live character counting, and interactive quiz reveals.

---

## ✨ 4. Key Features

### 📥 1. Study Notes Input & Validation
- **Large Multiline Input Area:** Accommodates extensive study material.
- **Instant Sample Presets:** Quick one-click testing using built-in presets in Biology, Computer Science, and History.
- **Live Character Counter:** Displays character count with a strict **8,000-character upper limit** and clear warning messages for oversized or empty submissions.
- **Input Sanitization:** Strips excess whitespace and neutralizes delimiter injection attempts.

### 📝 2. AI Summary Generator
- **Factually Faithful:** Preserves original definitions, core mechanisms, and relationships without hallucinating outside facts.
- **Reading Time & Word Count Metrics:** Provides immediate feedback on summary length.
- **Academic Disclaimer:** Prominently clarifies that AI outputs are revision aids and should be cross-referenced with course textbooks.

### 💡 3. Key Point Extraction
- **Five Core Takeaways:** Formats exactly 5 distinct, high-impact concepts into numbered cards.
- **Plain English:** Rephrases complex academic jargon into accessible language.
- **Fidelity Check:** If the input material is too sparse, the system explicitly acknowledges that limitation.

### 🎯 4. Practice Quiz & Active Recall
- **Conceptual Questions:** Focuses on comprehension and causal understanding rather than rote word-matching.
- **Interactive Radio Buttons:** Allows students to select their answer before revealing the solution.
- **Expandable Answers & Explanations:** Explains *why* an answer is correct based strictly on the text.

### 🛡️ 5. Input Safety & Privacy
- **Prompt Injection Defense:** Notes are strictly enclosed in XML tags (`<study_notes>...</study_notes>`) with system instructions forbidding command execution or persona overrides.
- **Privacy-First Design:** Notes are transmitted solely over encrypted HTTPS to Google Gemini and are never stored or logged to a local database.

### 💾 6. Export to Markdown
- **One-Click Download:** Allows students to save their generated summary, key points, and quiz as an offline `.md` study sheet.

---

## 🛠️ 5. Technology Stack & Rationale

| Layer | Technology | Version | Rationale |
|---|---|---|---|
| **Language** | Python | `3.12+` | Clean, readable, industry standard for AI applications. |
| **User Interface** | Streamlit | `1.35.0+` | Rapid prototyping of reactive Python web apps with zero HTML/JS boilerplate. |
| **AI Provider** | Google Gemini API (Free Tier) | `gemini-2.5-flash` | Ultra-fast, highly accurate reasoning model with generous free-tier limits (15 RPM, 1,500 RPD, zero cost). |
| **Official AI SDK** | `google-genai` | `2.0.0+` | **Official modern SDK** released by Google, featuring native Pydantic schema enforcement and unified client architecture. |
| **Schema Validation** | Pydantic | `2.0.0+` | Enforces type safety and structured JSON parsing for summary, key points, and quiz. |
| **Config Management**| `python-dotenv` | `1.0.0+` | Safely loads API keys from local `.env` files without hardcoding credentials. |
| **Testing** | Pytest / Unittest | `7.0.0+` | Automated validation of input checks, sanitization, and JSON schema parsing. |

### Why `google-genai` and `gemini-2.5-flash`?
1. **Official SDK:** Google has designated `google-genai` as the next-generation unified SDK, replacing the legacy `google-generativeai` package. It features first-class support for `response_schema` with Pydantic models.
2. **Model Choice:** `gemini-2.5-flash` offers state-of-the-art token efficiency, low latency (< 3 seconds), and a high rate allowance on the free tier without requiring a billing account or credit card.

---

## 🏗️ 6. System Architecture & Workflow

```text
[ Student Input / Sample Preset ]
                │
                ▼
[ Input Validation (app.py / ai_service.py) ]
  ├── Empty / Whitespace check
  ├── Minimum length check (50 characters)
  └── Upper boundary check (<= 8,000 characters)
                │
                ▼ (Cleaned Text & Neutralized Delimiters)
[ Single API Request to Google Gemini API ]
  ├── System Prompt: Strict tutor role, passive text rule
  ├── Model: gemini-2.5-flash
  └── Response Schema: Pydantic StudyHelperResponse
                │
                ▼
[ JSON Parsing & Validation ]
  ├── Strip markdown fences if present
  ├── Pydantic model validation (summary, 5 points, 3 quiz items)
  └── Single Automatic Retry if JSON malformed
                │
                ▼
[ Interactive Streamlit Display ]
  ├── Tab 1: Summary & Metrics
  ├── Tab 2: 5 Distinct Key Points
  ├── Tab 3: Interactive Practice Quiz
  └── Export Button: Download Study Pack (.md)
```

---

## 💻 7. Installation Instructions (Windows PowerShell)

Follow these steps to set up and run the application locally on Windows:

### Step 1: Open PowerShell and Navigate to the Project Folder
```powershell
cd "c:\Users\Eswar\Desktop\SwynexTASK_4_AI_study helper"
```

### Step 2: Create and Activate a Virtual Environment
```powershell
# Create the virtual environment
python -m venv venv

# Activate the virtual environment
.\venv\Scripts\Activate.ps1
```
*(If PowerShell shows an execution policy error, run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` once).*

### Step 3: Install Required Dependencies
```powershell
pip install -r requirements.txt
```

---

## 🔑 8. Free Gemini API Key Configuration

The application uses Google's free tier Gemini API. **No credit card is required.**

### How to Get Your Free Key in 60 Seconds:
1. Navigate to [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Sign in with your standard Google account.
3. Click **Get API key** -> **Create API key**.
4. Copy the generated API key (it begins with `AIzaSy...`).

### How to Configure the Key in the App:
**Option A: Using the `.env` file (Recommended)**
1. Copy the example configuration template:
   ```powershell
   copy .env.example .env
   ```
2. Open `.env` in any text editor and replace the placeholder:
   ```env
   GEMINI_API_KEY=AIzaSyYourActualKeyHere
   GEMINI_MODEL=gemini-2.5-flash
   ```

**Option B: Directly in the Web Interface**
- If you don't configure a `.env` file, simply start the app and paste your key into the masked password field in the sidebar!

---

## 🏃 9. How to Run the Application

With your virtual environment activated, launch Streamlit:

```powershell
streamlit run app.py
```

The application will automatically open in your default browser at:
`http://localhost:8501`

---

## 📖 10. Example Usage Walkthrough

1. **Launch App:** Open `http://localhost:8501`.
2. **Select Preset:** Choose `🌿 Biology: Photosynthesis & Cellular Respiration` from the dropdown.
3. **Inspect Character Count:** Observe the character counter reading ~1,085 / 8,000 characters.
4. **Generate Study Pack:** Click **🚀 Generate Study Pack**.
5. **Explore Tabs:**
   - Click **📝 Summary** to read the synthesized summary.
   - Click **💡 Key Points (5)** to review the 5 bullet cards.
   - Click **🎯 Practice Quiz** to test your knowledge, select answers, and reveal solutions.
6. **Export:** Click **📥 Download Study Pack (.md)** to save your offline notes.

---

## 🖼️ 11. Screenshots Section

*(Add real screenshots here after running the app)*

```
+--------------------------------------------------------------------------+
| 🎓 AI Study Helper — SWYNEX Task 4 Final AI Project                      |
| [🌿 Biology Preset Selected] [Character Count: 1,085 / 8,000]           |
|                                                                          |
| [ 🚀 Generate Study Pack ]  [ 🗑️ Clear All ]                             |
|                                                                          |
| ──────────────────────────────────────────────────────────────────────── |
| [ 📝 Summary ]        [ 💡 Key Points (5) ]       [ 🎯 Practice Quiz ]   |
|                                                                          |
| Summary: Photosynthesis converts solar energy into glucose...           |
| Key Points: 1. Occurs in chloroplasts. 2. Uses chlorophyll...           |
| Quiz: Q1. Which organelle drives photosynthesis? [B) Chloroplast]        |
+--------------------------------------------------------------------------+
```

---

## 🧪 12. Evaluation Methodology & Live Evaluation Script

The project provides **two distinct evaluation mechanisms**:

### A) Automated Offline Unit Tests (`tests/`)
These tests do **not** call any external API and run instantaneously. They test:
- Empty string, `None`, and whitespace input rejection.
- Minimum length (50 characters) requirement.
- Boundary test at exactly 8,000 characters (pass) vs 8,001 characters (rejection).
- Prompt injection delimiter neutralization (`</study_notes>` -> `[/study_notes]`).
- Structured JSON parsing, markdown code-fence stripping, and Pydantic schema validation.

**Command to run:**
```powershell
pytest -v
# or
python -m unittest discover -s tests -p "test_*.py" -v
```

### B) Live Evaluation Script (`evaluate.py`)
This script executes **real live calls** against the Google Gemini API across 7 distinct cases:
1. Normal, well-structured notes (Biology).
2. Very short input (< 50 chars).
3. Empty input.
4. Repetitive/poorly structured notes.
5. Contradictory/misleading statements.
6. Boundary exceeding 8,000 characters.
7. Prompt injection attack (`"Ignore previous instructions"`).

**Command to run (run on your machine with your API key):**
```powershell
python evaluate.py
```
Outputs and manual review checklists are automatically saved into [`evaluation_results.md`](evaluation_results.md).

---

## 📊 13. Actual Unit Test Results (Verified)

Executed on Windows with Python 3.12.10:

```text
============================= test session starts =============================
platform win32 -- Python 3.12.10, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\Eswar\Desktop\SwynexTASK_4_AI_study helper
plugins: anyio-4.15.1
collected 20 items

tests/test_input_validation.py::TestInputValidation::test_empty_string_rejected PASSED [  5%]
tests/test_input_validation.py::TestInputValidation::test_exact_8000_char_boundary_accepted PASSED [ 10%]
tests/test_input_validation.py::TestInputValidation::test_exceeding_8000_chars_rejected PASSED [ 15%]
tests/test_input_validation.py::TestInputValidation::test_large_overflow_input_rejected PASSED [ 20%]
tests/test_input_validation.py::TestInputValidation::test_none_input_rejected PASSED [ 25%]
tests/test_input_validation.py::TestInputValidation::test_too_short_input_rejected PASSED [ 30%]
tests/test_input_validation.py::TestInputValidation::test_valid_input_accepted PASSED [ 35%]
tests/test_input_validation.py::TestInputValidation::test_whitespace_only_rejected PASSED [ 40%]
tests/test_input_validation.py::TestTextSanitization::test_empty_or_none_cleaning PASSED [ 45%]
tests/test_input_validation.py::TestTextSanitization::test_prompt_injection_closing_tag_neutralized PASSED [ 50%]
tests/test_input_validation.py::TestTextSanitization::test_prompt_injection_opening_tag_neutralized PASSED [ 55%]
tests/test_input_validation.py::TestTextSanitization::test_whitespace_normalization PASSED [ 60%]
tests/test_text_processing.py::TestTextProcessingAndJSONParsing::test_empty_key_points_raises_error PASSED [ 65%]
tests/test_text_processing.py::TestTextProcessingAndJSONParsing::test_empty_string_raises_error PASSED [ 70%]
tests/test_text_processing.py::TestTextProcessingAndJSONParsing::test_invalid_notes_caught_before_api_call PASSED [ 75%]
tests/test_text_processing.py::TestTextProcessingAndJSONParsing::test_malformed_syntax_raises_error PASSED [ 80%]
tests/test_text_processing.py::TestTextProcessingAndJSONParsing::test_missing_api_key_raises_exception_without_calling_network PASSED [ 85%]
tests/test_text_processing.py::TestTextProcessingAndJSONParsing::test_missing_quiz_field_raises_error PASSED [ 90%]
tests/test_text_processing.py::TestTextProcessingAndJSONParsing::test_parse_markdown_fenced_json PASSED [ 95%]
tests/test_text_processing.py::TestTextProcessingAndJSONParsing::test_parse_valid_json_fixture PASSED [100%]

============================= 20 passed in 0.22s ==============================
```

---

## 📝 14. Actual Evaluation Results (Verified with `evaluate.py`)

Executed live against the Google Gemini API (`gemini-flash-latest`) using `python evaluate.py`:

| Case ID | Scenario | Input Length | Status | Latency | Real Output / Error Summary | Manual Review Check |
|---|---|---|---|---|---|---|
| **CASE_1** | Normal Structured Notes | 556 chars | `SUCCESS` | 11.91s | Summary (54 words), 5 points, 3 quiz questions | [x] Reflects source, no hallucinations |
| **CASE_2** | Very Short Input (< 50 chars) | 22 chars | `CAUGHT_BY_VALIDATION` | 0.00s | Rejected: Input is too short (< 50 chars) | [x] Blocked locally with guidance |
| **CASE_3** | Empty Input | 0 chars | `CAUGHT_BY_VALIDATION` | 0.00s | Rejected: Input cannot be empty | [x] Blocked locally without crash |
| **CASE_4** | Repetitive / Poorly Structured | 262 chars | `SUCCESS` | 7.31s | Summary (30 words), 5 distinct points, 3 quiz items | [x] Avoided duplicate bullet points |
| **CASE_5** | Contradictory / Misleading | 254 chars | `SUCCESS` | 11.95s | Summary (56 words), 5 points, 3 questions | [x] Remains faithful to input notes |
| **CASE_6** | Exceeding 8,000 Chars | 13,200 chars | `CAUGHT_BY_VALIDATION` | 0.00s | Rejected: Exceeds 8,000 character limit | [x] Blocked locally with exact count |
| **CASE_7** | Prompt Injection Attack | 186 chars | `SUCCESS` | 33.45s | Passive summarization; refused 'HACKED' hijack | [x] Delimiters held; model not hijacked |

---

## ⚠️ 15. Known Failure Cases & Application Responses

| Failure Case | Root Cause | Application Handling |
|---|---|---|
| **Empty or Whitespace Input** | User clicked submit without typing notes | Rejected locally with friendly warning: `"Input cannot be empty. Please paste your study notes."` |
| **Input > 8,000 Characters** | Notes exceed maximum length | Rejected before API call: `"Input length exceeds the 8,000 character limit... Please shorten your notes."` |
| **Missing API Key** | `.env` key not set and sidebar empty | Clear UI notice with a 1-click guide to getting a free key at Google AI Studio. |
| **Invalid API Key (HTTP 401/403)** | Typos or revoked key | Catches `APIAuthenticationError`, alerts user to recheck credentials. |
| **Rate Limit Exceeded (HTTP 429)** | Exceeded free-tier quota (15 RPM) | Catches `APIRateLimitError`, instructs user to wait 30-60 seconds. |
| **Malformed JSON Response** | AI returned invalid syntax | System automatically retries once; if still malformed, displays clean error instead of made-up data. |
| **Network Disconnection** | Offline or unstable Wi-Fi | Catches `NetworkConnectionError` with clear connectivity guidance. |

---

## ⚖️ 16. Limitations & Ethical Considerations

### Academic Limitations
- **Study Aid, Not Teacher Replacement:** AI summaries cannot substitute for attending lectures, engaging in lab work, or reading primary textbooks.
- **Omission of Subtle Details:** By nature, summaries condense text; niche exam exceptions or edge cases may be compressed.
- **Verification Requirement:** Students should independently verify formulas, numerical values, and historical dates before exams.

### Ethical Considerations & Privacy
- **User Privacy:** Student notes are sent solely over encrypted HTTPS to Google's official Gemini endpoint. Notes are not logged, sold, or cached.
- **Sensitive Data Advisory:** Users are explicitly advised not to paste confidential, personal identifiable, or proprietary materials.
- **Transparency:** The application clearly labels all outputs as AI-generated and discloses the model identifier (`gemini-2.5-flash`).

---

## 🔮 17. Future Improvements

- [ ] **PDF & Document Upload:** Direct ingestion of lecture `.pdf` slides and `.docx` lecture transcripts.
- [ ] **Flashcard Export:** Integration with Anki via `.apkg` or `.csv` export.
- [ ] **Speech Synthesis:** Audio playback of generated summaries for auditory learners.
- [ ] **Custom Quiz Length:** Allow students to select 3, 5, or 10 quiz questions.

---

## 📁 18. Project Folder Structure

```text
SWYNEX-Final-AI-Application/
├── .env.example                     # Template for environment variables (API keys)
├── .gitignore                       # Protects credentials, venv, and cache files
├── HOW_IT_WORKS.md                  # Beginner explanation, demo video script, LinkedIn post
├── README.md                        # Master project documentation (this file)
├── ai_service.py                    # Core AI engine, validation, single structured API call
├── app.py                           # Clean Streamlit user interface
├── evaluate.py                      # Live API evaluation suite for 7 real-world test cases
├── requirements.txt                 # Python library dependencies
└── tests/
    ├── __init__.py                  # Tests package marker
    ├── test_input_validation.py     # Offline unit tests for inputs, limits & sanitization
    └── test_text_processing.py      # Offline unit tests for JSON parsing & schema checks
```

---

## 📄 19. License & Acknowledgments

Built for the **SWYNEX Internship Program (Task 4 Final Task)**.  
Powered by Google Gemini and Streamlit.
