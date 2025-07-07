import streamlit as st
from ibm_watson_machine_learning.foundation_models import Model
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(page_title="Legal Sentiment Analyzer", layout="wide")

# Sidebar for API inputs
with st.sidebar:
    st.header("Watsonx.ai Settings")
    api_key = st.text_input("API Key", type="password", value=os.getenv("WATSONX_API_KEY"))
    project_id = st.text_input("Project ID", type="password", value=os.getenv("WATSONX_PROJECT_ID"))

# Initialize Watsonx model
def get_model():
    credentials = {
        "apikey": api_key,
        "url": os.getenv("WATSONX_URL")
    }
    model = Model(
        model_id="google/flan-t5-xxl",
        credentials=credentials,
        project_id=project_id
    )
    return model

# Few-shot prompt template
def build_prompt(legal_text):
    return f"""
    Analyze the sentiment of this legal text as POSITIVE, NEGATIVE, or NEUTRAL:
    
    Examples:
    1. "The appeal is denied." → NEGATIVE
    2. "Judgment for the plaintiff." → POSITIVE
    3. "Case remanded for further review." → NEUTRAL
    
    Text: "{legal_text}"
    Sentiment:"""

# Main UI
st.title("📜 Legal Sentiment Analyzer")
user_input = st.text_area("Paste legal text here:", height=200, placeholder="Enter the legal text")

if st.button("Analyze Sentiment"):
    if not user_input.strip():
        st.warning("Please enter legal text!")
    else:
        with st.spinner("Analyzing..."):
            try:
                model = get_model()
                prompt = build_prompt(user_input)
                response = model.generate_text(prompt=prompt)
                st.success(f"Result: **{response.strip()}**")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Example section
with st.expander("💡 Example Inputs"):
    st.code("""
    - "The motion to dismiss is granted." → POSITIVE
    - "Defendant found liable for breach." → NEGATIVE
    - "Parties agree to mediation." → NEUTRAL
    """)