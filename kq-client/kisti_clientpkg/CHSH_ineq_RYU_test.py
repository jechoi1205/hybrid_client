import pennylane as qml
from pennylane import numpy as np
import matplotlib.pyplot as plt
from .rabbitmq_utils import rabbitmq_update_cpu_iter, rabbitmq_check_qpu_iter, rabbitmq_update_job_status
from .job_mgmt import run_emul
from .CHSH_emulator import chsh_correlator
from pennylane._grad import numerical_grad

chsh_dev = qml.device("default.qubit", wires=2)

class GradientDescentOptimizer:
    def __init__(self, stepsize=0.01):
        self.stepsize = stepsize

    def step(self, objective_fn, *args, grad_fn=None, **kwargs):
        g, _ = self.compute_grad(objective_fn, args, kwargs, grad_fn=grad_fn)
        new_args = self.apply_grad(g, args)
        if len(new_args) == 1:
            return new_args[0]
        return new_args

    @staticmethod
    def compute_grad(objective_fn, args, kwargs, grad_fn=None):
        g = numerical_grad(objective_fn)
        grad = g(*args, **kwargs)
        forward = getattr(g, "forward", None)
        num_trainable_args = sum(getattr(arg, "requires_grad", False) for arg in args)
        grad = (grad,) if num_trainable_args == 1 else grad
        return grad, forward

    def apply_grad(self, grad, args):
        args_new = list(args)
        trained_index = 0
        for index, arg in enumerate(args):
            if getattr(arg, "requires_grad", False):
                args_new[index] = arg - self.stepsize * grad[trained_index]
                trained_index += 1
        return args_new
    
    

def tensor_to_list(tensor):
    if isinstance(tensor, np.ndarray):
        return tensor.tolist()
    elif hasattr(tensor, '_value'):
        return np.array(tensor._value).tolist()
    else:
        raise TypeError("Unsupported type for tensor_to_list")
    
def list_to_tensor(lst):
    if isinstance(lst, list):
        return np.array(lst)
    else:
        raise TypeError("Unsupported type for list_to_tensor. Expected a list.")


def random_scenario_settings():
    # np.random.seed(3)
    preparation_settings = np.random.random(2)
    measurement_settings = np.random.random(4)
    return np.array(preparation_settings.tolist()+measurement_settings.tolist())

@qml.qnode(chsh_dev)
def chsh_cost(scenario_settings):
    if len(scenario_settings) < 6:
        raise ValueError("scenario_settings must have at least 6 elements.")
    
    value = 0.0
    for x in range(2):
        for y in range(2):
            qnode_settings = np.array([
                *scenario_settings[:2],
                scenario_settings[2+x],
                scenario_settings[4+y],
            ])

            #cpu_iter = cpu_iter + 1 
            #rabbitmq_update_cpu_iter(cpu_iter)
            #val = chsh_correlator(qnode_settings) #qpu
            data = tensor_to_list(qnode_settings)
            payload = {
                    "json_data": data
                }
            val_tmp = run_emul(payload)
            val_tmp = np.array(val_tmp,dtype=np.float64)
            #print("val = ", val)
            #qpu_iter = rabbitmq_check_qpu_iter()
            #print("qpu_iter", qpu_iter)
            # value += (-1)**(x * y) * chsh_correlator(qnode_settings) #cpu
            #print(qml.PauliZ(0))
            #print(qml.expval(qml.PauliZ(0)))
            #value += (-1)**(x * y) * (qml.expval(qml.PauliZ(0) @ qml.PauliZ(1))) #cpu
            #value = np.array([[-0.3, 1.2, 0.1, 0.9], [-0.2, -3.1, 0.5, -0.7]])
            value += (-1)**(x * y) * val_tmp
    return -(value)

def CHSH_client_part():
    init_settings = random_scenario_settings()

    num_steps = 2
    step_size = 0.3
    #epsilon = 1e-5
    #cpu_iter = 0

    opt = qml.GradientDescentOptimizer(stepsize=step_size)
    #opt = GradientDescentOptimizer(stepsize=step_size)
    #opt = Optimizer()

    values = []
    settings_list = []

    for i in range(num_steps):
        print(i, "print", init_settings)
        value = -(chsh_cost(init_settings))
        print("value = ", value)
        values.append(value)
        settings_list.append(init_settings)
    
        if i % 1 == 0:
            print("iteration : ", i, ", value : ", value, "init_settings : ", init_settings)
    
        init_settings = opt.step(chsh_cost, init_settings)
        
        
        if i % 1 == 0:
            print("iteration : ", i, ", value : ", value, "updated_settings : ", init_settings)


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
    plt.plot(range(num_steps + 1), [2*np.sqrt(2)]*len(range(num_steps + 1)), label="Quantum upperbound")#

    plt.title("Optimization of CHSH Violation\n")
    plt.ylabel("CHSH value")
    plt.xlabel("Iteration")
    plt.legend()

    plt.show()