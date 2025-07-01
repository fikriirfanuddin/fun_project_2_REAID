import streamlit as st
import requests

# Ganti dengan API key OpenRouter kamu
OPENROUTER_API_KEY = "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"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "openchat/openchat-3.5-0106:free"  # Contoh model

# Validasi API Key duluan
if not OPENROUTER_API_KEY:
    st.error("API Key belum disetel. Periksa kembali.")
    st.stop()

st.set_page_config(page_title="AI Chatbot Wisata Indonesia", page_icon="💬")
st.title("💬 AI Chatbot Wisata Indonesia")

# Inisialisasi riwayat chat di session_state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Fungsi untuk memanggil OpenRouter API
def get_ai_response(user_message):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            *st.session_state.messages,
            {"role": "user", "content": user_message}
        ]
    }
    response = requests.post(OPENROUTER_API_URL, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()
    if "choices" in result and len(result["choices"]) > 0:
        return result["choices"][0]["message"]["content"]
    else:
        return "AI tidak memberikan jawaban. Coba lagi nanti."

# Tampilkan riwayat chat sebagai bubble
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f"<div style='background:#DCF8C6;padding:10px;border-radius:10px;margin-bottom:5px;text-align:right'><b>🧑 Kamu:</b> {msg['content']}</div>",
            unsafe_allow_html=True)
    else:
        st.markdown(
            f"<div style='background:#F1F0F0;padding:10px;border-radius:10px;margin-bottom:5px;text-align:left'><b>🤖 AI:</b> {msg['content']}</div>",
            unsafe_allow_html=True)

# Input pesan user (gunakan key yang aman)
user_input = st.text_input("Ketik pesan...", key="user_message", placeholder="Tulis pesan di sini...")

if st.button("Kirim", use_container_width=True):
    if user_input.strip():
        # Simpan pesan user ke riwayat
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        with st.spinner("AI sedang mengetik..."):
            try:
                ai_reply = get_ai_response(user_input)
            except requests.exceptions.RequestException as e:
                st.error("Terjadi error saat request API.")
                if e.response is not None:
                    st.error(f"Detail error:\n{e.response.text}")
                ai_reply = "Terjadi kesalahan saat menghubungi AI."

        # Simpan respons AI ke riwayat
        st.session_state.messages.append({"role": "assistant", "content": ai_reply})
        # Bersihkan input (reset nilai key text_input)
        st.session_state.user_message = ""

        st.experimental_rerun()
