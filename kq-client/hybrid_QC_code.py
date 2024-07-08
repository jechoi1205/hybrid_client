from kisti_clientpkg.mq import rabbitmq_check_cpu_iter
from kisti_clientpkg.mq import rabbitmq_update_cpu_iter
from kisti_clientpkg.mq import rabbitmq_check_qpu_iter
from kisti_clientpkg.mq import rabbitmq_update_qpu_iter

import requests



def main():

    max_iter = 50
    cpu_iter = 0
    api_server_url = "http://127.0.0.1:8080" ## http://150.183.117.168:8000

    response = requests.post(api_server_url+"/files/")

    for i in range(max_iter):
        rabbitmq_update_cpu_iter(cpu_iter)



if __name__ == "__main__":
    main()