import pennylane as qml
from pennylane import numpy as np
import matplotlib.pyplot as plt

def random_scenario_settings():
    # np.random.seed(3)
    preparation_settings = np.random.random(2)
    measurement_settings = np.random.random(4)
    
    return np.array(preparation_settings.tolist()+measurement_settings.tolist())

chsh_dev = qml.device("default.qubit", wires=2)

@qml.qnode(chsh_dev)
def chsh_correlator(settings): 
    qml.RY(settings[0], wires=[0])
    qml.RY(settings[1], wires=[1])
    qml.CNOT(wires=[0, 1])
    
    qml.RY(settings[2], wires=[0])
    qml.RY(settings[3], wires=[1])
    
    return qml.expval(qml.PauliZ(0) @ qml.PauliZ(1))

def chsh_cost(scenario_settings):
    value = 0
    for x in range(2):
        for y in range(2):
            qnode_settings = np.array([
                *scenario_settings[:2],
                scenario_settings[2+x],
                scenario_settings[4+y],
            ])
            value += (-1)**(x * y) * chsh_correlator(qnode_settings)
    return -(value)

init_settings = random_scenario_settings()

num_steps = 20
step_size = 0.3

opt = qml.GradientDescentOptimizer(stepsize=step_size)

values = []
settings_list = []

for i in range(num_steps):
    
    value = -(chsh_cost(init_settings))
    values.append(value)
    settings_list.append(init_settings)
    
    if i % 5 == 0:
        print("iteration : ", i, ", value : ", value)
    
    init_settings = opt.step(chsh_cost, init_settings)


final_value = -(chsh_cost(init_settings))
values.append(final_value)
settings_list.append(init_settings)
    
max_value = max(values)
max_id = values.index(max_value)
opt_settings = settings_list[max_id]

print("max value : ", max_value)
print("optimal settings : ", opt_settings, "\n")
print("theoretical max : ", 2 * np.sqrt(2), "\n")

plt.plot(range(num_steps + 1), values, "o--", label="Optimization")
plt.plot(range(num_steps + 1), [2]*len(range(num_steps + 1)), label="Classical upperbound")
plt.plot(range(num_steps + 1), [2*np.sqrt(2)]*len(range(num_steps + 1)), label="Quantum upperbound")

plt.title("Optimization of CHSH Violation\n")
plt.ylabel("CHSH value")
plt.xlabel("Iteration")
plt.legend()

plt.show()