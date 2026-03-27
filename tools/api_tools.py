"""
tools/api_tools.py — Tool untuk mengirim permintaan HTTP (HTTP Request).
"""
import requests
import json
from langchain.tools import tool

@tool
def make_http_request(url: str, method: str = 'GET', headers_json: str = '{}', body_json: str = '{}') -> str:
    """
    Melakukan permintaan HTTP Request (GET, POST, PUT, DELETE) ke sebuah URL API atau layanan web.
    Gunakan tool ini jika agen perlu berinteraksi dengan API eksternal (misalnya cek cuaca, fetch JSON, dsb).
    
    Args:
        url (str): URL endpoint yang dituju.
        method (str, optional): HTTP Method (GET, POST, PUT, DELETE). Default: 'GET'.
        headers_json (str, optional): String berformat JSON yang merepresentasikan Dictionary header. Default: '{}'.
        body_json (str, optional): String berformat JSON yang merepresentasikan Dictionary payload/body. Default: '{}'.
        
    Returns:
        str: Hasil response HTTP berupa teks atau representasi JSON, atau pesan error.
    """
    try:
        # Parse JSON ke Dictionary
        headers = json.loads(headers_json)
        body = json.loads(body_json)
        
        # Validasi method
        method = method.upper()
        if method not in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD']:
            return "Metode HTTP tidak valid. Gunakan GET, POST, PUT, DELETE, dll."
            
        # Kirim HTTP Request
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            json=body if body else None,
            timeout=15 # Batas waktu 15 detik
        )
        
        # Ekstrak Status Code
        result = f"Status Code: {response.status_code}\\n"
        
        # Coba format response jika JSON
        try:
            result += "Response JSON:\\n"
            result += json.dumps(response.json(), indent=2)
        except json.JSONDecodeError:
            result += "Response Text:\\n"
            # Potong response jika terlalu panjang agar tidak merusak prompt
            text = response.text
            result += text[:2000] + ('...' if len(text) > 2000 else '')
            
        return result
    except json.JSONDecodeError:
        return "Gagal: Format `headers_json` atau `body_json` bukan JSON string yang valid."
    except requests.exceptions.RequestException as e:
        return f"Gagal mengirim request HTTP: {str(e)}"
    except Exception as e:
        return f"Error tidak dikenal: {str(e)}"
