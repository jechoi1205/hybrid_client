import qiskit
from qiskit.quantum_info import SparsePauliOp
from qiskit.circuit.library import EfficientSU2
import numpy as np
from qiskit_algorithms.optimizers import SPSA
from qiskit.providers.basic_provider import BasicSimulator  # local simulator
from qiskit_algorithms import VQE
from qiskit.primitives import Estimator
import logging

logger = logging.getLogger(__name__)

# 로거 설정
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


num_qubits = 2
hamiltonian = SparsePauliOp.from_list(
    [("YZ", 0.3980), ("ZI", -0.3980)]
)
target_energy = -1


# the rotation gates are chosen randomly, so we set a seed for reproducibility
ansatz = EfficientSU2(num_qubits, reps=1, entanglement='linear', insert_barriers=True) 
#ansatz.draw('mpl', style='iqx')


optimizer = SPSA(maxiter=5)

np.random.seed(10)  # seed for reproducibility
initial_point = np.random.random(ansatz.num_parameters)


intermediate_info = {
    'nfev': [],
    'parameters': [],
    'energy': [],
    'stddev': []
}

## 중간정보를 저장하는 콜백함수
## 최적화 과정중에 호출됨
## 현재 함수의 evaluation 횟수
## 파라미터, 에너지, 표준편차를 출력하고 저장함

def callback(nfev, parameters, energy, stddev):
    ##print("QPU")
    print(f"Callback called: nfev={nfev}, energy={energy}, stddev={stddev}")
    intermediate_info['nfev'].append(nfev)
    intermediate_info['parameters'].append(parameters)
    intermediate_info['energy'].append(energy)
    intermediate_info['stddev'].append(stddev)
    if isinstance(stddev, (int, float)):
        intermediate_info['stddev'].append(stddev)
    else:
        intermediate_info['stddev'].append(None)
    
## VQE 인스턴스 생성 (ansatz, 최적화 알고리즘, 초기값, estimator, 콜백함수를 전달하고)
local_vqe = VQE(ansatz=ansatz,
                optimizer=optimizer,
                initial_point=initial_point,
                estimator=Estimator(),
                quantum_instance=BasicSimulator(),
                callback=callback)

## 헤밀토니안 행렬의 최소 eigenvalue를 계산함
logger.info("Starting compute_minimum_eigenvalue():")
local_result = local_vqe.compute_minimum_eigenvalue(hamiltonian)


### 결과값 출력
print('Eigenvalue:', local_result.eigenvalue)
print('Target:', target_energy)
if any(intermediate_info['stddev']):
    mean_error = np.mean([x for x in intermediate_info['stddev'] if x is not None])
    print('Mean error:', mean_error)
else:
    print('No valid standard deviation data collected.')
