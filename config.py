"""
config.py — Konfigurasi global untuk Personal AI Agent
"""
import os

# Workspace: folder tempat AI boleh baca/tulis/hapus file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_PATH = os.path.join(BASE_DIR, "workspace")

# Ollama (LLM lokal)
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL    = os.getenv("OLLAMA_MODEL", "kimi-k2.5:cloud")

# SearXNG (self-hosted search engine)
SEARXNG_URL = os.getenv("SEARXNG_URL", "http://localhost:8080")

# Agent settings
AGENT_NAME = "Jamal"
MAX_ITERATIONS = 30          # Batas loop ReAct agent (ditingkatkan agar tidak mudah limit)
REQUEST_TIMEOUT = 25         # Timeout HTTP (detik)
