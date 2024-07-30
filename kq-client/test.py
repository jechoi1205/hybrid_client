import numpy as np
import functions as fct
from kisti_clientpkg.submit_file import submit_file
from kisti_clientpkg.job_mgmt import run_kriss_emul

fci_file_name = "./kq-client/FCIDUMP"
submit_file(fci_file_name)

emul_file_name="test.py"
run_kriss_emul(emul_file_name)

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
