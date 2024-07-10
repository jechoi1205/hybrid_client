import requests
from rich.console import Console

console = Console()
server_url = "http://150.183.117.145:8001"

def submit_file():
    file_path = console.input("[bold cyan]Enter a file name or file path [ex) ./files/tmp.csv]:[/] ").strip()

    with open(file_path, 'r') as file:
        data = list(file)
        console.print(f"[bold blue]file_data =[/] {data}")
    
    payload = {
        "json_data": data,
        "filename": file_path
    }
    response = requests.post(f"{server_url}/files/", json=payload)
    if response.status_code == 202:
        console.print("[bold green]data sent successfully![/]")
    else:
        console.print(f"[bold red]Failed to send data: {response.status_code}[/]")
