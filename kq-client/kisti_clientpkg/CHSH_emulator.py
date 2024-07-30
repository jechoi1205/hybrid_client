import pennylane as qml

chsh_dev = qml.device("default.qubit", wires=2)


# The quantum function must always return either a single or a tuple of measurement values, 
# by applying a measurement function to the qubit register.
@qml.qnode(chsh_dev)
def chsh_correlator(settings): 
    qml.RY(settings[0], wires=[0])
    qml.RY(settings[1], wires=[1])
    qml.CNOT(wires=[0, 1])
    
    qml.RY(settings[2], wires=[0])
    qml.RY(settings[3], wires=[1])
    
    val = qml.expval(qml.PauliZ(0) @ qml.PauliZ(1))
    print(val)
    return val