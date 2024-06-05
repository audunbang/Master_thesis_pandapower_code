"""
Created between 2023-08 to 2024-05

@author: Audun Hagland Bangsund

Quasi-static power flow model for nanogrid created for master thesis at NTNU 2024.
"""


#dependencies

import pandapower as pp
import pandapower.plotting as pp_plotting
import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import sys 
import load_profiles as lp
import pandapower_read_csv as ppcsv
import numba
import csv


#creating network with Eco Moyo at the 1 bus
net = pp.create_empty_network(name='Eco_moyo_nanogrid', f_hz=50, sn_mva=0.010, add_stdtypes=True)
 
#Creating the EcoMoyo bus
bus_EcoMoyo = pp.create_bus(net, vn_kv=0.400, index = 0)
 
 
#Creating residental load buses
bus_res1 = pp.create_bus(net, vn_kv=0.400, index = 1)
bus_res2 = pp.create_bus(net, vn_kv=0.400, index = 2)
bus_res3 = pp.create_bus(net, vn_kv=0.400, index = 3)
bus_res4 = pp.create_bus(net, vn_kv=0.400, index = 4)
bus_res5 = pp.create_bus(net, vn_kv=0.400, index = 5)
 
#Creating hospital and church buses
 
bus_hospital = pp.create_bus(net, vn_kv=0.400, index = 6)
bus_farm = pp.create_bus(net, vn_kv=0.400, index = 7)
 
 
#Creating lines
 
pp.create_line(net, from_bus=bus_farm, to_bus=bus_EcoMoyo, length_km=0.07, std_type="94-AL1/15-ST1A 0.4") #Church
pp.create_line(net, from_bus=bus_farm, to_bus=bus_res1, length_km=0.1, std_type="94-AL1/15-ST1A 0.4")
pp.create_line(net, from_bus=bus_farm, to_bus=bus_res2, length_km=0.1, std_type="94-AL1/15-ST1A 0.4")
pp.create_line(net, from_bus=bus_farm, to_bus=bus_res3, length_km=0.19, std_type="94-AL1/15-ST1A 0.4")
pp.create_line(net, from_bus=bus_farm, to_bus=bus_res4, length_km=0.268, std_type="94-AL1/15-ST1A 0.4")
pp.create_line(net, from_bus=bus_farm, to_bus=bus_res5, length_km=0.288, std_type="94-AL1/15-ST1A 0.4")
pp.create_line(net, from_bus=bus_farm, to_bus=bus_hospital, length_km=0.232, std_type="94-AL1/15-ST1A 0.4")

 
 
#Creating loads and generation, with Eco Moyo as slack bus
 
pp.create_gen(net, bus=7, p_mw = 0, slack = True)
 
pp.create_sgen(net, bus = 7, p_mw = 1, q_mvar=0, name="Eco Moyo gen", type = "PV")

pp.create_load(net, bus=bus_EcoMoyo, p_mw=1)
pp.create_load(net, bus=bus_res1, p_mw=1)
pp.create_load(net, bus=bus_res2, p_mw=1)
pp.create_load(net, bus=bus_res3, p_mw=1)
pp.create_load(net, bus=bus_res4, p_mw=1)
pp.create_load(net, bus=bus_res5, p_mw=1)
pp.create_load(net, bus=bus_hospital, p_mw=1)
pp.create_load(net, bus=bus_farm, p_mw=1)

 

#Battery parameters
charging_rate = 8500*10**(-6)
discharging_rate = 6400*10**(-6)
battery_capacity = 14500*0.75*10**(-6)
battery_efficiancy = 0.95
soc = 60
battery_flow = 0
battery_energy = soc*battery_capacity/100
 
pp.create_storage(net, 7, p_mw = -discharging_rate, max_p_mw = -discharging_rate, max_e_mwh = battery_capacity, soc_percent= soc)


#Reading loadfiles 
file_path_loads = r"data_nano\Weekly load demands 1.csv"
file_path_generation = r"data_nano\EcoMoyo_scn1_1weeek_may 1.CSV"


