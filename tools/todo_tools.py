"""
tools/todo_tools.py — Tool untuk manajemen To-Do List agent.
"""
import json
import os
from datetime import datetime
from langchain.tools import tool

TODO_FILE = "workspace/todo_list.json"

def _ensure_workspace():
    """Memastikan folder workspace ada."""
    if not os.path.exists("workspace"):
        os.makedirs("workspace")

def _load_todos():
    """Memuat daftar tugas dari file JSON."""
    _ensure_workspace()
    if not os.path.exists(TODO_FILE):
        return []
    try:
        with open(TODO_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def _save_todos(todos):
    """Menyimpan daftar tugas ke file JSON."""
    _ensure_workspace()
    with open(TODO_FILE, "w") as f:
        json.dump(todos, f, indent=4)

@tool
def add_todo(task: str, priority: str = "Sedang", deadline: str = "Tidak ada") -> str:
    """
    Menambahkan tugas baru ke dalam to-do list.
    
    Args:
        task (str): Deskripsi tugas (contoh: "Beli kopi", "Kirim email ke bos").
        priority (str): Tingkat prioritas (Tinggi, Sedang, Rendah). Default: "Sedang".
        deadline (str): Tenggat waktu penyelesaian tugas (contoh: "Besok jam 10 pagi", "2023-10-31 17:00"). Default: "Tidak ada".
        
    Returns:
        str: Pesan konfirmasi berhasil atau gagal.
    """
    todos = _load_todos()
    new_id = 1 if not todos else max(t.get("id", 0) for t in todos) + 1
    
    new_task = {
        "id": new_id,
        "task": task,
        "priority": priority,
        "deadline": deadline,
        "status": "pending",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    todos.append(new_task)
    _save_todos(todos)
    return f"Berhasil menambahkan tugas '{task}' (ID: {new_id}, Prioritas: {priority}, Deadline: {deadline})."

@tool
def view_todos(status: str = "pending") -> str:
    """
    Melihat daftar tugas (to-do list). Gunakan ini untuk menganalisis tugas dan merekomendasikan apa yang harus dikerjakan user berdasarkan prioritas dan deadline.
    
    Args:
        status (str): Filter status tugas ("pending", "selesai", atau "semua"). Default: "pending".
        
    Returns:
        str: Daftar tugas dalam format teks, atau pesan jika kosong.
    """
    todos = _load_todos()
    if not todos:
        return "To-do list saat ini kosong. Tidak ada tugas yang perlu dikerjakan."
        
    filtered = todos
    if status.lower() != "semua":
        filtered = [t for t in todos if t.get("status") == status.lower()]
        
    if not filtered:
        return f"Tidak ada tugas dengan status '{status}'."
        
    result = f"Daftar Tugas ({status}):\n"
    for t in filtered:
        result += f"- [ID: {t['id']}] {t['task']} | Prioritas: {t['priority']} | Deadline: {t['deadline']} | Status: {t['status']}\n"
        
    return result

@tool
def update_todo_status(task_id: int, new_status: str) -> str:
    """
    Memperbarui status sebuah tugas (misalnya mengubah menjadi 'selesai').
    
    Args:
        task_id (int): ID dari tugas yang ingin diubah statusnya.
        new_status (str): Status baru (contoh: "selesai", "pending").
        
    Returns:
        str: Pesan konfirmasi berhasil atau gagal.
    """
    todos = _load_todos()
    for t in todos:
        if t.get("id") == task_id:
            old_status = t.get("status")
            t["status"] = new_status.lower()
            _save_todos(todos)
            return f"Berhasil mengubah status tugas ID {task_id} dari '{old_status}' menjadi '{new_status}'."
    return f"Gagal: Tugas dengan ID {task_id} tidak ditemukan."

@tool
def delete_todo(task_id: int) -> str:
    """
    Menghapus tugas dari to-do list berdasarkan ID.
    
    Args:
        task_id (int): ID dari tugas yang ingin dihapus.
        
    Returns:
        str: Pesan konfirmasi berhasil atau gagal.
    """
    todos = _load_todos()
    initial_length = len(todos)
    todos = [t for t in todos if t.get("id") != task_id]
    
    if len(todos) < initial_length:
        _save_todos(todos)
        return f"Berhasil menghapus tugas dengan ID {task_id}."
    return f"Gagal: Tugas dengan ID {task_id} tidak ditemukan."
