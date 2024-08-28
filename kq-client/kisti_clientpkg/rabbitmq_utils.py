import json, os
from mq_pub_con import RabbitPublisher, QueueInformation, RabbitConsumer
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_INFO = {
    "host": os.getenv("RABBITMQ_HOST"),
    "port": int(os.getenv("RABBITMQ_PORT")),
    "username": os.getenv("RABBITMQ_USERNAME"),
    "password": os.getenv("RABBITMQ_PASSWORD"),
    "exchange": os.getenv("RABBITMQ_EXCHANGE"),
    "routekey": os.getenv("RABBITMQ_ROUTEKEY", "quantum.job.status"),
}

RABBITMQ_CPU_ITERQ = {
    "host": os.getenv("RABBITMQ_HOST"),
    "port": int(os.getenv("RABBITMQ_PORT")),
    "username": os.getenv("RABBITMQ_USERNAME"),
    "password": os.getenv("RABBITMQ_PASSWORD"),
    "exchange": os.getenv("RABBITMQ_EXCHANGE"),
    "routekey": "cpu_iter",
}

RABBITMQ_QPU_ITERQ = {
    "host": os.getenv("RABBITMQ_HOST"),
    "port": int(os.getenv("RABBITMQ_PORT")),
    "username": os.getenv("RABBITMQ_USERNAME"),
    "password": os.getenv("RABBITMQ_PASSWORD"),
    "exchange": os.getenv("RABBITMQ_EXCHANGE"),
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

def rabbitmq_update_job_status(jobUUID: str, status: str):
    payload = {"jobUUID": jobUUID, "status": status}
    body = json.dumps(payload)
    RabbitPublisher(queue).publish(RABBITMQ_INFO["routekey"], body)

def rabbitmq_update_cpu_iter(iter: int):
    payload = {"iter": iter}
    body = json.dumps(payload)
    RabbitPublisher(cpu_iter_queue).publish(RABBITMQ_CPU_ITERQ["routekey"], body)
    
def rabbitmq_update_qpu_iter(iter: int):
    payload = {
        "iter": iter
    }
    body = json.dumps(payload)
    RabbitPublisher(qpu_iter_queue).publish(RABBITMQ_QPU_ITERQ["routekey"], body)

def rabbitmq_check_qpu_iter():
    return RabbitConsumer(qpu_iter_queue).consume('qpu_iter_queue')

def rabbitmq_check_cpu_iter():
    return RabbitConsumer(cpu_iter_queue).consume('cpu_iter_queue')