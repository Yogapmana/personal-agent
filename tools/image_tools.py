"""
tools/image_tools.py — Tool untuk mencari dan mengunduh gambar ke workspace
"""
import os
import requests
from langchain_core.tools import tool
from config import WORKSPACE_PATH

# Konfigurasi SearXNG lokal sesuai arsitektur proyek
SEARXNG_URL = "http://localhost:8080/search"

@tool
def search_and_download_image(query: str, filename: str) -> str:
    """
    Mencari gambar di internet berdasarkan query menggunakan mesin pencari (SearXNG) 
    dan mengunduhnya ke workspace.
    Gunakan tool ini ketika pengguna meminta untuk mencari dan mengunduh gambar.
    
    Args:
        query: Kata kunci pencarian gambar (contoh: 'kucing lucu', 'logo python').
        filename: Nama file untuk menyimpan gambar (contoh: 'kucing.jpg' atau 'images/logo.png').
    """
    try:
        # Tentukan lokasi penyimpanan dan pastikan aman di dalam workspace
        safe_path = os.path.normpath(os.path.join(WORKSPACE_PATH, filename))
        
        # Security check: must be inside WORKSPACE_PATH
        if not safe_path.startswith(os.path.abspath(WORKSPACE_PATH)):
            return f"❌ Error keamanan: Akses ditolak untuk '{filename}'. Harus disimpan di dalam workspace."
            
        # Pastikan folder penyimpanan ada
        os.makedirs(os.path.dirname(safe_path), exist_ok=True)
        
        # Request ke SearXNG lokal
        params = {
            "q": query,
            "format": "json",
            "categories": "images"
        }
        
        search_resp = requests.get(SEARXNG_URL, params=params, timeout=10)
        search_resp.raise_for_status()
        data = search_resp.json()
        
        results = data.get("results", [])
        if not results:
            return f"❌ Tidak dapat menemukan gambar untuk query '{query}'. Data dari SearXNG: {str(data)[:200]}"
            
        # Coba unduh dari hasil pertama yang memiliki img_src
        for res in results:
            image_url = res.get("img_src")
            if not image_url:
                continue
                
            # Hindari SVG atau icon engines kecuali jika mencari vector
            if image_url.lower().endswith('.svg') or res.get("engine") == "lucide":
                continue
                
            try:
                # Mengunduh gambar dengan stream dan timeout
                # Tambahkan User-Agent agar tidak diblokir oleh beberapa CDN/server gambar
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
                response = requests.get(image_url, stream=True, headers=headers, timeout=10)
                response.raise_for_status()
                
                # Verifikasi bahwa file yang didownload benar-benar gambar
                content_type = response.headers.get('Content-Type', '').lower()
                if not content_type.startswith('image/') or 'svg' in content_type:
                    continue
                
                with open(safe_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                return f"🖼️ Berhasil mencari dan mengunduh gambar '{query}'. Disimpan sebagai '{filename}' di workspace."
            except Exception as e:
                # Jika satu gambar gagal diunduh, lanjut mencoba gambar berikutnya dari hasil
                continue
                
        return f"❌ Gagal mengunduh gambar dari hasil pencarian untuk '{query}'."

    except Exception as e:
        return f"❌ Terjadi kesalahan saat mencari/mengunduh gambar: {str(e)}"
