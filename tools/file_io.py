"""
tools/file_io.py — File CRUD tools untuk Personal AI Agent
Semua operasi dibatasi HANYA di dalam WORKSPACE_PATH (sandbox).
"""
import os
from langchain_core.tools import tool
from config import WORKSPACE_PATH


def _safe_path(filename: str) -> str:
    """
    Resolve path dan pastikan masih di dalam WORKSPACE_PATH.
    Lempar ValueError jika ada path traversal attack.
    """
    # Bersihkan leading slash biar aman
    safe_name = os.path.basename(filename)
    full_path = os.path.join(WORKSPACE_PATH, safe_name)
    # Cek: path hasil resolve harus berada di dalam workspace
    if not os.path.abspath(full_path).startswith(os.path.abspath(WORKSPACE_PATH)):
        raise ValueError(f"Akses ditolak: '{filename}' berada di luar workspace.")
    return full_path


@tool
def write_file(filename: str, content: str) -> str:
    """
    Buat atau tulis file baru di workspace dengan konten tertentu.
    Gunakan tool ini ketika user meminta membuat atau menyimpan suatu file.

    Args:
        filename: Nama file yang akan dibuat (contoh: 'catatan.txt')
        content: Isi / konten yang akan ditulis ke dalam file
    """
    try:
        os.makedirs(WORKSPACE_PATH, exist_ok=True)
        path = _safe_path(filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"✅ File '{filename}' berhasil dibuat di workspace."
    except ValueError as e:
        return f"❌ Error keamanan: {e}"
    except Exception as e:
        return f"❌ Gagal membuat file: {e}"


@tool
def read_file(filename: str) -> str:
    """
    Baca dan kembalikan isi file dari workspace.
    Gunakan tool ini ketika user meminta membaca isi suatu file.

    Args:
        filename: Nama file yang ingin dibaca (contoh: 'catatan.txt')
    """
    try:
        path = _safe_path(filename)
        if not os.path.exists(path):
            return f"❌ File '{filename}' tidak ditemukan di workspace."
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        return f"📄 Isi file '{filename}':\n\n{content}"
    except ValueError as e:
        return f"❌ Error keamanan: {e}"
    except Exception as e:
        return f"❌ Gagal membaca file: {e}"


@tool
def update_file(filename: str, new_content: str) -> str:
    """
    Update / timpa isi file yang sudah ada di workspace.
    Gunakan tool ini ketika user meminta mengubah atau menambah isi file.

    Args:
        filename: Nama file yang akan diupdate (contoh: 'catatan.txt')
        new_content: Konten baru yang akan menggantikan isi file lama
    """
    try:
        path = _safe_path(filename)
        if not os.path.exists(path):
            return f"❌ File '{filename}' tidak ditemukan. Gunakan write_file untuk membuat file baru."
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        return f"✅ File '{filename}' berhasil diupdate."
    except ValueError as e:
        return f"❌ Error keamanan: {e}"
    except Exception as e:
        return f"❌ Gagal mengupdate file: {e}"


@tool
def delete_file(filename: str) -> str:
    """
    Hapus file dari workspace.
    Gunakan tool ini hanya ketika user secara eksplisit meminta penghapusan file.

    Args:
        filename: Nama file yang akan dihapus (contoh: 'catatan.txt')
    """
    try:
        path = _safe_path(filename)
        if not os.path.exists(path):
            return f"❌ File '{filename}' tidak ditemukan di workspace."
        os.remove(path)
        return f"🗑️ File '{filename}' berhasil dihapus dari workspace."
    except ValueError as e:
        return f"❌ Error keamanan: {e}"
    except Exception as e:
        return f"❌ Gagal menghapus file: {e}"


@tool
def create_directory(dirname: str) -> str:
    """
    Buat folder/direktori baru di dalam workspace.
    Gunakan tool ini ketika user meminta membuat folder baru.

    Args:
        dirname: Nama folder yang akan dibuat (contoh: 'proyek_baru' atau 'data/images')
    """
    try:
        # Resolve the path properly to allow nested directories like "data/images"
        safe_path = os.path.normpath(os.path.join(WORKSPACE_PATH, dirname))
        
        # Security check: must be inside WORKSPACE_PATH
        if not safe_path.startswith(os.path.abspath(WORKSPACE_PATH)):
            return f"❌ Error keamanan: Akses ditolak. '{dirname}' berada di luar workspace."
            
        if os.path.exists(safe_path):
            return f"⚠️ Folder '{dirname}' sudah ada di workspace."
            
        os.makedirs(safe_path, exist_ok=True)
        return f"📁 Folder '{dirname}' berhasil dibuat di workspace."
    except Exception as e:
        return f"❌ Gagal membuat folder: {e}"


@tool
def list_files() -> str:
    """
    Tampilkan daftar semua file yang ada di workspace.
    Gunakan tool ini ketika user bertanya file apa saja yang ada.
    """
    try:
        os.makedirs(WORKSPACE_PATH, exist_ok=True)
        files = os.listdir(WORKSPACE_PATH)
        if not files:
            return "📂 Workspace kosong, belum ada file."
        file_list = "\n".join(f"  • {f}" for f in sorted(files))
        return f"📂 File di workspace ({len(files)} file):\n{file_list}"
    except Exception as e:
        return f"❌ Gagal membaca workspace: {e}"
