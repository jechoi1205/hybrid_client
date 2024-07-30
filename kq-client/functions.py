import numpy as np

def read_fcidump(file_name):
    with open(file_name, 'r') as f:
        lines = f.readlines()

    # Parse the integrals
    integrals = []
    for line in lines:
        if line.startswith(' &FCI') or line.startswith('/'):
            continue
        parts = line.strip().split()
        if len(parts) == 5:
            integral = float(parts[0])
            indices = tuple(int(x) for x in parts[1:])
            integrals.append((integral, indices))

    # Print some of the parsed integrals
    print("\nIntegrals:")
    for integral in integrals[:10]:  # Print the first 10 integrals as an example
        print(integral)
    print("\n")

def generate_random_matrix_file(file_path):
    labels = [(i, j) for i in range(1, 3) for j in range(1, 3)]
    
    with open(file_path, 'w') as f:
        for label in labels:
            random_value = np.random.random()
            f.write(f"{label[0]} {label[1]} {random_value:.6f}\n")

def generate_random_tensor_file(file_path):
    labels = [(i, j, k, l) for i in range(1, 3) for j in range(1, 3) for k in range(1, 3) for l in range(1, 3)]
    
    with open(file_path, 'w') as f:
        for label in labels:
            random_value = np.random.random()
            f.write(f"{label[0]} {label[1]} {label[2]} {label[3]} {random_value:.6f}\n")
