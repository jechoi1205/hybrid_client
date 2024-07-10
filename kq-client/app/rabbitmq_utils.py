import json
from app.libs.mq_pub_con import RabbitPublisher, QueueInformation, RabbitConsumer

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

def rabbitmq_update_job_status(jobUUID: str, status: str):
    payload = {"jobUUID": jobUUID, "status": status}
    body = json.dumps(payload)
    RabbitPublisher(queue).publish(RABBITMQ_INFO["routekey"], body)

def rabbitmq_update_cpu_iter(iter: int):
    payload = {"iter": iter}
    body = json.dumps(payload)
    RabbitPublisher(cpu_iter_queue).publish(RABBITMQ_CPU_ITERQ["routekey"], body)

def rabbitmq_check_qpu_iter():
    return RabbitConsumer(qpu_iter_queue).consume('qpu_iter_queue')