import requests, json
import json, time, requests
from sqlalchemy.orm import Session
from qiskit import QuantumCircuit, transpile
from .rabbitmq_utils import rabbitmq_update_cpu_iter, rabbitmq_check_qpu_iter, rabbitmq_update_job_status

server_url = "http://150.183.117.145:8001"
headers = {
    "Content-Type": "application/json"
}

def submit_file():
    file_path = input("Enter a file name or file path [ex) ./files/tmp.csv]: ").strip()

    with open(file_path, 'r') as file:
        data = list(file)
        print("file_data = ", data)
    
    payload = {
        "json_data": data,
        "filename" : file_path
    }
    response = requests.post(f"{server_url}/files/", json=payload)
    print("data sent: ", response.status_code)

    
    
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

#def submit_hybrid_job(jobInfo: schemas.JobCreate, db: Session, jobUUID: str):
def submit_hybrid_job():
    #resource_info.setStatus(False)
    #rabbitmq_update_job_status(jobUUID, "SUBMITTED")
    #crud.update_job_status(
    #    db=db,
    #    jobStatus=schemas.JobUpdateStatus(uuid=jobUUID, status="RUNNING"),
    #)
    #rabbitmq_update_job_status(jobUUID, "RUNNING")
    #result = excute_qiskit_circuit_to_qasm(jobInfo)
    
    
    ##### 여기서부터 사용자 hybrid 알고리즘
    sum = 0
    cpu_iter = 0


    for i in range(3):
        if cpu_iter == 0:
            cpu_iter = cpu_iter + 1        ## CPU_iter 증가시킴
            ### cpu job 
            print("~~~start cpu job~~~")
            ## qpu circuit send
            print("~~~qpu circuit send~~~")
            rabbitmq_update_cpu_iter(cpu_iter)    ## 메시지큐에 cpu_iter 전달하고 == QPU run 
            #time.sleep(5)
            qpu_iter = rabbitmq_check_qpu_iter()
            time.sleep(10)
            print("qpu_iter: ", qpu_iter)
        
        else:
            #qpu_iter = rabbitmq_check_qpu_iter()
            #print("qpu_iter: ", qpu_iter)
            if cpu_iter == qpu_iter:
                print("cpu_iter == qpu_iter")

                cpu_iter = cpu_iter + 1
                ## cpu job
                sum = sum + i
                print("sum = ", sum)
                rabbitmq_update_cpu_iter(cpu_iter)
                time.sleep(5)
                ## qpu running...
                qpu_iter = rabbitmq_check_qpu_iter()
                time.sleep(10)
            else:
                print("error....")
                
    ### 여기까지 사용자 알고리즘을 위한 코드 부분
                
    #crud.update_job_result(
    #    db=db,
    #    jobOutputObj=schemas.JobUpdateResultfile(
    #        uuid=jobUUID,
    #        status="SUCCESS",
    #        result_file=json.dumps(result, indent=2),
    #    ),
    #)
    #rabbitmq_update_job_status(jobUUID, "SUCCESS")
    #resource_info.setStatus(True)    
        

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
