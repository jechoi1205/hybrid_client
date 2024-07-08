import json

from .mq_pub_con import RabbitConsumer, RabbitPublisher, QueueInformation

RABBITMQ_CPU_ITERQ = {
    "host": "150.183.117.145",
    "port": 5672,
    "username": "admin",
    "password": "admin",
    "exchange": "kisti.quantum.computing",
    "routekey": "cpu_iter",
}


RABBITMQ_QPU_ITERQ = {
    "host": "150.183.117.145",
    "port": 5672,
    "username": "admin",
    "password": "admin",
    "exchange": "kisti.quantum.computing",
    "routekey": "qpu_iter",
}


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


def rabbitmq_update_cpu_iter(iter: int):
    payload = {
        "iter": iter
    }
    body = json.dumps(payload)
    RabbitPublisher(cpu_iter_queue).publish(RABBITMQ_CPU_ITERQ["routekey"], body)

def rabbitmq_update_qpu_iter(iter: int):
    payload = {
        "iter": iter
    }
    body = json.dumps(payload)
    RabbitPublisher(qpu_iter_queue).publish(RABBITMQ_QPU_ITERQ["routekey"], body)

def rabbitmq_check_qpu_iter():
    #RabbitConsumer(qpu_iter_queue).consume('qpu_iter_queue')
    return RabbitConsumer(qpu_iter_queue).consume('qpu_iter_queue')


def rabbitmq_check_cpu_iter():
    #RabbitConsumer(cpu_iter_queue).consume('cpu_iter_queue')
    return RabbitConsumer(cpu_iter_queue).consume('cpu_iter_queue')
