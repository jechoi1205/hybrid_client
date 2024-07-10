import requests

server_url = "http://150.183.117.145:8001"
headers = {
    "Content-Type": "application/json"
}

def submit_file():
    file_path = input("Enter a file name or file path [ex) ./example_files/tmp.csv]: ").strip()

    with open(file_path, 'r') as file:
        data = list(file)
        print("file_data = ", data)
    
    payload = {
        "json_data": data,
        "filename" : file_path
    }
    response = requests.post(f"{server_url}/files/", json=payload)
    print("data sent: ", response.status_code)
