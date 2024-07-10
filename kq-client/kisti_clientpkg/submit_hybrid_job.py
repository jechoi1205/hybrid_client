import time
import requests
from .rabbitmq_utils import rabbitmq_update_cpu_iter, rabbitmq_check_qpu_iter, rabbitmq_update_job_status


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
                
    print("~~~cpu job end~~~")
                
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