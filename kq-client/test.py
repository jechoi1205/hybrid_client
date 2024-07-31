import numpy as np
import functions as fct
from kisti_clientpkg.submit_file import submit_file
from kisti_clientpkg.job_mgmt import run_kriss_emul
from kisti_clientpkg.rabbitmq_utils import rabbitmq_check_cpu_iter, rabbitmq_check_qpu_iter, rabbitmq_update_cpu_iter
from kisti_clientpkg.download_file import download_file
import time

fci_file_name = "./kq-client/FCIDUMP"
#submit_file(fci_file_name)

emul_file_name="test.py"
#run_kriss_emul(emul_file_name)

download_file1 = 'noref_0_0.rdm1'
download_file2 = 'noref_0_0.rdm2'

sum = 0
cpu_iter = 0
for i in range(2):
    cpu_iter += 1
    # FCIDUMP file update?
    # 파일을 다시 전송할지? 데이터만 보낼지?
    submit_file(fci_file_name)
    time.sleep(3)  
    #rabbitmq_update_cpu_iter(cpu_iter)
    
    run_kriss_emul(emul_file_name)
    #qpu_iter = rabbitmq_check_qpu_iter()   
    time.sleep(3)
    download_file(download_file1)
    time.sleep(3)
    download_file(download_file2)
   

# Import qubit Hamiltonian
#fct.read_fcidump('FCIDUMP')

# Export rdm1
#new_file_path_1 = 'noref_0_0.rdm1'
#fct.generate_random_matrix_file(new_file_path_1)
#print(f"Generated {new_file_path_1} with random matrix values.")

# Export rdm2
#new_file_path_2 = 'noref_0_0.rdm2'
#fct.generate_random_tensor_file(new_file_path_2)
#print(f"Generated {new_file_path_2} with random tensor values.")
#print("\n")
