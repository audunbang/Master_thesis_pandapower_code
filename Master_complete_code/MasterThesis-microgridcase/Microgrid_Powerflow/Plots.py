import matplotlib.pyplot as plt
import csv
import pandas as pd
import load_profiles as lp

#%% Plot power flow
# Read data from CSV file
'''with open('Results/Line_powerflow.csv', 'r') as csvfile:
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
            values_per_node[i].append(-float(value))

# Plot each node
for i, node_values in enumerate(values_per_node):
    plt.step(range(len(node_values)), node_values, label=f'Line {i+1} - 8')

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
    values_per_node = [[] for _ in range(num_nodes)]
    
    # Iterate through the rows and append values to the corresponding lists
    for row in csvreader:
        # Skip empty lines
        if not row:
            continue
        
        for i, value in enumerate(row):
            if i == 8:
                values_per_node[i].append(float(value)*(-1))
            else:
                values_per_node[i].append(float(value))

# Plot each node
for i, node_values in enumerate(values_per_node):
    if i == 8:
        plt.step(range(len(node_values)), node_values, label=f'External grid')
    else:    
        plt.step(range(len(node_values)), node_values, label=f'Bus {i + 1}')

plt.xlabel('Time Step')
plt.ylabel('Value')
plt.title('P [W] for each bus')
plt.legend()
plt.grid(True)
plt.show()

with open('Results/Bus_voltages.csv', 'r') as csvfile:
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
    plt.step(range(len(node_values)), node_values, label=f'Line 1 - {i + 2}')

plt.xlabel('Time Step')
plt.ylabel('Bus voltage')
plt.title('Bus voltages')
plt.legend()
plt.grid(True)
plt.show()'''


hours = []
df = pd.read_csv('Results_totnet/Unmet_load.csv')

load_demand_df = pd.read_csv('data/Weekly load demands 1.csv')
load_demand_df = load_demand_df.drop(columns = 'Time')
row_sums1 = load_demand_df.sum(axis =1)

load_demand_df2 = pd.read_csv('data2/Weekly load demands 2.csv')
load_demand_df2 = load_demand_df2.drop(columns = 'Time')
row_sums2 = load_demand_df2.sum(axis =1)

load_demand_df3 = pd.read_csv('data3/Weekly load demands 3.csv')
load_demand_df3 = load_demand_df3.drop(columns = 'Time')
row_sums3 = load_demand_df3.sum(axis =1)

load_demand_df4 = pd.read_csv('data4/Weekly load demands 4.csv')
load_demand_df4 = load_demand_df4.drop(columns = 'Time')
row_sums4 = load_demand_df4.sum(axis =1)

hours = []

for i in range(24*7):   
    hours.append(i)

values = df.drop(columns=['timestamp'])
load_demands_nano1 = df

row_sums_list = [row_sums1,row_sums2,row_sums3,row_sums4]
count = 0

for col in values.columns:
    
    plt.bar(hours, row_sums_list[count] - values[col]*10**6, label = 'Total demand delivered for nanogrid {}'.format(count+1), alpha = 1)
    plt.step(hours, row_sums_list[count], color = 'black', label = 'Total demand for nanogrid {}'.format(count+1), where = 'mid')
    plt.bar(hours, -values[col]*10**6, color = 'darkred',label='Unmet demand for nanogrid {}'.format(count+1), alpha = 1)
    plt.xlabel('Hour')
    plt.ylabel('Value')
    plt.xticks(range(0, 24*7, 24), ['Day {}'.format(i+1) for i in range(7)])
    plt.title('Unmet demand for nanogrid {}'.format(count+1))
    plt.legend()
    plt.show()
    count += 1

# Add labels and legend

# Show the plot


file_path_loads = "/Users/stian/Documents/Ar_5/MasterThesis-main/data/Weekly load demands 1.csv"
file_path_generation = "/Users/stian/Documents/Ar_5/MasterThesis-main/data/EcoMoyo_scn1_1weeek_may 1.CSV"
load_profiles = pd.read_csv(file_path_loads)
gen_profiles = pd.read_csv(file_path_generation)


