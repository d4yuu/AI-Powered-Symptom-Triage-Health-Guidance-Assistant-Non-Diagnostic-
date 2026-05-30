import streamlit as st
from prompt_builder import build_prompt
from llm_client import generate_ai_response

# Page config
st.set_page_config(page_title="Health Chat Assistant", layout="centered")

st.title("Health Symptom Chat Assistant")
st.write("Ask about your symptoms. This tool provides general guidance only (non-diagnostic).")

# -----------------------------
# Initialize session state
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Display chat history
# -----------------------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.write(msg["content"])
    else:
        with st.chat_message("assistant"):
            st.write(msg["content"])

# -----------------------------
# User input
# -----------------------------
user_input = st.chat_input("Describe your symptoms or ask a question...")

if user_input:
    # 1. Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # 2. Build simple context (last 3 messages)
    recent_context = ""
    for msg in st.session_state.messages[-4:]:
        role = "User" if msg["role"] == "user" else "Assistant"
        recent_context += f"{role}: {msg['content']}\n"

    # 3. Build prompt with context
    combined_input = f"""
Previous conversation:
{recent_context}

Current user message:
{user_input}
"""

    prompt = build_prompt(combined_input)

    # 4. Call API
    with st.spinner("Thinking..."):
        ai_response = generate_ai_response(prompt)

    # 5. Add AI response to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_response
    })

    # 6. Rerun to update UI
    st.rerun()