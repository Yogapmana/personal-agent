"""
tools/__init__.py — Ekspor semua tool ke agent
"""
from tools.file_io import (
    write_file,
    read_file,
    update_file,
    delete_file,
    create_directory,
    list_files,
)
from tools.web_search import (
    internet_search,
    scrape_url,
    get_current_datetime,
)
from tools.system_monitor import get_system_status
from tools.image_tools import search_and_download_image
from tools.pdf_tools import create_pdf
from tools.reminder_tools import set_reminder
from tools.shell_tools import execute_shell_command
from tools.api_tools import make_http_request
from tools.selenium_tools import advanced_scrape_url
from tools.todo_tools import add_todo, view_todos, update_todo_status, delete_todo

ALL_TOOLS = [
    write_file,
    read_file,
    update_file,
    delete_file,
    create_directory,
    list_files,
    internet_search,
    scrape_url,
    get_current_datetime,
    get_system_status,
    search_and_download_image,
    create_pdf,
    set_reminder,
    execute_shell_command,
    make_http_request,
    advanced_scrape_url,
    add_todo,
    view_todos,
    update_todo_status,
    delete_todo,
]
