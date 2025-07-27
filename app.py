import streamlit as st
import openai
from fpdf import FPDF

# ✅ Set your API key here (for local testing only)
openai.api_key = st.secrets["OPENAI_API_KEY"]


st.set_page_config(page_title="Requirements Gathering Assistant")
st.title("📝 AI Requirements Gathering Assistant")
st.write("Generate User Stories, Acceptance Criteria, and a BRD Summary in seconds!")

# 📌 INPUT SECTION
st.subheader("Enter Project Details")

project_name = st.text_input("📌 Project Name")
project_desc = st.text_area("🖋️ Project Description")

industry_type = st.selectbox(
    "🏭 Industry Type",
    ["Logistics", "Healthcare", "E-commerce", "Finance", "Education", "Technology", "Manufacturing"]
)

methodology = st.selectbox(
    "📈 Preferred Methodology",
    ["Agile", "Scrum", "Waterfall", "Hybrid"]
)

technology_stack = st.selectbox(
    "💻 Preferred Technology",
    ["Salesforce", "SAP", "AWS", "Azure", "Custom Web App", "Mobile App"]
)

# 🚀 Generate Output
if st.button("Generate Requirements"):
    if not openai.api_key:
        st.error("❌ No API key found! Add it in app.py or secrets.toml")
    else:
        with st.spinner("Generating requirements..."):
            prompt = f"""
            Project Name: {project_name}
            Description: {project_desc}
            Industry: {industry_type}
            Methodology: {methodology}
            Technology Stack: {technology_stack}

            Generate:
            1. 3 user stories (As a ___, I want ___ so that ___)
            2. 3 acceptance criteria (Given-When-Then format)
            3. A short BRD summary including Objective, Scope, Stakeholders, Risks, 
               Industry-specific considerations, Preferred methodology, and Suggested technology stack.
            """

            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            output = response.choices[0].message.content
            st.session_state["generated_text"] = output
            st.success("✅ Requirements Generated!")
            st.write(output)

# 📥 PDF Download
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
