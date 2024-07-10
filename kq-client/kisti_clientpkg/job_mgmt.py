import requests
from sqlalchemy.orm import Session
from qiskit import QuantumCircuit, transpile

server_url = "http://150.183.117.145:8001"
headers = {
    "Content-Type": "application/json"
}
    
def check_job_manager():
    try:
        response = requests.get(f"{server_url}/job/")
        response.raise_for_status()
        print("GET /job/ Response:")
        print(response.json())
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

"""
def get_qreg_to_qasm(qasm_string: str):
    for line in qasm_string.split("\n"):
        line = line.rstrip()
        if line.startswith("qreg"):
            qreg_line = line.split(sep="[")
            qreg_num = qreg_line[1].split(sep="]")
            return int(qreg_num[0])


def get_creg_to_qasm(qasm_string: str):
    for line in qasm_string.split("\n"):
        line = line.rstrip()
        if line.startswith("qreg"):
            creg_line = line.split(sep="[")
            creg_num = creg_line[1].split(sep="]")
            return int(creg_num[0])
"""

"""
def excute_qiskit_circuit_to_qasm(jobInfo: schemas.JobCreate):
    circ = QuantumCircuit.from_qasm_str(jobInfo.input_file)

    creg = get_creg_to_qasm(jobInfo.input_file)
    qreg = get_qreg_to_qasm(jobInfo.input_file)

    meas = QuantumCircuit(qreg, creg)
    meas.barrier(range(qreg))
    meas.measure(range(qreg), range(creg))

    qc = meas.compose(circ, range(creg), front=True)

    backend = AerSimulator()
    qc_compiled = transpile(qc, backend)
    job_sim = backend.run(qc_compiled, shots=jobInfo.shot)

    simu_result = job_sim.result().to_dict()

    return {
        "backend_name": "KQ-Hardware",
        "backend_version": "0.0.1",
        "date": simu_result["date"],
        "success": simu_result["success"],
        "status": "success",
        "time_taken": simu_result["time_taken"],
        "results": [
            {
                "shots": simu_result["results"][0]["shots"],
                "data": simu_result["results"][0]["data"],
                "success": True,
                "status": "done",
                "header": simu_result["results"][0]["header"],
            }
        ],
    }
"""
        

def check_job_info(job_uuid):
    try:
        response = requests.get(f"{server_url}/job/{job_uuid}")
        response.raise_for_status()
        print(f"GET /job/{job_uuid} Response:")
        print(response.json())
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def delete_job(job_uuid):
    try:
        response = requests.delete(f"{server_url}/job/{job_uuid}")
        response.raise_for_status()
        print(f"DELETE /job/{job_uuid} Response:")
        print(response.json())
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def get_job_status(job_uuid):
    try:
        response = requests.get(f"{server_url}/job/{job_uuid}/status/")
        response.raise_for_status()
        print(f"GET /job/{job_uuid}/status/ Response:")
        print(response.json())
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def get_job_result(job_uuid):
    try:
        response = requests.get(f"{server_url}/job/{job_uuid}/result/")
        response.raise_for_status()
        print(f"GET /job/{job_uuid}/result/ Response:")
        print(response.json())
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