sums_list = load_profiles.iloc[:, 1:].sum(axis=1).tolist()

#load_per_hr = file_path_loads.drop(columns=['Time'])

#sums_per_hour = load_per_hr.groupby(hour_column).sum()

'''for i in load_profiles:
    for hour, load in enumerate(i):
        load_per_hr[hour] += load'''


#print(load_per_hr)

df_dis_charge = pd.read_csv('Results_totnet/Charge_discharge_batt.csv')
df_exports = pd.read_csv('Results_totnet/exports.csv')
df_imports = pd.read_csv('Results_totnet/imports.csv')
df_excess = pd.read_csv('Results_totnet/Excess_power.csv')
eco_moyo_load = pd.read_csv('Results_totnet/eco_moyo_load_met.csv')

#fig, ax = plt.subplots(figsize=(10,6))


print(-df_imports['Nanogrid 2'].sum())
print(-df_imports['Nanogrid 3'].sum())
print(-df_imports['Nanogrid 4'].sum())




discharge1 = []
charge1 = []

for i in -df_dis_charge['Battery 1']*10**3:
    if i >= 0:
        discharge1.append(i)
        charge1.append(0)
    else:
        discharge1.append(0)
        charge1.append(i)


discharge1_df = pd.DataFrame(discharge1, columns= ['discharge 1'])
charge1_df = pd.DataFrame(charge1, columns= ['charge 1'])

plt.bar(hours, discharge1_df['discharge 1'], bottom =  eco_moyo_load['Nanogrid 1']*10**3 + df_dis_charge['Battery 1']*10**3 + df_exports['Nanogrid 1']*10**3 + df_imports['Nanogrid 1']*10**3,color = 'forestgreen', label = 'Battery charing and discharging')
plt.bar(hours, charge1_df['charge 1'] ,color = 'forestgreen')
plt.step(hours, [val / 1000 for val in sums_list], color = 'black', label = 'Load demand', where = 'mid')
plt.step(hours, gen_profiles ['EUseful'], color = 'orange', label = 'Solar generation', where = 'mid')
plt.bar((hours), -df_exports['Nanogrid 1']*10**3, bottom = charge1_df['charge 1'] ,color='lightblue', label='Exports', alpha = 0.7)
plt.bar((hours), df_imports['Nanogrid 1']*10**3, color='darkblue', label='Imports', alpha = 0.7)
plt.bar((hours), eco_moyo_load['Nanogrid 1']*10**3 + df_dis_charge['Battery 1']*10**3 + df_exports['Nanogrid 1']*10**3 + df_imports['Nanogrid 1']*10**3,color='orange', label='Utilized solar generation', alpha = 0.7)


# Add labels and legend
plt.xlabel('Time of day')
plt.ylabel('Value [kW]')
plt.title('Eco moyo nanogrid power distribution')
plt.legend()

plt.grid(True, linestyle='--', alpha=0.5)
plt.xticks(range(0, 24*7, 24), ['Day {}'.format(i+1) for i in range(7)])
#plt.xticks([0] + list(hours[::24]), ['0'] + list(hours[::24]), rotation=45)
plt.axhline(0, color='black', linewidth=0.5)
plt.ylim(-10, 10)

# Show the plot
plt.tight_layout()
plt.show()

print('Gen', gen_profiles['EUseful'].sum())

file_path_loads2 = "/Users/stian/Documents/Ar_5/MasterThesis-main/data2/Weekly load demands 2.csv"
file_path_generation2 = "/Users/stian/Documents/Ar_5/MasterThesis-main/data2/HighIncHousehold_scn3_1week_may.CSV"
load_profiles2 = pd.read_csv(file_path_loads2)
gen_profiles2 = pd.read_csv(file_path_generation2)


sums_list2 = load_profiles2.iloc[:, 1:].sum(axis=1).tolist()

#load_per_hr = file_path_loads.drop(columns=['Time'])

#sums_per_hour = load_per_hr.groupby(hour_column).sum()

'''for i in load_profiles:
    for hour, load in enumerate(i):
        load_per_hr[hour] += load'''


#print(load_per_hr)
discharge2 = []
charge2 = []