load_profiles = lp.load_profiles(file_path_loads)
gen_profiles = pd.read_csv(file_path_generation)

#Mapping loadprofiles to network
repr_days = list(range(1,8))

mapping_file_path = r"data_nano\Test_loads_mapping.csv"
profiles_mapped = load_profiles.map_rel_load_profiles(mapping_file_path,repr_days)


#Creating results files and dataframes
file_path_voltage_results = r"Results_nano\Bus_voltages.csv"
file_path_powerflow_results = r"Results_nano\Line_powerflow.csv"
file_path_power_results = r'Results_nano\Bus_power.csv'
file_path_unmet_results = r"Results_nano\Unmet_load.csv"
file_path_excess_results = r"Results_nano\Excess_power.csv"


df_vm_res = pd.DataFrame(columns=net.bus.index)
df_buspower_res = pd.DataFrame(columns=net.bus.index)
df_lineflow_res = pd.DataFrame(columns=net.line.index)
df_buspower_unmet = pd.DataFrame(columns=net.bus.index)
df_original_load = pd.DataFrame(columns=net.bus.index)
df_altered_load = pd.DataFrame(columns=net.bus.index)
batt_power_res = []
Original_gen_list = []
Sgen_res_list = []
gen_res_list = []
batt_charg_res = []


timepoint_sums = load_profiles.calculate_sum_per_timepoint()
print(net)
print('------')
print(net.storage)
print('------')
print(net.load['p_mw'])
print('---------')
print(net.ext_grid)

timestamps = []
unmet_demand_list = []
unmet_demand_list2 = []
excess_energy = []
count = 0
battery_soc_list = []
bus_list = []
bus_list2 = []

num_buses = net.bus.shape[0]


for i in range(8):
    bus_list.append(i)


