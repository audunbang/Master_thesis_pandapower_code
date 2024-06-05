import matplotlib.pyplot as plt
import csv
import pandas as pd
import load_profiles as lp

#%% Plot power flow
# Read data from CSV file
with open('Results/Line_powerflow.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    
    # Read nodes from the first row
    nodes = next(csvreader)
    num_nodes = len(nodes)
    
    # Initialize a list of lists to store values for each node
    values_per_node = [[] for _ in range(num_nodes)]
    
    # Iterate through the rows and append values to the corresponding lists
    for row in csvreader:
        # Skip empty lines
        if not row:
            continue
        
        for i, value in enumerate(row):
            values_per_node[i].append(float(value))

# Plot each node
for i, node_values in enumerate(values_per_node):
    if i != 7:
        plt.step(range(len(node_values)), node_values, label=f'Line {i} - 7')

plt.xlabel('Time Step')
plt.ylabel('Power [W]')
plt.title('Power flow in lines')
plt.legend()
plt.grid(True)
plt.show()


#%% Plot bus power

with open('Results/Bus_power.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    
    # Read nodes from the first row
    nodes = next(csvreader)
    num_nodes = len(nodes)
    
    # Initialize a list of lists to store values for each node
    values_per_node2 = [[] for _ in range(num_nodes)]
    
    # Iterate through the rows and append values to the corresponding lists
    for row in csvreader:
        # Skip empty lines
        if not row:
            continue
        
        for i, value in enumerate(row):
            if i == 7:
                values_per_node2[i].append(float(value)*(-1))
            else:
                values_per_node2[i].append(float(value))

# Plot each node
for i, node_values in enumerate(values_per_node2):
    if i == 8:
        plt.step(range(len(node_values)), node_values, label=f'External grid')
    else:    
        plt.step(range(len(node_values)), node_values, label=f'Bus {i}')

plt.xlabel('Time Step')
plt.ylabel('Value')
plt.title('P [W] for each bus')
plt.legend()
plt.grid(True)
plt.show()


Busnames = ['Church', 'Residential load 1', 'Residential load 2', 'Residential load 3', 'Residential load 4', 'Residential load 5', 'Health centre', 'Eco Moyo']
with open('Results/Bus_voltages.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    
    # Read nodes from the first row
    nodes = next(csvreader)
    num_nodes = len(nodes)
    
    # Initialize a list of lists to store values for each node
    values_per_node3 = [[] for _ in range(num_nodes)]
    
    # Iterate through the rows and append values to the corresponding lists
    for row in csvreader:
        # Skip empty lines
        if not row:
            continue
        
        for i, value in enumerate(row):
            values_per_node3[i].append(float(value))

# Plot each node
for i, node_values in enumerate(values_per_node3):
    plt.step(range(len(node_values)), node_values, label= Busnames[i])

plt.xlabel('Time Step')
plt.ylabel('Voltage [PU]')
plt.title('Bus voltages')
plt.ylim(0.999, 1.001)
plt.legend()
plt.grid(True)
plt.show()


with open('Results/Unmet_load.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    
    # Read nodes from the first row
    nodes = next(csvreader)
    num_nodes = len(nodes)
    
    # Initialize a list of lists to store values for each node
    values_per_node = [[] for _ in range(num_nodes)]
    
    # Iterate through the rows and append values to the corresponding lists
    for row in csvreader:
        # Skip empty lines
        if not row:
            continue
        
        for i, value in enumerate(row):
            values_per_node[i].append(float(value))

# Plot each node
for i, node_values in enumerate(values_per_node):
    if i == 8:
        plt.step(range(len(node_values)), node_values, label=f'Total')
    else:
        plt.step(range(len(node_values)), node_values, label=f'Bus - {i}')

plt.xlabel('Time Step')
plt.ylabel('Unmet load Surplus energy [W]')
plt.title('Unmet load/Surplus energy Eco Moyo Nanogrid')
plt.legend()
plt.grid(True)
plt.show()