for i in -df_dis_charge['Battery 2']*10**3:
    if i >= 0:
        discharge2.append(i)
        charge2.append(0)
    else:
        discharge2.append(0)
        charge2.append(i)


discharge2_df = pd.DataFrame(discharge2, columns= ['discharge 2'])
charge2_df = pd.DataFrame(charge2, columns= ['charge 2'])

plt.bar(hours, discharge2_df['discharge 2'], bottom =  [val / 1000 for val in sums_list2] + df_dis_charge['Battery 2']*10**3 + df_exports['Nanogrid 2']*10**3 + df_imports['Nanogrid 2']*10**3,color = 'forestgreen', label = 'Battery charing and discharging')
plt.bar(hours, charge2_df['charge 2'] ,color = 'forestgreen')
plt.step(hours, [val / 1000 for val in sums_list2], color = 'black', label = 'Load demand', where = 'mid')
plt.step(hours, gen_profiles2['EUseful']*0.33, color = 'orange', label = 'Solar generation', where = 'mid')
plt.bar((hours), -df_exports['Nanogrid 2']*10**3, color='lightblue', label='Exports', alpha = 0.7)
plt.bar((hours), df_imports['Nanogrid 2']*10**3, color='darkblue', label='Imports', alpha = 0.7)
plt.bar((hours),  [val / 1000 for val in sums_list2] + df_dis_charge['Battery 2']*10**3 + df_exports['Nanogrid 2']*10**3 + df_imports['Nanogrid 2']*10**3, color='orange', label='Utilized solar generation', alpha = 0.7)


print('Gen', gen_profiles2['EUseful'].sum()*0.33)
print(sum([val / 1000 for val in sums_list2]))

# Add labels and legend
plt.xlabel('Hour')
plt.ylabel('Value [kW]')
plt.title('Nanogrid 2 power distribution')
plt.legend()

plt.grid(True, linestyle='--', alpha=0.5)
plt.xticks(range(0, 24*7, 24), ['Day {}'.format(i+1) for i in range(7)])
plt.axhline(0, color='black', linewidth=0.5)
plt.ylim(-5, 10)

# Show the plot
plt.tight_layout()
plt.show()

file_path_loads3 = "/Users/stian/Documents/Ar_5/MasterThesis-main/data3/Weekly load demands 3.csv"
file_path_generation3 = "/Users/stian/Documents/Ar_5/MasterThesis-main/data3/MedIncHpousehold_scn3_1week_may_2.CSV"
load_profiles3 = pd.read_csv(file_path_loads3)
gen_profiles3 = pd.read_csv(file_path_generation3)


sums_list3 = load_profiles3.iloc[:, 1:].sum(axis=1).tolist()

#load_per_hr = file_path_loads.drop(columns=['Time'])

#sums_per_hour = load_per_hr.groupby(hour_column).sum()

'''for i in load_profiles:
    for hour, load in enumerate(i):
        load_per_hr[hour] += load'''


#print(load_per_hr)


#fig, ax = plt.subplots(figsize=(10,6))

discharge3 = []
charge3 = []

for i in -df_dis_charge['Battery 3']*10**3:
    if i >= 0:
        discharge3.append(i)
        charge3.append(0)
    else:
        discharge3.append(0)
        charge3.append(i)


discharge3_df = pd.DataFrame(discharge3, columns= ['discharge 3'])
charge3_df = pd.DataFrame(charge3, columns= ['charge 3'])

plt.bar(hours, discharge3_df['discharge 3'], bottom =  [val / 1000 for val in sums_list3] + df_dis_charge['Battery 3']*10**3 + df_exports['Nanogrid 3']*10**3 + df_imports['Nanogrid 3']*10**3,color = 'forestgreen', label = 'Battery charing and discharging')
plt.bar(hours, charge3_df['charge 3'] ,color = 'forestgreen')
plt.step(hours, [val / 1000 for val in sums_list3], color = 'black', label = 'Load demand', where = 'mid')
plt.step(hours, gen_profiles3['EUseful']*0.5, color = 'orange', label = 'Solar generation', where = 'mid')
plt.bar((hours), -df_exports['Nanogrid 3']*10**3, color='lightblue', label='Exports', alpha = 0.7)
plt.bar((hours), df_imports['Nanogrid 3']*10**3, color='darkblue', label='Imports', alpha = 0.7)
plt.bar((hours),  [val / 1000 for val in sums_list3] + df_dis_charge['Battery 3']*10**3 + df_exports['Nanogrid 3']*10**3 + df_imports['Nanogrid 3']*10**3, color='orange', label='Utilized solar generation', alpha = 0.7)

