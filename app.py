import streamlit as st
from rag_chain import ask_ecoassist, clear_memory

st.set_page_config(
    page_title="EcoAssist AI",
    page_icon="🌱",
    layout="centered"
)

# ---------------- SESSION ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "run_once" not in st.session_state:
    st.session_state.run_once = False


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("🌱 EcoAssist")

    st.markdown("""
🌍 Climate change  
♻ Recycling  
💧 Water saving  
⚡ Renewable energy  
🌱 Sustainable living  
""")

    st.divider()

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []
        clear_memory()
        st.rerun()


# ---------------- HEADER ----------------
st.title("🌱 EcoAssist AI")
st.markdown("Ask anything about sustainability 🌍")

st.markdown("---")


# ---------------- QUICK BUTTONS ----------------
st.markdown("## ⚡ Quick Questions")

col1, col2 = st.columns(2)

with col1:
    if st.button("🌍 Climate change"):
        st.session_state.user_input = "What is climate change?"

    if st.button("♻ Recycling"):
        st.session_state.user_input = "How does recycling help?"

with col2:
    if st.button("💧 Save water"):
        st.session_state.user_input = "How can I save water?"

    if st.button("⚡ Renewable energy"):
        st.session_state.user_input = "What is renewable energy?"


# ---------------- INPUT ----------------
user_input = st.chat_input("Ask EcoAssist...")

if user_input:
    st.session_state.user_input = user_input

prompt = st.session_state.pop("user_input", None)


# ---------------- CHAT OUTPUT ----------------
if prompt:

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("🌱 Thinking..."):
            answer = ask_ecoassist(prompt)
            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})


# ---------------- HISTORY (ONLY ONCE) ----------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