#%%
#Iterating each item in the timeseries
for index, row in profiles_mapped.iterrows():

    timestamps.append(gen_profiles['date'].iloc[count])
    unmet_demand_list.append(0)
    unmet_demand_list2.append(0)
    #battery_soc_list.append(net.storage['soc_percent'].iloc[0])
    net.storage.at[0,'p_mw'] = -discharging_rate
    net.sgen.at[0, 'p_mw'] =  gen_profiles['EUseful'][index]/1000
    Original_gen = gen_profiles['EUseful'][index]/1000
    Original_gen_list.append(Original_gen*10**6)
    for column_name in profiles_mapped.columns:
        value = row[column_name]
        net.load.at[column_name, 'p_mw'] = value/10**6
        
    original_tot_load = net.load['p_mw'].sum()    

    for idx, p in net.load['p_mw'].items(): 
        df_original_load.loc[index, idx] = p*10**6
    
    soc = net.storage.at[0,'soc_percent']
    batt_power = net.storage.at[0,'p_mw']

    if index == 7:
        lol = True


    if net.sgen['p_mw'].sum() >= net.load['p_mw'].sum() + min(battery_capacity*(100-soc)*0.01, charging_rate):
       batt_power = min(battery_capacity*(100-soc)*0.01, charging_rate)
       df_buspower_unmet.loc[index, 7] = (net.sgen.at[0, 'p_mw'] - net.load['p_mw'].sum() - min(battery_capacity*(100-soc)*0.01, charging_rate))*10**6
       net.sgen.at[0, 'p_mw'] = net.load['p_mw'].sum() + min(battery_capacity*(100-soc)*0.01, charging_rate)
       

    else:
        if net.sgen['p_mw'].sum() > net.load.at[7, 'p_mw'] +  min(battery_capacity*(100-soc)*0.01, charging_rate):    
            for bus in bus_list[:-1]:
                if net.sgen['p_mw'].sum() >= net.load['p_mw'].sum() + min(battery_capacity*(100-soc)*0.01, charging_rate):
                    batt_power = min(min(battery_capacity*(100-soc)*0.01, charging_rate), net.sgen['p_mw'].sum() - net.load['p_mw'].sum())
                    break
                else:
                    df_buspower_unmet.loc[index, bus] = -(net.load.at[bus, 'p_mw'])*10**6
                    net.load.at[bus, 'p_mw'] = 0
        else:
            for bus in range(7):
                df_buspower_unmet.loc[index, bus] = -(net.load.at[bus, 'p_mw'])*10**6
                net.load.at[bus, 'p_mw'] = 0
            
            if min(discharging_rate, soc*battery_capacity/100) + net.sgen['p_mw'].sum() > net.load.at[7, 'p_mw']:
                batt_power = -min(min(discharging_rate, soc*battery_capacity/100), net.load.at[7, 'p_mw'] - net.sgen.at[0, 'p_mw'])

            else:
                if min(discharging_rate, soc*battery_capacity/100) + net.sgen['p_mw'].sum() > 1800*10**(-6):
                    df_buspower_unmet.loc[index, 7] = -(net.load.at[7, 'p_mw']*10**(6) - 1800)
                    net.load.at[7, 'p_mw'] = 1800*10**(-6)
                    batt_power = -min(min(discharging_rate, soc*battery_capacity/100), 1800*10**(-6) - net.sgen.at[0, 'p_mw'])

                else:
                    df_buspower_unmet.loc[index, 7] = -(net.load.at[7,'p_mw'])*10**6
                    net.load.at[7,'p_mw'] = 0
                    batt_power = net.sgen.at[0, 'p_mw']


    #Updating battery parameters

    net.storage.at[0,'p_mw'] = batt_power
    net.storage.at[0,'soc_percent'] = soc
    
    
    print('Iteration: ', index)
    pp.runpp(net, numba = False, max_iteration = 50)

    print('Res generation [W]', net.res_gen*10**6)
    print('Net res_storage: [W]', net.res_storage*10**6)

    
    soc_update = (net.res_storage.at[0, 'p_mw']/battery_capacity)*100
    soc += soc_update
    battery_soc_list.append(soc)
    net.storage.at[0,'soc_percent'] = soc
    
    print('Soc: ', net.storage.at[0, 'soc_percent'])

    #Writing to dataframes

    for idx, p in net.load['p_mw'].items(): 
        df_altered_load.loc[index, idx] = p*10**6

    for idx, vm in net.res_bus['vm_pu'].items(): 
        df_vm_res.loc[index, idx] = vm

    for idx, p in net.res_bus['p_mw'].items(): 
        df_buspower_res.loc[index, idx] = p*10**6


    for idx, pf in net.res_line['p_from_mw'].items(): 
        df_lineflow_res.loc[index, idx] = pf*10**6

    if net.res_storage.at[0, 'p_mw'] < 0:
        batt_power_res.append(-net.res_storage.at[0, 'p_mw']*10**6)
        batt_charg_res.append(0)
    else:
        batt_charg_res.append(-net.res_storage.at[0, 'p_mw']*10**6)
        batt_power_res.append(0)
    
    Sgen_res_list.append(net.res_sgen['p_mw'].sum()*10**6)
    gen_res_list.append(net.res_gen['q_mvar'].sum()*10**6)


#Formatting dataframes

df_buspower_unmet.fillna(0, inplace=True)

df_buspower_unmet['tot'] = df_buspower_unmet.sum(axis=1)
df_lineflow_res['tot'] = df_lineflow_res.sum(axis=1)
df_original_load['tot'] = df_original_load.sum(axis=1)
df_altered_load['tot'] = df_altered_load.sum(axis=1)
df_diff = df_altered_load - df_original_load
df_batt_power_res = pd.DataFrame(batt_power_res, columns=['Battery power'])
df_original_solar_gen = pd.DataFrame(Original_gen_list, columns=['Solar gen'])
df_sgen_res = pd.DataFrame(Sgen_res_list, columns=['Utilized solar gen'])
df_batt_soc = pd.DataFrame(battery_soc_list, columns=['SOC'])
df_altered_load_neg = -df_altered_load
df_batt_charging_res = pd.DataFrame(batt_charg_res, columns=['Battery power'])



#Writing to csv

with open(file_path_unmet_results, "w") as file:
    df_buspower_unmet.to_csv(file, index= False)


