import streamlit as st
import openai
from fpdf import FPDF

st.set_page_config(page_title="AI BA Assistant", page_icon="🤖", layout="centered")
st.markdown(
    """
    <style>
        .top-left-logo {
            position: fixed;
            top: 10px;
            left: 10px;
            width: 50px;       /* Try reducing this to 40px or 30px */
            height: auto;
            object-fit: contain;  /* Ensures full logo is visible */
        }
    </style>
    <img class="top-left-logo" src="https://raw.githubusercontent.com/Ramanujamkv98/BA_Agent/refs/heads/main/DALL%C2%B7E%202025-07-27%2010.41.49%20-%20A%20professional%20and%20modern%20logo%20for%20a%20business%20intelligence%20assistant%20chatbot%2C%20incorporating%20the%20letters%20'BA'%20in%20a%20creative%20way.%20The%20design%20should%20look.webp">
    """,
    unsafe_allow_html=True
)



st.markdown(
    "<h1 style='text-align:center; color:white;'>📝 AI Business Analyst Assistant</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center; color:#ddd;'>Generate user stories, acceptance criteria, and BRD summaries based on selected methodology & technology.</p>",
    unsafe_allow_html=True
)



# --------- CUSTOM CSS for BLACK BACKGROUND + WHITE TEXT ----------
st.markdown("""
    <style>
        .stApp {
            background-color: #111111;
            color: #ffffff;
        }
        .title-text {
            font-size: 32px;
            font-weight: bold;
            text-align: center;
            padding: 10px;
            color: white;
        }
        .subtitle-text {
            text-align: center;
            font-size: 16px;
            color: #dddddd;
            margin-bottom: 20px;
        }
        .chat-box {
            background-color: #1e1e1e;
            border: 1px solid #333;
            border-radius: 12px;
            padding: 15px;
            margin-top: 20px;
            font-size: 16px;
            box-shadow: 0px 1px 3px rgba(0,0,0,0.2);
            color: #eeeeee;
        }
        .stButton button {
            width: 100%;
            font-size: 18px;
            border-radius: 10px;
            background-color: #10a37f;
            color: white;
            font-weight: bold;
        }
        .stTextInput > div > input,
        .stTextArea > div > textarea,
        .stSelectbox > div > div {
            background-color: #1e1e1e;
            color: #ffffff;
        }
    </style>
""", unsafe_allow_html=True)


# --------- INPUT SECTION ----------
project_name = st.text_input("📌 Project Name")
project_desc = st.text_area("🖋️ Project Description")

col1, col2, col3 = st.columns(3)

with col1:
    industry_type = st.selectbox("🏭 Industry", ["Logistics", "Healthcare", "E-commerce", "Finance", "Education", "Technology"])
with col2:
    methodology = st.selectbox("📈 Methodology", ["Agile", "Scrum", "Waterfall", "Hybrid"])
with col3:
    technology_stack = st.selectbox("💻 Technology", ["Salesforce", "SAP", "AWS", "Azure", "Custom Web App", "Mobile App"])

# --------- API KEY ---------
openai.api_key = st.secrets["OPENAI_API_KEY"]

# --------- GENERATE OUTPUT ----------
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

        # Fix encoding issue
        clean_text = st.session_state["generated_text"].encode("latin-1", "replace").decode("latin-1")
        pdf.multi_cell(0, 10, clean_text)

        pdf.output("requirements.pdf")

        with open("requirements.pdf", "rb") as file:
            st.download_button(
                label="📥 Click to Download PDF",
                data=file,
                file_name="requirements.pdf",
                mime="application/pdf"
            )
