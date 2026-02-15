import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq
from prompt import SYSTEM_PROMPT

load_dotenv()

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Lead Response Assistant", page_icon="✉️", layout="centered")

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Clean, minimal, human feel */
    .block-container { max-width: 700px; padding-top: 2rem; }
    h1 { font-size: 1.4rem !important; font-weight: 600 !important; color: #111 !important; }
    .subtitle { color: #666; font-size: 0.9rem; margin-bottom: 1.5rem; }
    .reply-box {
        background: #fff;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 22px 26px;
        font-size: 0.95rem;
        line-height: 1.75;
        color: #222;
        white-space: pre-wrap;
        font-family: Georgia, serif;
        margin-top: 1rem;
    }
    .label { font-size: 0.8rem; color: #888; font-weight: 500; text-transform: uppercase;
             letter-spacing: 0.05em; margin-bottom: 0.3rem; }
    .stButton > button {
        border-radius: 6px !important;
        font-size: 0.85rem !important;
    }
    footer { visibility: hidden; }
    #MainMenu { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Session State ──────────────────────────────────────────────────────────────
if "enquiry_text" not in st.session_state:
    st.session_state.enquiry_text = ""

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("### 📬 Lead Response Assistant")
st.markdown('<p class="subtitle">Turn customer enquiries into ready-to-send replies.</p>', unsafe_allow_html=True)

# ── API Key ────────────────────────────────────────────────────────────────────
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    api_key = st.text_input("API Key", type="password", placeholder="gsk_...")
    if not api_key:
        st.stop()

client = Groq(api_key=api_key)

# ── Quick Examples ─────────────────────────────────────────────────────────────
st.markdown('<p class="label">Quick examples</p>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

EXAMPLES = {
    "damp": "Hi, I am getting damp patches on my bedroom wall after rains. What should I do?",
    "roof": "Our office roof has been leaking for two weeks. We have important equipment inside. How quickly can someone come?",
    "mould": "I think there might be mould behind my bathroom tiles. Is this dangerous and how much would it cost to fix?"
}

with col1:
    if st.button("Damp wall", use_container_width=True):
        st.session_state.enquiry_text = EXAMPLES["damp"]
        st.rerun()
with col2:
    if st.button("Roof leak", use_container_width=True):
        st.session_state.enquiry_text = EXAMPLES["roof"]
        st.rerun()
with col3:
    if st.button("Mould issue", use_container_width=True):
        st.session_state.enquiry_text = EXAMPLES["mould"]
        st.rerun()

st.markdown("")

# ── Input ──────────────────────────────────────────────────────────────────────
st.markdown('<p class="label">Customer message</p>', unsafe_allow_html=True)
enquiry = st.text_area(
    label="Incoming Message",
    value=st.session_state.enquiry_text,
    height=140,
    placeholder="Paste the customer's message here...",
    label_visibility="visible"
)


# ── Draft Button ───────────────────────────────────────────────────────────────
if st.button("Generate Response", type="primary", use_container_width=True):
    if not enquiry.strip():
        st.warning("Add a customer message first.")
    else:
        with st.spinner("Writing..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": f"Write a reply to this customer message:\n\n{enquiry}"}
                    ],
                    max_tokens=512,
                    temperature=0.85
                )

                reply = response.choices[0].message.content.strip()

                st.markdown("")
                st.markdown('<p class="label">Suggested response</p>', unsafe_allow_html=True)
                st.markdown(f'<div class="reply-box">{reply}</div>', unsafe_allow_html=True)
                st.markdown("")
                st.code(reply, language=None)
                st.caption("Click the copy icon in the top-right to copy this response.")

            except Exception as e:
                err = str(e)
                if "401" in err or "invalid" in err.lower():
                    st.error("API key not valid — check your .env file.")
                elif "429" in err or "quota" in err.lower():
                    st.error("Rate limit — wait 30 seconds and try again.")
                else:
                    st.error(f"Error: {e}")