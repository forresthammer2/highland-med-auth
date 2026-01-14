import streamlit as st
from google import genai
import time

# UI CONFIG
st.set_page_config(page_title="Highland Medical Auth", page_icon="🛡️", layout="wide")

# CUSTOM CSS FOR "MEDICAL LOOK"
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { background-color: #004a99; color: white; border-radius: 5px; width: 100%; }
    .reportview-container { background: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.title("🛡️ Admin Portal")
    st.info("2026 CMS Compliance Engine Active")
    api_key = st.text_input("Clinic Access Key", type="password", value="AIzaSyCIhY6gqvWARF9iwAUi-z2upYqhrNKnw5M")
    st.divider()
    st.write("📍 **Location:** Highland/Springville Hub")

# MAIN INTERFACE
st.title("Prior Authorization Drafting Assistant")
st.subheader("Automated 'Letter of Medical Necessity' Generator")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 1. Clinical Input")
    patient_id = st.text_input("Internal Patient ID (e.g. Pt-99)", placeholder="Do NOT use real names")
    procedure = st.text_input("Requested Procedure/Medication", placeholder="e.g. Lumbar MRI or Humira")
    raw_notes = st.text_area("Paste De-identified Clinical Notes", height=300, 
                             placeholder="Patient has failed 6 weeks of PT... Exam shows + Lasegue sign...")

with col2:
    st.markdown("### 2. Draft Generation")
    if st.button("Generate Bulletproof Draft"):
        if not raw_notes or not procedure:
            st.error("Please provide both the procedure and the clinical notes.")
        else:
            with st.spinner("Analyzing 2026 CMS Guidelines..."):
                try:
                    client = genai.Client(api_key=api_key)
                    prompt = f"""
                    Role: Expert Medical Billing Advocate.
                    Task: Write a formal Letter of Medical Necessity for {procedure}.
                    Patient Ref: {patient_id}.
                    
                    Clinical Context: {raw_notes}
                    
                    Structure:
                    - Clinical History & Diagnosis (ICD-10 relevance)
                    - Summary of Failed Treatments (Step Therapy)
                    - Rationale for current request
                    - Urgent 72-hour turnaround request (per 2026 CMS-0057-F)
                    
                    Tone: Professional, clinical, and firm.
                    """
                    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
                    
                    st.success("Draft Complete!")
                    st.text_area("Final Draft (Copy/Paste to EHR)", value=response.text, height=450)
                    st.download_button("Download Draft (.txt)", response.text, file_name=f"PA_{patient_id}.txt")
                except Exception as e:
                    st.error(f"Error: {e}")

st.divider()
st.caption("Internal Use Only - HIPAA Compliance Warning: Ensure all PHI is removed before processing.")
