"""
tools/system_monitor.py — Tool untuk memantau status sistem (CPU, RAM, Disk, GPU, Uptime, Network)
"""
import psutil
import time
import subprocess
from datetime import datetime
from langchain.tools import tool

@tool
def get_system_status() -> str:
    """
    Mengambil informasi status sistem saat ini secara menyeluruh.
    Mencakup CPU, RAM, Disk usage, GPU usage (via nvidia-smi), Network I/O, dan Uptime.
    Gunakan tool ini ketika pengguna bertanya tentang kondisi sistem, performa server, penggunaan RAM, CPU, kapasitas disk, GPU, atau jaringan.
    
    Returns:
        str: Laporan teks berisi data pemantauan sistem yang komprehensif.
    """
    try:
        # Uptime
        boot_time_timestamp = psutil.boot_time()
        bt = datetime.fromtimestamp(boot_time_timestamp).strftime("%Y-%m-%d %H:%M:%S")
        uptime_seconds = time.time() - boot_time_timestamp
        uptime_hours = int(uptime_seconds // 3600)
        uptime_minutes = int((uptime_seconds % 3600) // 60)
        
        # CPU
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count_logical = psutil.cpu_count(logical=True)
        cpu_count_physical = psutil.cpu_count(logical=False)
        
        # Memory
        mem = psutil.virtual_memory()
        mem_total_gb = mem.total / (1024**3)
        mem_used_gb = mem.used / (1024**3)
        mem_percent = mem.percent
        
        # Disk
        disk = psutil.disk_usage('/')
        disk_total_gb = disk.total / (1024**3)
        disk_used_gb = disk.used / (1024**3)
        disk_percent = disk.percent
        
        # Network
        net_io = psutil.net_io_counters()
        bytes_sent_mb = net_io.bytes_sent / (1024**2)
        bytes_recv_mb = net_io.bytes_recv / (1024**2)
        
        # GPU (via nvidia-smi)
        gpu_info = ""
        try:
            # Query nvidia-smi for specific fields
            nvidia_cmd = [
                "nvidia-smi", 
                "--query-gpu=index,name,utilization.gpu,memory.used,memory.total,temperature.gpu", 
                "--format=csv,noheader,nounits"
            ]
            result = subprocess.run(nvidia_cmd, capture_output=True, text=True, check=True)
            lines = result.stdout.strip().split('\\n')
            if lines and lines[0]:
                for line in lines:
                    idx, name, util, mem_used, mem_total, temp = [x.strip() for x in line.split(',')]
                    gpu_info += f"  - GPU {idx} ({name}): Load {util}%, Mem {mem_used}MB/{mem_total}MB, Temp {temp}°C\n"
            else:
                gpu_info = "  - Tidak ada informasi GPU dari nvidia-smi\n"
        except (subprocess.CalledProcessError, FileNotFoundError):
            gpu_info = "  - nvidia-smi tidak ditemukan atau gagal dijalankan (mungkin driver GPU belum terinstal)\n"


        report = (
            f"💻 System Status Report:\n\n"
            f"⏱️ Uptime & Boot Time:\n"
            f"  - Boot Time: {bt}\n"
            f"  - Uptime: {uptime_hours} Jam {uptime_minutes} Menit\n\n"
            f"🧠 CPU:\n"
            f"  - Usage: {cpu_percent}%\n"
            f"  - Cores: {cpu_count_physical} Physical, {cpu_count_logical} Logical\n\n"
            f"💾 RAM:\n"
            f"  - Usage: {mem_used_gb:.2f} GB / {mem_total_gb:.2f} GB ({mem_percent}%)\n\n"
            f"💽 Disk (Root /):\n"
            f"  - Usage: {disk_used_gb:.2f} GB / {disk_total_gb:.2f} GB ({disk_percent}%)\n\n"
            f"🎮 GPU:\n{gpu_info}\n"
            f"🌐 Network I/O:\n"
            f"  - Data Sent: {bytes_sent_mb:.2f} MB\n"
            f"  - Data Received: {bytes_recv_mb:.2f} MB\n"
        )
        return report
    except Exception as e:
        return f"Error mengambil status sistem: {str(e)}"
