import streamlit as st
from google import genai

# This pulls the key safely from the Streamlit "Vault"
api_key = st.secrets["GOOGLE_API_KEY"]
client = genai.Client(api_key=api_key)

st.set_page_config(page_title="Highland Med Auth", page_icon="🏥")
st.title("🏥 Highland Med: Prior Auth Assistant")

patient_details = st.text_area("Patient & Procedure Details:", 
                             placeholder="e.g. Sarah Jones, In-home PT post-op...")

if st.button("Generate Letter"):
    with st.spinner('Drafting your letter...'):
        response = client.models.generate_content(
            model="gemini-1.5-flash", 
            contents=f"Draft a professional medical prior authorization letter for: {patient_details}"
        )
        st.markdown("### Drafted Letter:")
        st.write(response.text)