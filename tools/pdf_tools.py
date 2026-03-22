"""
tools/pdf_tools.py — Tool untuk membuat file PDF di dalam workspace
"""
import os
from langchain_core.tools import tool
from config import WORKSPACE_PATH

try:
    from fpdf import FPDF
except ImportError:
    FPDF = None

@tool
def create_pdf(filename: str, title: str, content: str, image_path: str = "") -> str:
    """
    Buat file PDF baru di workspace dengan judul, konten teks, dan opsional gambar.
    Gunakan tool ini ketika user meminta untuk membuat, mengekspor, atau menggenerate file PDF (contoh: laporan, ringkasan, dll).

    Args:
        filename: Nama file PDF yang akan dibuat (contoh: 'laporan.pdf' atau 'docs/resume.pdf'). Harus berakhiran .pdf
        title: Judul dokumen yang akan ditulis di bagian atas PDF.
        content: Isi teks dari dokumen PDF tersebut.
        image_path: (Opsional) Path/nama file gambar di dalam workspace yang ingin disisipkan ke dalam PDF (contoh: 'mountain.jpg' atau 'Picture/foto.png'). Kosongkan jika tidak ada gambar.
    """
    if not FPDF:
        return "❌ Modul fpdf2 tidak terinstal. Tidak dapat membuat PDF."

    if not filename.lower().endswith('.pdf'):
        filename += '.pdf'

    try:
        # Resolve the path properly and check security
        safe_path = os.path.normpath(os.path.join(WORKSPACE_PATH, filename))
        
        # Security check: must be inside WORKSPACE_PATH
        if not safe_path.startswith(os.path.abspath(WORKSPACE_PATH)):
            return f"❌ Error keamanan: Akses ditolak. '{filename}' berada di luar workspace."
            
        # Pastikan folder tempat file akan disimpan sudah ada
        os.makedirs(os.path.dirname(safe_path), exist_ok=True)
        
        class PDF(FPDF):
            def header(self):
                # Arial bold 15
                self.set_font("helvetica", "B", 15)
                # Judul
                self.cell(0, 10, title, align="C", new_x="LMARGIN", new_y="NEXT")
                # Line break
                self.ln(10)

            def footer(self):
                # Posisi 1.5 cm dari bawah
                self.set_y(-15)
                # Arial italic 8
                self.set_font("helvetica", "I", 8)
                # Nomor halaman
                self.cell(0, 10, f"Page {self.page_no()}", align="C")

        pdf = PDF()
        pdf.add_page()
        
        # Sisipkan gambar jika diberikan
        if image_path:
            safe_image_path = os.path.normpath(os.path.join(WORKSPACE_PATH, image_path))
            if not safe_image_path.startswith(os.path.abspath(WORKSPACE_PATH)):
                return f"❌ Error keamanan gambar: Akses ditolak. '{image_path}' berada di luar workspace."
            
            if not os.path.exists(safe_image_path):
                return f"❌ File gambar '{image_path}' tidak ditemukan di workspace."
                
            try:
                # Menggunakan max width 150 agar muat di halaman (A4 lebar ~210mm)
                # gambar akan diposisikan di tengah (asumsi A4 lebar 210, gambar lebar 150 -> x=(210-150)/2=30)
                pdf.image(safe_image_path, x=30, w=150)
                pdf.ln(10)  # Tambahkan jarak setelah gambar
            except Exception as img_err:
                return f"❌ Gagal memuat gambar '{image_path}' ke dalam PDF: {str(img_err)}"
        
        # Set font untuk konten
        pdf.set_font("helvetica", size=12)
        
        # Tambahkan teks dengan multi_cell agar teks yang panjang di-wrap ke baris berikutnya
        safe_content = content.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 10, safe_content)
        
        # Simpan file PDF
        pdf.output(safe_path)
        
        msg = f"📄 Berhasil membuat file PDF '{filename}' di workspace."
        if image_path:
            msg += f" (dengan gambar '{image_path}')"
        return msg
        
    except Exception as e:
        return f"❌ Gagal membuat file PDF: {str(e)}"
