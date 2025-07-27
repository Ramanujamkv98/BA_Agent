import streamlit as st
import openai
from fpdf import FPDF

st.set_page_config(page_title="AI BA Assistant", page_icon="🤖", layout="centered")

# --------- CUSTOM CSS (Dark Mode UI) ----------
st.markdown(
    f"""
    <div style="text-align:center; margin-bottom:10px;">
        <img src="https://raw.githubusercontent.com/Ramanujamkv98/BA_Agent/refs/heads/main/DALL%C2%B7E%202025-07-27%2011.03.59%20-%20A%20modern%20neon%20lights%20style%20logo%20design%20for%20a%20business%20intelligence%20assistant%20chatbot.%20The%20logo%20should%20feature%20a%20glowing%20chatbot%20icon%20with%20a%20speech%20bub.webp" style="width:80px; margin-bottom:10px;">
        <h1 style="color:white; font-size:36px;">📝 AI Business Analyst Assistant</h1>
        <p style="color:#ddd; font-size:16px;">
            Generate user stories, acceptance criteria, and BRD summaries based on selected methodology & technology.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)



# --------- INPUT FIELDS ----------
project_name = st.text_input("📌 Project Name")
project_desc = st.text_area("🖋️ Project Description")

col1, col2, col3 = st.columns(3)

with col1:
    industry_type = st.selectbox("🏭 Industry", ["Logistics", "Healthcare", "E-commerce", "Finance", "Education", "Technology"])

with col2:
    methodology = st.selectbox("📈 Preferred Methodology", ["Agile", "Scrum", "Waterfall", "Hybrid"])

with col3:
    technology_stack = st.selectbox("💻 Preferred Technology",
        ["Web App + Cloud Backend", "Mobile App + Cloud Backend", "Salesforce", "SAP", "Cloud Hosted Solution (AWS/Azure)"])

# --------- API KEY ---------
openai.api_key = st.secrets["OPENAI_API_KEY"]

# --------- GENERATE BUTTON ----------
if st.button("🚀 Generate Requirements"):
    with st.spinner("Generating best recommendations..."):
        prompt = f"""
        You are an expert Business Analyst. Evaluate the following project details:

        Project Name: {project_name}
        Description: {project_desc}
        Industry: {industry_type}
        Preferred Methodology (user selected): {methodology}
        Preferred Technology (user selected): {technology_stack}

        Your tasks:
        1. Based on the project description, decide if the chosen methodology ({methodology}) is the best fit. 
           - If yes, confirm it and explain why.
           - If no, suggest a better methodology and explain why it fits better.

        2. Evaluate if the selected technology ({technology_stack}) is the right choice. 
           - If yes, confirm and explain why.
           - If no, recommend a more suitable technology (e.g., Web App, Mobile App, Salesforce, SAP) 
             and explain why it's a better choice.

        3. Generate 3 user stories aligned with the **recommended methodology**.
        4. Generate 3 acceptance criteria using the **recommended methodology's format**.
        5. Provide a short BRD summary (Objective, Scope, Stakeholders, Risks).

        Always act as a decision-maker. If the user's choice is not ideal, clearly recommend the better option.
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
