import numpy as np
import os
import sys
sys.path.append(os.path.expanduser('/root/Demo'))
sys.path.append('/home/junghee/hybrid_client/kq-client/kisti_clientpkg')
from saoovqe import *
from qiskit_nature.second_q.mappers import ParityMapper
from popup import show_popup, gui_setup, show_image_popup
from submit_file import submit_file
from job_mgmt import run_kriss_emul
from download_file import download_file
import matplotlib
matplotlib.use('Agg')  # Switch to a non-GUI backend like Agg
import matplotlib.pyplot as plt

import time

def run_LiH(root):
    time.sleep(10)
    start = time.time()

    thresh = 1.0e-6
    maxiter = 20
    

    result = []
    plot_result = []
    combined_points = []

    # Generate initial MO Integrals
    parity_mapper = ParityMapper(num_particles=(1, 1))
    fci_dump = 'FCIDUMP'
    json_init_file_path = 'LiH_init.json'
    json_file_path = 'LiH.json'
    solver = SA_OO_SSVQE(json_file_path=json_init_file_path, fci_dump=fci_dump, mapper=parity_mapper)
    hamiltonian_dir = 'hamiltonian.txt'
    

    ### hybrid_client interface ###
    submit_file(hamiltonian_dir)
    noti1 = f"HAMILTONIAN"
    root.after(0, show_popup, root, noti1, 800, 200, 'lightblue')
    ### hybrid_client interface ###
    
    
    circuits = solver.prepare_states(filter_triplets=True, ground_state_only=True)
    score_init = 0
    score_best = 0

    E_qpu = []
    E_OO = []
    indices_qpu = []
    indices_OO = []

    for iter in range(1, maxiter + 1):
        print(f"Iteration {iter}")
        
        ### hybrid_client interface ### 
        emul_file_name = "phoem.py"
        val = run_kriss_emul(emul_file_name)
        #print("return ", val)

        download_file1 = 'noref_0_0.rdm1'
        download_file(download_file1)
        noti2 = f"RESULTS"
        root.after(0, show_popup, root, noti2, 800, 700, 'lightgreen')

        download_file2 = 'noref_0_0.rdm2'
        download_file(download_file2)
        #noti3 = f"{download_file2} 파일을 받았습니다!!!"
        #root.after(0, show_popup, root, noti3, 1500, 300, 'lightgreen')
      
        download_file3 = 'min_eigenvalue.txt'
        download_file(download_file3)
        #noti4 = f"{download_file3} 파일을 받았습니다!!!"
        #root.after(0, show_popup, root, noti4, 1500, 300, 'lightgreen')

        download_file4 = 'cost_function_plot.png'
        download_file(download_file4)
        #noti5 = f"{download_file4} 파일을 받았습니다!!!"
        root.after(0, show_image_popup, root, download_file4, 1500, 80)

        time.sleep(3)

        ### hybrid_client interface ###
        solver.import_rdms_from_noref(file_path="noref_0_0")
        energy = solver.import_eigenvalue(file_path="min_eigenvalue.txt")
        score = energy
        E_qpu.append(energy)
        update = solver.update_problem(json_file_path)
        ### hybrid_client interface ###
        submit_file(hamiltonian_dir)
        noti1 = f"HAMILTONIAN"
        root.after(0, show_popup, root, noti1, 800, 200, 'lightblue')
        ### hybrid_client interface ###
        E_OO.append(update)

        if iter > 1:
            score_best = solver.import_eigenvalue(file_path="min_eigenvalue.txt")
            print(f"Energy Difference : {np.abs(score_best - score)}")
        else:
            score_init = score
        opt_energies = solver.opt_energies

        
        if np.abs(score_best - score) < thresh:
            print("Convergence Reached.")
            print(f"Energy Difference : {np.abs(score_best - score)}")
            final_score = score
            final_energy = opt_energies
            result.append(final_score)
            result.append(final_energy)
            E_qpu.append(*final_energy)
            break
        if iter == maxiter:
            final_score = score
            final_energy = opt_energies
            print("SA-OO-VQE step is not converged!")
            print(f"Energy Difference : {np.abs(score_best - score)}")
            result.append(final_score)
            result.append(final_energy)
            E_qpu.append(*final_energy)
            break

        plot_result.append(update)
    
    # Export Energies to txt file
    # file_path = "energies.txt"
    interleaved = [item for pair in zip(E_qpu, E_OO) for item in pair]
    remaining = E_qpu[len(E_OO):] if len(E_qpu) > len(E_OO) else E_OO[len(E_qpu):]
    E_result = interleaved + remaining


    #expected_length = maxiter + 1
    #if len(E_result) < expected_length:
    #    E_result += E_result[-1] * (expected_length - len(E_result))
    print("E_OO = ", E_OO)
    print("E_qpu = ", E_qpu)
    print("E_result = ", E_result)

    #with open(file_path, "w") as file:
    # for E_1 in E_qpu:
    #     file.write(f"{str(E_1)} \n")
    # for E_2 in E_OO:
    #     file.write(f"{str(E_2)} \n")
        
    print("")
    print("Computational Results")
    print(f"Initial score (state-averaged) : {score_init:.10f}")
    print(f"Score (state-averaged) : {final_score:.10f} \nOptimized energies : {opt_energies}")
    end = time.time()
    print("--------------------------------------------------")
    print("Computational Time : {} seconds".format(end-start))

    for i in range(len(E_OO)):
        combined_points.append((2*i, E_qpu[i]))
        combined_points.append((2*i+1, E_OO[i]))

    combined_points.append((2*len(E_OO), E_qpu[-1]))

    for i in range(len(combined_points) -1 ):
        x_values = [combined_points[i][0], combined_points[i+1][0]]
        y_values = [combined_points[i][1], combined_points[i+1][1]]

        plt.plot(x_values, y_values, 'k--')

        
        if i % 2 == 0:
            #plt.plot(index, value, "ro-", label='E_qpu' if i==0 else "")
            plt.plot(combined_points[i][0], combined_points[i][1], 'ro')
        else:
            plt.plot(combined_points[i][0], combined_points[i][1], 'bo')
            #plt.plot(index, value, "bo-", label='E_OO' if i==1 else "")
    #plt.plot(range(maxiter*2+1), E_result, "o--", label="Optimization")
    #plt.plot(range(maxiter), E_OO, "o--", label="Optimization_cpu")
    #plt.plot(range(maxiter+1), E_qpu, "o--", label="Optimization_qpu")
    #plt.plot(range(maxiter + 1), [2]*len(range(maxiter + 1)), label="Classical upperbound")
    #plt.plot(range(maxiter + 1), [2*np.sqrt(2)]*len(range(maxiter + 1)), label="Quantum upperbound")#

    plt.plot(combined_points[-1][0], combined_points[-1][1], 'ro')

    plt.plot([],[], 'ro', label="E_qpu")
    plt.plot([],[], 'bo', label="E_OO")

    plt.title("Optimized energies\n")
    plt.ylabel("Energy (Hartree)", labelpad=20, fontsize=8)
    plt.subplots_adjust(left=0.2)
    plt.xlabel("Iteration")
    plt.legend()

    #plt.show()
    plt.savefig('optimized_orbital_rb.png')
    #plt.savefig('optimized_qpu.png')

    # Optionally, display the plot in your GUI later
    root.after(0, show_image_popup, root, 'optimized_orbital_rb.png', 500, 200, 900, 650, 1000000000000)

    time.sleep(1000)



if __name__ == "__main__":
    gui_setup(run_LiH) 
