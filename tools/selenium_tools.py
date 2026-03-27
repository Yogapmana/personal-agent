"""
tools/selenium_tools.py — Tool web scraping lanjutan menggunakan Selenium (mendukung JavaScript rendering).
"""
import time
from bs4 import BeautifulSoup
from langchain.tools import tool
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@tool
def advanced_scrape_url(url: str, wait_time: int = 5) -> str:
    """
    Mengambil konten teks dari sebuah URL / halaman web secara LENGKAP menggunakan browser headless (Selenium).
    Gunakan tool ini jika halaman web banyak menggunakan JavaScript (misal: React, Vue, Twitter, situs berita modern)
    atau jika tool `scrape_url` biasa mengembalikan hasil kosong / error.
    
    Args:
        url (str): URL lengkap halaman yang ingin di-scrape.
        wait_time (int): Waktu tunggu ekstra dalam detik agar JavaScript selesai memuat konten (default 5 detik).
        
    Returns:
        str: Konten teks hasil scraping yang sudah dibersihkan, atau pesan error.
    """
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Menambahkan fake User-Agent
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    driver = None
    try:
        # Menginisialisasi WebDriver (Selenium Manager di Selenium 4.10+ otomatis mendownload Chrome for Testing)
        driver = webdriver.Chrome(options=options)
        
        # Mengatur batas waktu pemuatan halaman (timeout)
        driver.set_page_load_timeout(30)
        
        # Membuka URL
        driver.get(url)
        
        # Tunggu beberapa detik agar script AJAX/React/Vue merender konten
        time.sleep(wait_time)
        
        # Ambil seluruh sumber HTML yang sudah dirender oleh browser
        page_source = driver.page_source
        
        # Gunakan BeautifulSoup untuk membersihkan tag HTML
        soup = BeautifulSoup(page_source, "html.parser")
        
        # Hapus elemen yang tidak penting (script, style, nav, dll)
        for tag in soup(["script", "style", "nav", "footer", "header", "aside", "noscript"]):
            tag.decompose()
            
        # Ambil teks bersih
        text = soup.get_text(separator="\n", strip=True)
        lines = [l for l in text.splitlines() if l.strip()]
        
        # Batasi output maksimal agar tidak membebani memori context agent (sekitar 200 baris)
        clean = "\n".join(lines[:200])
        
        if not clean:
            return f"⚠️ Tidak bisa mengambil konten (mungkin halamannya kosong atau diblokir) dari {url}."
            
        return f"🌐 [SELENIUM] Konten dirender dari {url}:\n\n{clean}"
        
    except Exception as e:
        return f"❌ Error saat advanced scraping {url}: {str(e)}"
    finally:
        if driver:
            driver.quit()  # Pastikan browser ditutup agar tidak membebani memori