with open(file_path_voltage_results, "w") as file:
    df_vm_res.to_csv(file, index= False)

with open(file_path_powerflow_results, "w") as file:
    df_lineflow_res.to_csv(file, index= False)

with open(file_path_power_results, "w") as file:
    df_buspower_res.to_csv(file, index= False)


#Plots and results

print('Peak load Eco Moyo: ', df_original_load[7].max())
print('Delivered load Eco Moyo [kWh]: ', df_altered_load[7].sum()/1000)
print('Unmet demand Eco moyo [kWh]: ', df_diff[7].sum()/-1000)
print('Original generation Eco Moyo [kWh]: ', df_original_solar_gen.sum()/1000, )
print('Altered generation Eco Moyo [kWh]: ', df_sgen_res.sum()/1000, )
print('Load exported from Eco Moyo [kWh]: ', df_altered_load.iloc[:, 0:7].sum(axis=1).sum()/1000)
print('Load Eco Moyo unable to meet [kWh]: ', df_original_load.iloc[:, 0:7].sum(axis=1).sum()/1000) #- df_altered_load.iloc[:, 0:7].sum(axis=1).sum()/1000)



plt.plot(range(len(df_diff[7])), df_diff[7] , drawstyle = 'steps-mid', color = 'red', label = 'Unmet load Eco Moyo', linewidth = 2)
plt.bar(range(len(df_batt_power_res['Battery power'])), df_batt_power_res['Battery power'], bottom = df_sgen_res['Utilized solar gen'],  width = 0.85, color = 'green', label = 'Battery power')
plt.bar(range(len(df_batt_power_res['Battery power'])), df_batt_charging_res['Battery power'], width = 0.85, color = 'green')
plt.bar(range(len(df_sgen_res['Utilized solar gen'])), df_sgen_res['Utilized solar gen'], width = 0.85, color = 'orange', label = 'Utilized solar generation')
plt.plot(df_original_solar_gen['Solar gen'], drawstyle = 'steps-mid', label = 'Total solar generation', color = 'orange', linewidth = 2)
plt.bar(range(len(df_altered_load.iloc[:, 0:7].sum(axis=1))),df_altered_load_neg.iloc[:, 0:7].sum(axis=1), bottom = df_batt_charging_res['Battery power'],width = 0.85, color = 'lightblue', label = 'Power exported')
plt.plot(df_original_load[7], drawstyle = 'steps-mid', label = 'Total load Eco Moyo', color = 'black', linewidth = 2)

plt.xticks(range(0, 24*7, 24), ['Day {}'.format(i+1) for i in range(7)])

plt.tick_params(axis='both', which='major', labelsize=12)
plt.tick_params(axis='both', which='minor', labelsize=10)

plt.xlabel('Timestep', fontsize = 30)
plt.ylabel('Power [W]', fontsize = 30)
plt.title('Eco Moyo power distribution' , fontsize = 30)


plt.legend()
plt.show()



plt.subplot(2,1,1)
y_min = 20
y_max = 95

# Apply linear transformation
y_transformed = (df_batt_soc['SOC'] - 0) * (y_max - y_min) / (100 - 0) + y_min
plt.step(range(len(df_batt_soc['SOC'])), y_transformed, color = 'darkgreen')

# Adding labels
plt.xlabel('Day')
plt.ylabel('SOC [%]')
plt.title('Battery parameters for Eco Moyo')
plt.xticks(range(0, 24*7, 24), ['Day {}'.format(i+1) for i in range(7)])


plt.subplot(2,1,2)

plt.bar(range(len(df_batt_power_res['Battery power'])), df_batt_power_res['Battery power'], color = 'darkgreen', width = 0.85)
plt.bar(range(len(df_batt_power_res['Battery power'])), df_batt_charging_res['Battery power'], color = 'darkgreen', width = 0.85)
plt.axhline(0, color = 'black', linewidth = 2)
plt.ylabel('Battery power [W]')
plt.xticks(range(0, 24*7, 24), ['Day {}'.format(i+1) for i in range(7)])


# Display the plot
plt.show()
