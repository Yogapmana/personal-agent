"""
main.py — Entry point CLI untuk Personal AI Agent
"""
import sys
import os

# Pastikan root project ada di sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent_logic import create_agent, run_agent
from config import AGENT_NAME, OLLAMA_MODEL, WORKSPACE_PATH


BANNER = f"""
╔══════════════════════════════════════════════════════════════╗
║          🤖  Personal AI Agent — {AGENT_NAME:<26}║
║  Model  : {OLLAMA_MODEL:<50}║
║  Workspace: {WORKSPACE_PATH:<48}║
╚══════════════════════════════════════════════════════════════╝
  Ketik pesan kamu dan tekan Enter.
  Ketik 'exit' atau 'quit' untuk keluar.
  Ketik 'clear' untuk reset percakapan.
──────────────────────────────────────────────────────────────
"""


def print_separator():
    print("──────────────────────────────────────────────────────────────")


def main():
    print(BANNER)

    # Inisialisasi agent
    print("⏳ Menginisialisasi agent...")
    try:
        agent = create_agent()
        print(f"✅ {AGENT_NAME} siap! Yuk ngobrol.\n")
    except Exception as e:
        print(f"❌ Gagal menginisialisasi agent: {e}")
        print("   Pastikan Ollama berjalan: 'ollama serve'")
        sys.exit(1)

    chat_history = []

    while True:
        try:
            user_input = input("\n🧑 Kamu: ").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n\n👋 Sampai jumpa! {AGENT_NAME} keluar.")
            break

        if not user_input:
            continue

        # Perintah khusus
        if user_input.lower() in ("exit", "quit", "keluar"):
            print(f"\n👋 Sampai jumpa! {AGENT_NAME} keluar.")
            break

        if user_input.lower() in ("clear", "reset", "bersih"):
            chat_history = []
            print("🧹 Percakapan direset. Mulai fresh lagi!")
            continue

        if user_input.lower() in ("help", "bantuan", "?"):
            print(
                "\n📖 Perintah tersedia:\n"
                "  exit / quit / keluar  → Keluar dari agent\n"
                "  clear / reset         → Reset riwayat percakapan\n"
                "  help / bantuan / ?    → Tampilkan bantuan ini\n"
            )
            continue

        # Proses pesan ke agent
        print(f"\n🤖 {AGENT_NAME}: ", end="", flush=True)
        try:
            response, chat_history = run_agent(agent, user_input, chat_history)
            print(response)
            print_separator()
        except KeyboardInterrupt:
            print("\n⏸️  Dibatalkan.")
            continue
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("   Coba lagi atau ketik 'exit' untuk keluar.")
            continue


if __name__ == "__main__":
    main()
