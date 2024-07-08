import argparse
import json, time, csv, requests
from app.db import crud, schemas
from app.libs.resource import resource_info
from sqlalchemy.orm import Session
from qiskit import QuantumCircuit, transpile

from app.libs.mq_pub_con import RabbitPublisher, QueueInformation, RabbitConsumer



server_url = "http://150.183.117.145:8001"
headers = {
    "Content-Type": "application/json"
}

RABBITMQ_INFO = {
    "host": "localhost",
    "port": 5672,
    "username": "admin",
    "password": "admin",
    "exchange": "kisti.quantum.computing",
    "routekey": "quantum.job.status",
}

RABBITMQ_CPU_ITERQ = {
    "host": "localhost",
    "port": 5672,
    "username": "admin",
    "password": "admin",
    "exchange": "kisti.quantum.computing",
    "routekey": "cpu_iter",
}

RABBITMQ_QPU_ITERQ = {
    "host": "localhost",
    "port": 5672,
    "username": "admin",
    "password": "admin",
    "exchange": "kisti.quantum.computing",
    "routekey": "qpu_iter",
}


queue = (
    QueueInformation.builder()
    .host(RABBITMQ_INFO["host"])
    .port(RABBITMQ_INFO["port"])
    .username(RABBITMQ_INFO["username"])
    .password(RABBITMQ_INFO["password"])
    .exchange(RABBITMQ_INFO["exchange"])
    .build()
)

cpu_iter_queue = (
    QueueInformation.builder()
    .host(RABBITMQ_CPU_ITERQ["host"])
    .port(RABBITMQ_CPU_ITERQ["port"])
    .username(RABBITMQ_CPU_ITERQ["username"])
    .password(RABBITMQ_CPU_ITERQ["password"])
    .exchange(RABBITMQ_CPU_ITERQ["exchange"])
    .build()
)

qpu_iter_queue = (
    QueueInformation.builder()
    .host(RABBITMQ_QPU_ITERQ["host"])
    .port(RABBITMQ_QPU_ITERQ["port"])
    .username(RABBITMQ_QPU_ITERQ["username"])
    .password(RABBITMQ_QPU_ITERQ["password"])
    .exchange(RABBITMQ_QPU_ITERQ["exchange"])
    .build()
)


def rabbitmq_update_job_status(jobUUID: str, satatus: str):
    payload = {
        "jobUUID": jobUUID,
        "status": satatus,
    }
    body = json.dumps(payload)
    RabbitPublisher(queue).publish(RABBITMQ_INFO["routekey"], body)


def rabbitmq_update_cpu_iter(iter: int):
    payload = {
        "iter": iter
    }
    body = json.dumps(payload)
    RabbitPublisher(cpu_iter_queue).publish(RABBITMQ_CPU_ITERQ["routekey"], body)


def rabbitmq_check_qpu_iter():
    #RabbitConsumer(qpu_iter_queue).consume('qpu_iter_queue')
    return RabbitConsumer(qpu_iter_queue).consume('qpu_iter_queue')


### submit hybrid job to HPC Computer ###
def submit_QC_file(server_url, file_1, file_2):

    data = []
    with open(file_1, 'r') as f1:
        reader = csv.DictReader(f1)
        data = list(reader)

    csv_json_string = json.dumps(data)

    response = requests.post(server_url, headers=headers, data=csv_json_string)
    print("response: ", response)


    c_data = []
    with open(file_2, 'r') as f2:
        lines = f2.readlines()
    
    c_data = {"qasm_code": lines}

    with open("output.json", 'w') as output_f:
        json.dump(c_data, output_f, indent=4)
        
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


def submit_QC_hybridjob(jobInfo: schemas.JobCreate, db: Session, jobUUID: str):
    resource_info.setStatus(False)
    rabbitmq_update_job_status(jobUUID, "SUBMITTED")
    cpu_iter = 0
    url = "http://150.183.117.145:8001"
    headers = {
        "Content-Type": "application/json"
    }

    crud.update_job_status(
        db=db,
        jobStatus=schemas.JobUpdateStatus(uuid=jobUUID, status="RUNNING"),
    )
    rabbitmq_update_job_status(jobUUID, "RUNNING")

    #try:
    result = excute_qiskit_circuit_to_qasm(jobInfo) ## CPU에서
    sum = 0


    for i in range(5):
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

    crud.update_job_result(
        db=db,
        jobOutputObj=schemas.JobUpdateResultfile(
            uuid=jobUUID,
            status="SUCCESS",
            result_file=json.dumps(result, indent=2),
        ),
    )
    rabbitmq_update_job_status(jobUUID, "SUCCESS")

    resource_info.setStatus(True)


def main():
    parser = argparse.ArgumentParser(description="A Client Program for HPC & QC Hybrid Computing")
    parser.add_argument("-i", "--input_file", required=True, help="input file path")
    parser.add_argument("-q", "--qasm_file", required=True, help="qasm circuit file path")

    args = parser.parse_args()
    input_file_path = args.input_file
    qasm_file_path = args.qasm_file

    # 파일 내용을 JSON으로 변환
    with open(input_file_path, 'r') as csv_file:
        #reader = csv.DictReader(csv_file)
        csv_data = list(csv_file)

    print("csv_data = ", csv_data)

    with open(qasm_file_path, 'r') as qc_file:
        qasm_data = list(qc_file)

    print("qasm_data = ", qasm_data)


    job_data = {
        "type": "qasm",
        "shot": 1024,
        "input_file": 'OPENQASM 2.0; \ninclude "qelib1.inc"; \nqreg q[3]; \ncreg c[3]; \nrx(1.0) q[0]; \nry(0) q[0]; \nh q[0]; \ncx q[0], q[1]; \nz q[0]; \nmeasure q[0] -> c[0]; \nmeasure q[1] -> c[1]; \nmeasure q[2] -> c[2];'
    }

    response = requests.post("http://150.183.117.145:8001/job/", json=job_data)
    print("data sent:", response.status_code)


    csv_payload = {
        "json_data": csv_data,
        "filename": input_file_path
    }
    response = requests.post("http://150.183.117.145:8001/files/", json=csv_payload)
    print("data sent:", response.status_code)


    payload = {
        "json_data": qasm_data,
        "filename": qasm_file_path
    }
    qc_json_string = json.dumps(qasm_data)
    response = requests.post("http://150.183.117.145:8001/files/", json=payload)
    print("data sent:", response.status_code)

    sum = 0
    cpu_iter = 0


    for i in range(5):
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

    #except Exception as e:
    #    rabbitmq_update_job_status(jobUUID, "FAILED")
    #    crud.update_job_result(
    #        db=db,
    #        jobOutputObj=schemas.JobUpdateResultfile(
    #            uuid=jobUUID, status="FAILED", result_file=""
    #        ),
    #    )
    #    print(e)
    #    return -1



if __name__ == "__main__":
    main()
