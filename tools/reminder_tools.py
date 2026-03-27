"""
tools/reminder_tools.py — Tool untuk mengatur pengingat/reminder di waktu tertentu.
"""
import threading
from datetime import datetime
from langchain.tools import tool

def _show_reminder(message: str):
    """Fungsi internal yang akan dipanggil saat waktu pengingat tiba."""
    print(f"\n\n\033[93m[⏰ PENGINGAT/REMINDER]: {message}\033[0m\n\n")

@tool
def set_reminder(target_time: str, message: str) -> str:
    """
    Mengatur pengingat (reminder) yang akan aktif pada waktu yang ditentukan.
    Gunakan tool ini jika pengguna meminta untuk diingatkan tentang sesuatu di masa depan.
    
    Args:
        target_time (str): Waktu target pengingat dengan format 'YYYY-MM-DD HH:MM:SS'. Contoh: '2023-12-31 15:30:00'.
        message (str): Pesan pengingat yang ingin disampaikan.
        
    Returns:
        str: Konfirmasi apakah pengingat berhasil diatur atau gagal (misal jika format waktu salah).
    """
    try:
        target_dt = datetime.strptime(target_time, "%Y-%m-%d %H:%M:%S")
        now = datetime.now()
        
        delay_seconds = (target_dt - now).total_seconds()
        
        if delay_seconds <= 0:
            return "Gagal: Waktu yang ditentukan sudah berlalu. Silakan tentukan waktu di masa depan."
            
        # Membuat timer yang berjalan di background thread
        timer = threading.Timer(delay_seconds, _show_reminder, args=[message])
        timer.daemon = True  # Thread akan mati secara otomatis jika program utama berhenti
        timer.start()
        
        return f"Pengingat berhasil diatur. Sistem akan mengingatkan pada {target_time} dengan pesan: '{message}'"
    except ValueError:
        return "Gagal: Format waktu tidak valid. Pastikan menggunakan format 'YYYY-MM-DD HH:MM:SS'."
    except Exception as e:
        return f"Gagal mengatur pengingat: {str(e)}"
