"""
tools/web_search.py — Web search & scraping tools untuk Personal AI Agent
Menggunakan SearXNG sebagai search engine dan BeautifulSoup untuk scraping.
"""
import datetime
import requests
from bs4 import BeautifulSoup
from langchain_core.tools import tool
from config import SEARXNG_URL, REQUEST_TIMEOUT


@tool
def get_current_datetime() -> str:
    """
    Dapatkan waktu dan tanggal saat ini (timezone lokal).
    Gunakan tool ini sebelum mencari berita/info terbaru agar
    AI tahu konteks waktu yang relevan.
    """
    now = datetime.datetime.now()
    return (
        f"🕐 Waktu saat ini: {now.strftime('%A, %d %B %Y — %H:%M:%S WIB')}"
    )


@tool
def internet_search(query: str, num_results: int = 5) -> str:
    """
    Cari informasi terbaru di internet menggunakan SearXNG.
    Gunakan tool ini ketika user meminta info terkini, berita,
    atau hal yang memerlukan data real-time.

    Args:
        query: Kata kunci pencarian (contoh: 'berita teknologi Indonesia hari ini')
        num_results: Jumlah hasil yang dikembalikan (default 5, maks 10)
    """
    num_results = min(max(num_results, 1), 10)
    try:
        # Menambahkan parameter engines untuk menggunakan mesin pencari yang jarang memblokir
        # Karena google, duckduckgo, dan startpage sering terkena rate-limit / captcha.
        params = {
            "q": query,
            "format": "json",
            "language": "id-ID",
            "safesearch": "0",
            "engines": "bing,yahoo,qwant,brave,wikipedia"
        }
        resp = requests.get(
            f"{SEARXNG_URL}/search",
            params=params,
            timeout=REQUEST_TIMEOUT,
        )
        resp.raise_for_status()
        data = resp.json()
        results = data.get("results", [])[:num_results]

        # Jika masih kosong, coba tanpa filter engine (default SearXNG)
        if not results:
            params.pop("engines")
            resp = requests.get(
                f"{SEARXNG_URL}/search",
                params=params,
                timeout=REQUEST_TIMEOUT,
            )
            data = resp.json()
            results = data.get("results", [])[:num_results]

        # Cek engine unresponsive untuk debugging
        unresponsive = data.get("unresponsive_engines", [])
        unresponsive_info = ""
        if unresponsive:
            names = ", ".join(e[0] for e in unresponsive)
            unresponsive_info = f"\n⚠️ Engine tidak merespons: {names}"

        if not results:
            return (
                f"🔍 Tidak ada hasil untuk '{query}'.{unresponsive_info}\n"
                "   Tips: Pastikan SearXNG terhubung internet dan engine aktif."
            )

        lines = [f"🔍 Hasil pencarian untuk: '{query}'{unresponsive_info}\n"]
        for i, r in enumerate(results, 1):
            lines.append(
                f"{i}. **{r.get('title', 'Tanpa judul')}**\n"
                f"   URL: {r.get('url', '-')}\n"
                f"   {r.get('content', '')[:200]}...\n"
            )
        return "\n".join(lines)

    except requests.exceptions.ConnectionError:
        return (
            "❌ Tidak bisa terhubung ke SearXNG. "
            "Pastikan SearXNG berjalan di Docker/Podman "
            f"pada {SEARXNG_URL}."
        )
    except requests.exceptions.Timeout:
        return f"❌ Timeout saat mencari '{query}'. Coba lagi nanti."
    except Exception as e:
        return f"❌ Error saat melakukan pencarian: {e}"


@tool
def scrape_url(url: str) -> str:
    """
    Ambil dan bersihkan konten teks dari sebuah URL / halaman web.
    Gunakan tool ini setelah internet_search untuk membaca isi artikel berita
    atau halaman secara lebih detail.

    Args:
        url: URL lengkap halaman yang ingin di-scrape (contoh: 'https://cnnindonesia.com/...')
    """
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }
        resp = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")

        # Hapus tag yang tidak relevan
        for tag in soup(["script", "style", "nav", "footer", "header", "aside", "ads"]):
            tag.decompose()

        # Ambil teks bersih
        text = soup.get_text(separator="\n", strip=True)
        # Bersihkan baris kosong berlebihan
        lines = [l for l in text.splitlines() if l.strip()]
        clean = "\n".join(lines[:150])  # Batasi 150 baris

        if not clean:
            return f"⚠️ Tidak bisa mengambil konten dari {url}."

        return f"🌐 Konten dari {url}:\n\n{clean}"

    except requests.exceptions.Timeout:
        return f"❌ Timeout saat mengakses {url}."
    except requests.exceptions.ConnectionError:
        return f"❌ Tidak bisa terhubung ke {url}."
    except Exception as e:
        return f"❌ Error saat scraping {url}: {e}"
