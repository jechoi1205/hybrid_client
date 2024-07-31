import requests
from rich.console import Console
from dotenv import load_dotenv
import os

load_dotenv()

console = Console()
server_url = os.getenv("SERVER_URL")

current_working_dir = os.getcwd()
file_dir = os.path.join(current_working_dir, 'kq-client', 'storage', 'mywork')
file_dir_abs = os.path.abspath(file_dir)

def download_file(json_data):
    payload = {
        "filename": json_data
    }
    response = requests.get(f"{server_url}/kriss_emul_download/", json=payload)
    
    if response.status_code ==200:
        file_path = os.path.join(file_dir_abs, json_data)
        with open(file_path, 'wb') as f:
            f.write(response.content)