import streamlit as st
import requests

st.title("🧾 Legal Analyzer & 🤖 Assistant")

tab1, tab2 = st.tabs(["📄 Analyze Document", "🤖 Legal Assistant"])

# Analyzer Tab
with tab1:
    text_input = st.text_area("Paste legal text here:", height=300)
    if st.button("Analyze"):
        try:
            response = requests.post("http://localhost:8000/analyze/", data={"text": text_input})
            results = response.json()
            st.subheader("📌 Summary")
            st.write(results["summary"])
            st.subheader("📌 Key Clauses")
            st.write(results["clauses"])
            st.subheader("📌 Named Entities")
            st.write(results["entities"])
        except:
            st.error("Backend not responding. Please check if FastAPI is running.")

# Chatbot Tab
with tab2:
    st.markdown("Ask your legal questions here:")
    user_input = st.text_input("💬 You:")
    if st.button("Send"):
        if user_input:
            try:
                res = requests.post("http://localhost:8000/legal-assistant/chat/", data={"message": user_input})
                reply = res.json()["response"]
                st.success(f"🤖 Legal Assistant: {reply}")
            except:
                st.error("Chatbot backend unavailable. Is it running?")
