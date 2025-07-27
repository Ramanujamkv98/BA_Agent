import streamlit as st
import openai
from fpdf import FPDF

st.set_page_config(page_title="AI BA Assistant", page_icon="🤖", layout="centered")

# --------- CUSTOM CSS (ChatGPT-like UI) ----------
st.markdown("""
    <style>
        .stApp {
            background-color: #f7f7f8;
            font-family: "Segoe UI", sans-serif;
        }
        .title-text {
            font-size: 32px;
            font-weight: bold;
            text-align: center;
            padding: 10px;
        }
        .chat-box {
            background-color: #ffffff;
            border: 1px solid #ddd;
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 15px;
            font-size: 16px;
            box-shadow: 0px 1px 3px rgba(0,0,0,0.1);
        }
        .stButton button {
            width: 100%;
            font-size: 18px;
            border-radius: 10px;
            background-color: #10a37f;
            color: white;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# --------- PAGE TITLE ----------
st.markdown('<p class="title-text">📝 AI Business Analyst Assistant</p>', unsafe_allow_html=True)
st.write("Generate **user stories, acceptance criteria, and BRD summaries** based on methodology & technology.")

# --------- INPUTS ----------
project_name = st.text_input("📌 Project Name")
project_desc = st.text_area("🖋️ Project Description")

col1, col2, col3 = st.columns(3)

with col1:
    industry_type = st.selectbox("🏭 Industry", ["Logistics", "Healthcare", "E-commerce", "Finance", "Education", "Technology"])

with col2:
    methodology = st.selectbox("📈 Methodology", ["Agile", "Scrum", "Waterfall", "Hybrid"])

with col3:
    technology_stack = st.selectbox("💻 Technology", ["Salesforce", "SAP", "AWS", "Azure", "Custom Web App", "Mobile App"])

openai.api_key = st.secrets["OPENAI_API_KEY"]

# --------- GENERATE BUTTON ----------
if st.button("🚀 Generate Requirements"):
    with st.spinner("Generating requirements..."):
        prompt = f"""
        Project Name: {project_name}
        Description: {project_desc}
        Industry: {industry_type}
        Methodology: {methodology}
        Technology Stack: {technology_stack}

        Generate:
        1. 3 user stories aligned with {methodology} principles.
        2. 3 acceptance criteria in {methodology}-appropriate format.
        3. A BRD summary including Objective, Scope, Stakeholders, Risks.
        4. A short explanation of why {methodology} is ideal for this project.
        5. A short explanation of why {technology_stack} is suitable for this solution.
        """

        try:
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            output = response.choices[0].message.content
            st.session_state["generated_text"] = output

            st.markdown(f'<div class="chat-box">{output}</div>', unsafe_allow_html=True)

        except Exception as e:
            st.error(f"⚠️ Error: {e}")

# --------- PDF DOWNLOAD ----------
if "generated_text" in st.session_state:
    if st.button("📄 Download as PDF"):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, st.session_state["generated_text"])
        pdf.output("requirements.pdf")

        with open("requirements.pdf", "rb") as file:
            st.download_button(
                label="📥 Click to Download PDF",
                data=file,
                file_name="requirements.pdf",
                mime="application/pdf"
            )
