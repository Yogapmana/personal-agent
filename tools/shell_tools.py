"""
tools/shell_tools.py — Tool untuk mengeksekusi perintah shell/terminal.
"""
import subprocess
from langchain.tools import tool

@tool
def execute_shell_command(command: str) -> str:
    """
    Mengeksekusi perintah shell atau terminal di sistem operasi dan mengembalikan outputnya.
    Gunakan tool ini jika Anda perlu menginstal paket (pip/apt), menjalankan skrip, mengelola file tingkat lanjut, atau memeriksa environment.
    
    Args:
        command (str): Perintah bash/shell yang ingin dieksekusi. Contoh: 'ls -la', 'pip install requests', 'ping -c 4 google.com'.
        
    Returns:
        str: Output dari perintah (stdout) atau pesan error (stderr).
    """
    try:
        # Menjalankan perintah dengan timeout 60 detik untuk mencegah proses menggantung
        result = subprocess.run(
            command,
            shell=True,
            check=False,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        output = result.stdout.strip()
        error = result.stderr.strip()
        
        if result.returncode == 0:
            return output if output else "Perintah berhasil dieksekusi tanpa output."
        else:
            return f"Error eksekusi (Exit code {result.returncode}):\n{error}\nOutput:\n{output}"
            
    except subprocess.TimeoutExpired:
        return "Gagal: Eksekusi perintah melebihi batas waktu (timeout 60 detik)."
    except Exception as e:
        return f"Gagal mengeksekusi perintah: {str(e)}"