# Add labels and legend
plt.xlabel('Hour')
plt.ylabel('Value [kW]')
plt.title('Nanogrid 3 power distribution')
plt.legend()

plt.grid(True, linestyle='--', alpha=0.5)
plt.xticks(range(0, 24*7, 24), ['Day {}'.format(i+1) for i in range(7)])
plt.axhline(0, color='black', linewidth=0.5)
plt.ylim(-5, 10)

# Show the plot
plt.tight_layout()
plt.show()
print(sum([val / 1000 for val in sums_list3]))
print('Gen', gen_profiles3['EUseful'].sum()*0.5)
file_path_loads4 = "/Users/stian/Documents/Ar_5/MasterThesis-main/data4/Weekly load demands 4.csv"
file_path_generation4 = "/Users/stian/Documents/Ar_5/MasterThesis-main/data4/MedIncHpousehold_scn3_1week_may"
load_profiles4 = pd.read_csv(file_path_loads4)
gen_profiles4 = pd.read_csv(file_path_generation4)


sums_list4 = load_profiles4.iloc[:, 1:].sum(axis=1).tolist()

#load_per_hr = file_path_loads.drop(columns=['Time'])

#sums_per_hour = load_per_hr.groupby(hour_column).sum()

'''for i in load_profiles:
    for hour, load in enumerate(i):
        load_per_hr[hour] += load'''


#print(load_per_hr)


#fig, ax = plt.subplots(figsize=(10,6))

discharge4 = []
charge4 = []

for i in -df_dis_charge['Battery 4']*10**3:
    if i >= 0:
        discharge4.append(i)
        charge4.append(0)
    else:
        discharge4.append(0)
        charge4.append(i)

print('Gen', gen_profiles4['EUseful'].sum()*0.5)
discharge4_df = pd.DataFrame(discharge4, columns= ['discharge 4'])
charge4_df = pd.DataFrame(charge4, columns= ['charge 4'])
print(sum([val / 1000 for val in sums_list4]))
plt.bar(hours, discharge4_df['discharge 4'], bottom =  [val / 1000 for val in sums_list4] + df_dis_charge['Battery 4']*10**3 + df_exports['Nanogrid 4']*10**3 + df_imports['Nanogrid 4']*10**3,color = 'forestgreen', label = 'Battery charing and discharging')
plt.bar(hours, charge4_df['charge 4'] ,color = 'forestgreen')
plt.step(hours, [val / 1000 for val in sums_list4], color = 'black', label = 'Load demand', where = 'mid')
plt.step(hours, gen_profiles4['EUseful']*0.5, color = 'orange', label = 'Solar generation', where = 'mid')
plt.bar((hours), -df_exports['Nanogrid 4']*10**3, color='lightblue', label='Exports', alpha = 0.7)
plt.bar((hours), df_imports['Nanogrid 4']*10**3, color='darkblue', label='Imports', alpha = 0.7)
plt.bar((hours),  [val / 1000 for val in sums_list4] + df_dis_charge['Battery 4']*10**3 + df_exports['Nanogrid 4']*10**3 + df_imports['Nanogrid 4']*10**3, color='orange', label='Utilized solar generation', alpha = 0.7)


# Add labels and legend
plt.xlabel('Hour')
plt.ylabel('Value [kW]')
plt.title('Nanogrid 4 power distribution')
plt.legend()

plt.grid(True, linestyle='--', alpha=0.5)
plt.xticks(range(0, 24*7, 24), ['Day {}'.format(i+1) for i in range(7)])
plt.axhline(0, color='black', linewidth=0.5)
plt.ylim(-5, 10)

# Show the plot
plt.tight_layout()
plt.show()


