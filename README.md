# Personal AI Agent 🤖

Sebuah asisten AI pribadi berbasis CLI yang dibangun menggunakan **LangChain**, **LangGraph**, dan model lokal melalui **Ollama**. Agent ini dirancang untuk berinteraksi di dalam environment lokal dengan menggunakan berbagai *tools* yang tersedia.

## 🌟 Fitur

- **Command Line Interface (CLI):** Antarmuka terminal yang sederhana dan interaktif.
- **Local AI Execution:** Menggunakan Ollama untuk menjalankan model AI secara lokal, memastikan privasi data dan efisiensi.
- **Tools Integrations:** Agent dilengkapi dengan kemampuan untuk melakukan pencarian dan download gambar (via SearXNG), web scraping (BeautifulSoup), system monitoring (psutil), manipulasi file/direktori, dan pembuatan dokumen (fpdf2).
- **Workspace Isolation:** Mengelola dan menjalankan file secara terkendali pada folder workspace.

## 📋 Persyaratan Sistem

- Python 3.8 atau lebih baru
- [Ollama](https://ollama.com/) (terpasang dan berjalan dengan model yang ditentukan di konfigurasi)
- [Docker](https://docs.docker.com/get-docker/) (untuk menjalankan SearXNG lokal)

## 🚀 Cara Instalasi

1. Clone repositori ini atau pastikan kamu berada di dalam direktori `AgentAI`:
   ```bash
   cd /path/to/AgentAI
   ```

2. Buat Virtual Environment (opsional namun sangat disarankan):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Untuk Linux/macOS
   # .venv\Scripts\activate   # Untuk Windows
   ```

3. Install dependensi dari `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```

4. Menjalankan SearXNG via Docker:
   Agent ini menggunakan SearXNG sebagai mesin pencari lokal untuk mendapatkan berita dan gambar dari internet tanpa takut API limit. Jalankan SearXNG menggunakan Docker:
   ```bash
   docker run -d --name searxng \
     -p 8080:8080 \
     -v ${PWD}/searxng:/etc/searxng \
     -e "BASE_URL=http://localhost:8080/" \
     -e "INSTANCE_NAME=agent-search" \
     searxng/searxng:latest
   ```
   *Catatan: Pastikan container ini menyala sebelum menggunakan fitur `internet_search` atau `search_and_download_image`.*

## ⚙️ Konfigurasi

Kamu bisa mengatur perilaku agent dengan memodifikasi file `config.py`. Beberapa konfigurasi utama meliputi:
- `AGENT_NAME`: Nama dari agent.
- `OLLAMA_MODEL`: Model bahasa (LLM) dari Ollama yang akan digunakan (misalnya: `llama3`, `mistral`, dll).
- `WORKSPACE_PATH`: Direktori ruang kerja untuk agent.

## 🏃‍♂️ Cara Menjalankan

Setelah semua instalasi selesai, jalankan file utama:

```bash
python main.py
```

Setelah aplikasi berjalan, kamu akan melihat banner CLI dan dapat mulai mengetikkan perintah/pesan langsung kepada agent.

## 🗂️ Struktur Direktori

- `main.py` - Entry point CLI utama.
- `agent_logic.py` - Inti logika LangGraph dan definisi agent.
- `config.py` - File konfigurasi project.
- `tools/` - Kumpulan tools kustom yang bisa digunakan oleh agent.
- `workspace/` - Direktori khusus untuk file I/O agent.
