import streamlit as st
from fpdf import FPDF
import openai

# Set page configuration
st.set_page_config(page_title="AI Business Analyst Assistant", page_icon="📝", layout="centered")

# Load OpenAI API key from secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Add logo above the title
# Centered logo above the title
st.markdown(
    """
    <div style='text-align: center;'>
        <img src='https://raw.githubusercontent.com/Ramanujamkv98/BA_Agent/refs/heads/main/DALL%C2%B7E%202025-07-27%2011.03.59%20-%20A%20modern%20neon%20lights%20style%20logo%20design%20for%20a%20business%20intelligence%20assistant%20chatbot.%20The%20logo%20should%20feature%20a%20glowing%20chatbot%20icon%20with%20a%20speech%20bub.webp' width='120'>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align: center; color: white;'>Generate user stories, acceptance criteria, and BRD summaries with smart technology recommendations.</p>",
    unsafe_allow_html=True
)

# Input fields
project_name = st.text_input("📌 Project Name")
project_description = st.text_area("🖋 Project Description")

industry = st.selectbox("🏢 Industry", ["Logistics", "Finance", "Education", "Healthcare", "Retail"])
methodology = st.selectbox("📈 Methodology", ["Agile", "Waterfall", "Scrum", "Kanban"])
technology = st.selectbox(
    "💻 Technology",
    ["Web App + Cloud Backend", "Mobile App + Cloud Backend", "Salesforce Experience Cloud", "SAP"]
)

# Function to generate requirements
def generate_requirements(name, description, industry, methodology, technology):
    prompt = f"""
    Project Name: {name}
    Description: {description}
    Industry: {industry}
    Methodology: {methodology}
    Technology: {technology}

    1. Generate 3 clear user stories.
    2. Write acceptance criteria for these user stories.
    3. Provide a BRD summary.
    4. Evaluate if the selected technology is the right fit for this project.
       - If yes, explain why (mention capabilities like workflows, integrations, scalability).
       - If no, suggest a better alternative and explain why.
    """

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


# Generate button
if st.button("🚀 Generate Requirements"):
    if project_name and project_description:
        with st.spinner("Generating requirements..."):
            output = generate_requirements(project_name, project_description, industry, methodology, technology)
            st.session_state["generated_text"] = output
            st.success("✅ Requirements Generated!")
            st.markdown(output)

# PDF download
if "generated_text" in st.session_state:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, st.session_state["generated_text"].encode("latin-1", "replace").decode("latin-1"))
    pdf.output("requirements.pdf")

    with open("requirements.pdf", "rb") as file:
        st.download_button("📄 Download as PDF", file, "requirements.pdf", "application/pdf")

from jira import JIRA
import streamlit as st
from jira import JIRA

from jira import JIRA
import streamlit as st

def create_jira_ticket(summary, description):
    jira_options = {"server": st.secrets["JIRA_SERVER"]}

    jira = JIRA(
        options=jira_options,
        basic_auth=(st.secrets["JIRA_EMAIL"], st.secrets["JIRA_API_TOKEN"])
    )

    # ✅ Instead of using session_state directly, store a fixed project key
    project_key = st.secrets["JIRA_PROJECT_KEY"]  # Add this to your Streamlit secrets

    new_issue = jira.create_issue(
        project=project_key,      # Use Jira project key (like "SAM1")
        summary=summary,
        description=description,
        issuetype={"name": "Task"}
    )
    return new_issue.key


