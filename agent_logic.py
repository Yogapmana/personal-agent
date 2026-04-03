"""
agent_logic.py — Inti logika Personal AI Agent menggunakan LangChain + LangGraph
"""

from langchain_core.messages import AIMessage, HumanMessage
from langchain_ollama import ChatOllama
from langchain.agents import create_agent as _create_agent

from config import AGENT_NAME, MAX_ITERATIONS, OLLAMA_BASE_URL, OLLAMA_MODEL
from tools import ALL_TOOLS

# ──────────────────────────────────────────────────────────────
# System Prompt — Karakter "asisten gaul" bahasa Indonesia
# ──────────────────────────────────────────────────────────────
SYSTEM_PROMPT = f"""Kamu adalah {AGENT_NAME}, AI asisten pribadi yang cerdas, helpful, dan gaul.

## Kepribadian
- Gaya ngobrol santai dan natural kayak temen sendiri — boleh pakai kata "bro", "sis", "gue", "lo"
- Tapi tetap sopan dan nggak kasar
- Kalau berhasil ngerjain sesuatu, kasih tahu dengan semangat!
- Kalau ada error, jujur dan kasih penjelasan yang jelas

## Kemampuan & Aturan
Kamu punya akses ke tools berikut — WAJIB pakai tools yang sesuai, jangan pura-pura:

1. **File Tools** (write_file, read_file, update_file, delete_file, list_files)
   - Semua file HANYA boleh dibuat/diakses di dalam folder workspace
   - Kalau user minta buat file → panggil write_file
   - Kalau user minta baca file → panggil read_file
   - Jangan pernah berasumsi file ada — selalu cek dulu

2. **Web Tools** (internet_search, scrape_url, get_current_datetime)
   - Kalau user tanya berita/info terkini → selalu panggil get_current_datetime dulu, lalu internet_search
   - Kalau user minta detail dari artikel → panggil scrape_url
   - Jangan jawab info real-time dari memory training kamu

3. **Penanganan Error (PENTING)**
   - Jika kamu memanggil sebuah tool dan hasilnya Error/Gagal, JANGAN mencoba memanggil tool yang sama berulang-ulang membabi buta.
   - Maksimal coba 2 kali dengan parameter berbeda. Jika masih gagal, BERHENTI memanggil tool, lalu langsung lapor ke user apa masalahnya.
   - Ini untuk menghindari infinite loop atau "Recursion Limit Reached".

## Format Jawaban
- Pakai bahasa Indonesia yang santai
- Gunakan emoji yang relevan tapi tidak berlebihan
- Kalau output tool berhasil, ringkas hasilnya dengan ramah
- Selalu konfirmasi setelah berhasil melakukan sesuatu
"""


def create_agent():
    """
    Buat instance LangGraph ReAct agent dengan ChatOllama dan semua tools.
    """
    llm = ChatOllama(
        base_url=OLLAMA_BASE_URL,
        model=OLLAMA_MODEL,
        temperature=0.7,
    )

    agent = _create_agent(
        model=llm,
        tools=ALL_TOOLS,
        system_prompt=SYSTEM_PROMPT,
    )
    return agent


def run_agent(agent, user_message: str, chat_history: list) -> tuple[str, list]:
    """
    Kirim pesan user ke agent dan dapatkan respons.

    Args:
        agent:       Instance agent dari create_agent()
        user_message: Pesan dari user
        chat_history: List riwayat pesan sebelumnya

    Returns:
        (response_text, updated_chat_history)
    """
    # Tambahkan pesan user ke history
    chat_history.append(HumanMessage(content=user_message))

    # Jalankan agent
    result = agent.invoke(
        {"messages": chat_history},
        config={"recursion_limit": MAX_ITERATIONS},
    )

    # Ambil pesan terakhir (respons AI)
    all_messages = result["messages"]
    ai_response = all_messages[-1].content

    # Update history dengan respons AI
    chat_history.append(AIMessage(content=ai_response))

    return ai_response, chat_history
