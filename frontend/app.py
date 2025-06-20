import streamlit as st
import requests

# Set page title and layout
st.set_page_config(page_title="Legal Assistant", layout="centered")
st.title("Legal Document Analyzer and Assistant")

# Create two tabs: one for document analysis, one for chatbot
tab1, tab2 = st.tabs(["Analyze Document", "Legal Assistant Chatbot"])

# ==============================
# Tab 1: Legal Document Analyzer
# ==============================
with tab1:
    st.header("Document Analysis")
    st.markdown("Paste your legal document below. The system will summarize the content, extract key clauses, and identify named entities.")
    
    text_input = st.text_area("Legal Document Text", height=300)

    if st.button("Analyze Document"):
        if text_input.strip() == "":
            st.warning("Please enter some text to analyze.")
        else:
            try:
                response = requests.post("http://localhost:8000/analyze/", data={"text": text_input})
                results = response.json()

                st.subheader("Summary")
                st.write(results["summary"])

                st.subheader("Key Clauses")
                st.write(results["clauses"])

                st.subheader("Named Entities")
                st.write(results["entities"])

            except Exception as e:
                st.error(f"Unable to reach backend. Please ensure the API is running.\n\nDetails: {e}")

# ==============================
# Tab 2: Legal Assistant Chatbot
# ==============================
with tab2:
    st.header("Legal Assistant")
    st.markdown("Ask a legal question in plain English. The assistant will provide a simple explanation based on general legal knowledge.")

    user_input = st.text_input("Your Question")

    if st.button("Ask Assistant"):
        if user_input.strip() == "":
            st.warning("Please enter a question.")
        else:
            try:
                res = requests.post("http://localhost:8000/legal-assistant/chat/", data={"message": user_input})
                reply = res.json()["response"]
                st.text_area("Assistant's Response", value=reply, height=200)
            except Exception as e:
                st.error(f"Unable to connect to the chatbot backend. Please check your API.\n\nDetails: {e}")