with open('Results_totnet/Bus_voltages.csv', 'r') as csvfile:
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
        
        for i, value in enumerate(row[1:], start = 1):
            values_per_node[i-1].append(float(value))

# Plot each node
for node_name, node_values in enumerate(values_per_node):
    plt.step(range(len(node_values)), node_values, label = nodes[node_name])

plt.xlabel('Time Step')
plt.ylabel('Bus voltage')
plt.title('Bus voltages')
plt.grid(True)
plt.show()



soc_path = "/Users/stian/Documents/Ar_5/MasterThesis-main/Results_totnet/SoC_battery.csv"
soc_profiles = pd.read_csv(soc_path)


#load_per_hr = file_path_loads.drop(columns=['Time'])

#sums_per_hour = load_per_hr.groupby(hour_column).sum()

'''for i in load_profiles:
    for hour, load in enumerate(i):
        load_per_hr[hour] += load'''


#print(load_per_hr)

y_min = 20
y_max = 95

y_transformed = (soc_profiles['Battery 1'] - 0) * (y_max - y_min) / (100 - 0) + y_min
y_transformed2 = (soc_profiles['Battery 2'] - 0) * (y_max - y_min) / (100 - 0) + y_min
y_transformed3 = (soc_profiles['Battery 3'] - 0) * (y_max - y_min) / (100 - 0) + y_min
y_transformed4 = (soc_profiles['Battery 4'] - 0) * (y_max - y_min) / (100 - 0) + y_min
#fig, ax = plt.subplots(figsize=(10,6))

plt.step(hours, y_transformed, color = 'forestgreen', label = 'Eco Moyo nanogrid')
plt.step(hours, y_transformed2, color = 'darkblue', label = 'Nanogrid 2')
plt.step(hours, y_transformed3, color = 'darkred', label = 'Nanogrid 3')
plt.step(hours, y_transformed4, color = 'orange', label = 'Nanogrid 4')

plt.xlabel('Hour')
plt.ylabel('Battery state of charge [%]')
plt.title('Battery state of charge for each nanogrid')
plt.legend()


 
# Apply linear transformation

plt.grid(True, linestyle='--', alpha=0.5)
plt.xticks(range(0, 24*7, 24), ['Day {}'.format(i+1) for i in range(7)])
plt.axhline(0, color='black', linewidth=0.5)

# Show the plot
plt.tight_layout()
plt.show()





plt.bar((hours), (df_exports['Nanogrid 4']*10**3 +  df_imports['Nanogrid 4']*10**3), color='lightblue', label='Power exchange for nanogrid 4', alpha = 0.7)

plt.bar((hours), (df_exports['Nanogrid 3']*10**3 + df_imports['Nanogrid 3']*10**3), bottom = df_exports['Nanogrid 4']*10**3 + df_imports['Nanogrid 4']*10**3, color='darkred', label='Power exchange for nanogrid 3', alpha = 0.7)

plt.bar((hours), (df_exports['Nanogrid 2']*10**3 + df_imports['Nanogrid 2']*10**3), bottom = df_exports['Nanogrid 4']*10**3 + df_exports['Nanogrid 3']*10**3 + df_imports['Nanogrid 4']*10**3 + df_imports['Nanogrid 3']*10**3 ,color='darkgreen', label='Power exchange for nanogrid 2', alpha = 0.7)

plt.bar((hours), (df_exports['Nanogrid 1']*10**3 + df_imports['Nanogrid 1']*10**3), bottom = df_exports['Nanogrid 4']*10**3 + df_exports['Nanogrid 3']*10**3 + df_exports['Nanogrid 2']*10**3, color='darkorange', label='Power exchange for Eco Moyo nanogrid', alpha = 0.7)

plt.xlabel('Hour')
plt.ylabel('Power [kW]')
plt.title('Power exchange each nanogrid')
plt.legend()

plt.grid(True, linestyle='--', alpha=0.5)
plt.xticks(range(0, 24*7, 24), ['Day {}'.format(i+1) for i in range(7)])
plt.axhline(0, color='black', linewidth=0.5)

# Show the plot
plt.tight_layout()
plt.show()