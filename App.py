import time
import streamlit as st
from google import genai

st.set_page_config(page_title="Airvi AI", page_icon="✨")
st.title("Airvi AI")

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask Airvi anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        reply = None
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt,
                )
                reply = response.text
                break
            except Exception as e:
                if "503" in str(e) and attempt < 2:
                    time.sleep(2)
                    continue
                reply = "Airvi is experiencing high traffic right now. Please try sending your message again in a moment."
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
