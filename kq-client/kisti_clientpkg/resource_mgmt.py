import requests
from rich import print_json
from dotenv import load_dotenv
import os

load_dotenv()

server_url = os.getenv("SERVER_URL")

def get_resource(p_flag: bool):
    try:
        response = requests.get(f"{server_url}/resource")
        response.raise_for_status()
        print("GET /resource Response:")
        if p_flag == True:
            print_json(data = response.json())
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def patch_resource():
    try:
        # 현재 리소스 상태 확인
        resource_info = get_resource(False)
        if resource_info is None:
            print("Failed to get resource information.")
            return

        details = resource_info.get('details', [])
        current_state = None
        for detail in details:
            if detail.get('name') == 'status':
                current_state = detail.get('value')
                break

        print(f"Current resource state: {current_state}")

        # 사용자가 입력한 자원 상태 (on/off)를 받음
        state_input = input("Enter resource state (on/off): ").strip().lower()
        if state_input == "on":
            change_state = "Online"
            state = True
        elif state_input == "off":
            change_state = "Offline"
            state = False
        else:
            print("Invalid input. Please enter 'on' or 'off'.")
            return

        # 현재 상태와 같으면 업데이트하지 않음
        if change_state == current_state:
            print("Resource state is already set to the desired state.")
            return

        # PATCH 요청을 보냄
        payload = {
            "state": state
        }
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.patch(
            f"{server_url}/resource",
            params={"state": state},
            headers={"accept": "application/json"}
        )
        response.raise_for_status()
        print("PATCH /resource Response: " + change_state)
        #print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
