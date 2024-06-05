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

"""
Created between 2023-08 to 2024-05
 
@author: Stian Rummelhoff
 
Quasi-static power flow model for microgrid created for master thesis at NTNU 2024.
"""

net = pp.create_empty_network(name='Eco_moyo_nanogrid', f_hz=50, sn_mva=0.1, add_stdtypes=True)
 
#Creating the EcoMoyo bus
bus_EcoMoyo = pp.create_bus(net, vn_kv=0.400, index = 8)
 
#Creating residental load buses
bus_res1 = pp.create_bus(net, vn_kv=0.400, index = 2)
bus_res2 = pp.create_bus(net, vn_kv=0.400, index = 3)
bus_res3 = pp.create_bus(net, vn_kv=0.400, index = 4)
bus_res4 = pp.create_bus(net, vn_kv=0.400, index = 5)
bus_res5 = pp.create_bus(net, vn_kv=0.400, index = 6)
 
#Creating hospital, farm and church buses
 
bus_hospital = pp.create_bus(net, vn_kv=0.400, index = 7)
bus_church = pp.create_bus(net, vn_kv=0.400, index = 1)
 
#Creating lines
 
pp.create_line(net, from_bus=bus_EcoMoyo, to_bus=bus_res1, length_km=0.25, std_type="679-AL1/86-ST1A 380.0")
pp.create_line(net, from_bus=bus_EcoMoyo, to_bus=bus_res2, length_km=0.1, std_type="679-AL1/86-ST1A 380.0")
pp.create_line(net, from_bus=bus_EcoMoyo, to_bus=bus_res3, length_km=0.19, std_type="679-AL1/86-ST1A 380.0")
pp.create_line(net, from_bus=bus_EcoMoyo, to_bus=bus_res4, length_km=0.268, std_type="679-AL1/86-ST1A 380.0")
pp.create_line(net, from_bus=bus_EcoMoyo, to_bus=bus_res5, length_km=0.232, std_type="679-AL1/86-ST1A 380.0")
pp.create_line(net, from_bus=bus_EcoMoyo, to_bus=bus_hospital, length_km=0.1, std_type="679-AL1/86-ST1A 380.0")
pp.create_line(net, from_bus=bus_EcoMoyo, to_bus=bus_church, length_km=0.07, std_type="679-AL1/86-ST1A 380.0")
 
#Creating loads and generation, with Eco Moyo as slack bus
 
pp.create_gen(net, bus=bus_EcoMoyo, p_mw = 0, slack = True)
 
pp.create_sgen(net, 8, p_mw = 0, q_mvar=0, name="Eco Moyo gen", type = "PV")
 
pp.create_load(net, bus=bus_EcoMoyo, p_mw=1)
pp.create_load(net, bus=bus_res1, p_mw=1)
pp.create_load(net, bus=bus_res2, p_mw=1)
pp.create_load(net, bus=bus_res3, p_mw=1)
pp.create_load(net, bus=bus_res4, p_mw=1)
pp.create_load(net, bus=bus_res5, p_mw=1)
pp.create_load(net, bus=bus_hospital, p_mw=1)
pp.create_load(net, bus=bus_church, p_mw=1)


charging_rate = 5900/10**6
discharging_rate = 6400/10**6
battery_capacity = 14500*0.75/10**6
battery_efficiancy = 0.95
soc = 60
battery_flow = 0
battery_energy = soc*battery_capacity/100


pp.create_storage(net, 8, p_mw = - discharging_rate, max_p_mw = -6400/10**6, max_e_mwh = battery_capacity, soc_percent= soc)

file_path_loads = "data/Weekly load demands 1.csv"
file_path_generation = "data/EcoMoyo_scn1_1weeek_may 1.CSV"


load_profiles = lp.load_profiles(file_path_loads)
gen_profiles = pd.read_csv(file_path_generation)

#Mapping loadprofiles to network
repr_days = list(range(1,8))

mapping_file_path = "data/Test_loads_mapping.csv"
profiles_mapped = load_profiles.map_rel_load_profiles(mapping_file_path,repr_days)

load_time_series_mapped = profiles_mapped.mul(net.load['p_mw'])

#print(pp.diagnostic(net, report_style= 'detailled', warnings_only=True))
#Creating results files and dataframes
file_path_voltage_results = "Results/Bus_voltages.csv"
file_path_unmet_results = "Results/Unmet_load.csv"
file_path_excess_results = "Results/Excess_power.csv"
file_path_powerflow_results = "Results/Line_powerflow.csv"
file_path_power_results = 'Results/Bus_power.csv'

df_vm_res = pd.DataFrame(columns=net.bus.index)
df_buspower_res = pd.DataFrame(columns=net.bus.index)
df_lineflow_res = pd.DataFrame(columns=net.line.index)

net2 = pp.create_empty_network(name='Eco_moyo_nanogrid2', f_hz=50, sn_mva=0.1, add_stdtypes=True)
 
#Creating the EcoMoyo bus
bus_EcoMoyo2 = pp.create_bus(net2, vn_kv=0.400, index = 6)
 
#Creating residental load buses
bus_res12 = pp.create_bus(net2, vn_kv=0.400, index = 2)
bus_res22 = pp.create_bus(net2, vn_kv=0.400, index = 3)
bus_res32 = pp.create_bus(net2, vn_kv=0.400, index = 4)
bus_res42 = pp.create_bus(net2, vn_kv=0.400, index = 5)
bus_res52 = pp.create_bus(net2, vn_kv=0.400, index = 1)

 
#Creating lines
 
pp.create_line(net2, from_bus=bus_EcoMoyo2, to_bus=bus_res12, length_km=0.15, std_type="679-AL1/86-ST1A 380.0")
pp.create_line(net2, from_bus=bus_EcoMoyo2, to_bus=bus_res22, length_km=0.15, std_type="679-AL1/86-ST1A 380.0")
pp.create_line(net2, from_bus=bus_EcoMoyo2, to_bus=bus_res32, length_km=0.15, std_type="679-AL1/86-ST1A 380.0")
pp.create_line(net2, from_bus=bus_EcoMoyo2, to_bus=bus_res42, length_km=0.15, std_type="679-AL1/86-ST1A 380.0")
pp.create_line(net2, from_bus=bus_EcoMoyo2, to_bus=bus_res52, length_km=0.15, std_type="679-AL1/86-ST1A 380.0")

#Creating loads and generation, with Eco Moyo as slack bus
 
pp.create_gen(net2, bus=bus_EcoMoyo2, p_mw = 0, slack = True)
 
pp.create_sgen(net2, 6, p_mw = 0, q_mvar=0, name="Eco Moyo gen2", type = "PV")
 
pp.create_load(net2, bus=bus_EcoMoyo2, p_mw=1)
pp.create_load(net2, bus=bus_res12, p_mw=1)
pp.create_load(net2, bus=bus_res22, p_mw=1)
pp.create_load(net2, bus=bus_res32, p_mw=1)
pp.create_load(net2, bus=bus_res42, p_mw=1)
pp.create_load(net2, bus=bus_res52, p_mw=1)


surplus = 0
pp.create_storage(net2, 6, p_mw = -discharging_rate, max_p_mw = -6400/10**6, max_e_mwh = battery_capacity, soc_percent= soc)

file_path_loads2 = "data2/Weekly load demands 2.csv"
file_path_generation2 = "data2/HighIncHousehold_scn3_1week_may.CSV"


load_profiles2 = lp.load_profiles(file_path_loads2)
gen_profiles2 = pd.read_csv(file_path_generation2)

mapping_file_path2 = "data2/Test_loads_mapping.csv"
profiles_mapped2 = load_profiles2.map_rel_load_profiles(mapping_file_path2,repr_days)

load_time_series_mapped2 = profiles_mapped2.mul(net2.load['p_mw'])

#print(pp.diagnostic(net, report_style= 'detailled', warnings_only=True))
#Creating results files and dataframes
file_path_voltage_results2 = "Results2/Bus_voltages.csv"
file_path_unmet_results2 = "Results2/Unmet_load.csv"
file_path_excess_results2 = "Results2/Excess_power.csv"
file_path_powerflow_results2 = "Results2/Line_powerflow.csv"
file_path_power_results2 = 'Results2/Bus_power.csv'

df_vm_res2 = pd.DataFrame(columns=net2.bus.index)
df_buspower_res2 = pd.DataFrame(columns=net2.bus.index)
df_lineflow_res2 = pd.DataFrame(columns=net2.line.index)

net3 = pp.create_empty_network(name='Eco_moyo_nanogrid3', f_hz=50, sn_mva=0.1, add_stdtypes=True)
 
#Creating the EcoMoyo bus
bus_EcoMoyo3 = pp.create_bus(net3, vn_kv=0.400, index = 8)
 
#Creating residental load buses
bus_res13 = pp.create_bus(net3, vn_kv=0.400, index = 2)
bus_res23 = pp.create_bus(net3, vn_kv=0.400, index = 3)
bus_res33 = pp.create_bus(net3, vn_kv=0.400, index = 4)
bus_res43 = pp.create_bus(net3, vn_kv=0.400, index = 5)
bus_res53 = pp.create_bus(net3, vn_kv=0.400, index = 6)
 
#Creating hospital, farm and church buses
 
bus_hospital3 = pp.create_bus(net3, vn_kv=0.400, index = 7)
bus_farm3 = pp.create_bus(net3, vn_kv=0.400, index = 1)
 
#Creating lines
 
pp.create_line(net3, from_bus=bus_EcoMoyo3, to_bus=bus_res13, length_km=0.15, std_type="679-AL1/86-ST1A 380.0")
pp.create_line(net3, from_bus=bus_EcoMoyo3, to_bus=bus_res23, length_km=0.15, std_type="679-AL1/86-ST1A 380.0")
pp.create_line(net3, from_bus=bus_EcoMoyo3, to_bus=bus_res33, length_km=0.15, std_type="679-AL1/86-ST1A 380.0")
pp.create_line(net3, from_bus=bus_EcoMoyo3, to_bus=bus_res43, length_km=0.15, std_type="679-AL1/86-ST1A 380.0")
pp.create_line(net3, from_bus=bus_EcoMoyo3, to_bus=bus_res53, length_km=0.15, std_type="679-AL1/86-ST1A 380.0")
pp.create_line(net3, from_bus=bus_EcoMoyo3, to_bus=bus_hospital3, length_km=0.15, std_type="679-AL1/86-ST1A 380.0")
pp.create_line(net3, from_bus=bus_EcoMoyo3, to_bus=bus_farm3, length_km=0.15, std_type="679-AL1/86-ST1A 380.0")
 
#Creating loads and generation, with Eco Moyo as slack bus
 
pp.create_gen(net3, bus=bus_EcoMoyo3, p_mw = 0, slack = True)
 
pp.create_sgen(net3, 1, p_mw = 0, q_mvar=0, name="Eco Moyo gen3", type = "PV")
 
pp.create_load(net3, bus=bus_EcoMoyo3, p_mw=1)
pp.create_load(net3, bus=bus_res13, p_mw=1)
pp.create_load(net3, bus=bus_res23, p_mw=1)
pp.create_load(net3, bus=bus_res33, p_mw=1)
pp.create_load(net3, bus=bus_res43, p_mw=1)
pp.create_load(net3, bus=bus_res53, p_mw=1)
pp.create_load(net3, bus=bus_hospital3, p_mw=1)
pp.create_load(net3, bus=bus_farm3, p_mw=1)



pp.create_storage(net3, 8, p_mw = -discharging_rate, max_p_mw = -6400/10**6, max_e_mwh = battery_capacity, soc_percent= soc)

file_path_loads3 = "data3/Weekly load demands 3.csv"
file_path_generation3 = "data3/MedIncHpousehold_scn3_1week_may_2.CSV"


load_profiles3 = lp.load_profiles(file_path_loads3)
gen_profiles3 = pd.read_csv(file_path_generation3)

load_list2 = []
mapping_file_path3 = "data3/Test_loads_mapping.csv"

profiles_mapped3 = load_profiles3.map_rel_load_profiles(mapping_file_path3,repr_days)

load_time_series_mapped3 = profiles_mapped3.mul(net3.load['p_mw'])

#print(pp.diagnostic(net, report_style= 'detailled', warnings_only=True))
#Creating results files and dataframes
file_path_voltage_results3 = "Results3/Bus_voltages.csv"
file_path_unmet_results3 = "Results3/Unmet_load.csv"
file_path_excess_results3 = "Results3/Excess_power.csv"
file_path_powerflow_results3 = "Results3/Line_powerflow.csv"
file_path_power_results3 = 'Results3/Bus_power.csv'

df_vm_res3 = pd.DataFrame(columns=net3.bus.index)
df_buspower_res3 = pd.DataFrame(columns=net3.bus.index)
df_lineflow_res3 = pd.DataFrame(columns=net3.line.index)

net4 = pp.create_empty_network(name='Eco_moyo_nanogrid4', f_hz=50, sn_mva=0.1, add_stdtypes=True)
 
#Creating the EcoMoyo bus
bus_EcoMoyo4 = pp.create_bus(net4, vn_kv=0.400, index = 8)
 
#Creating residental load buses
bus_res14 = pp.create_bus(net4, vn_kv=0.400, index = 2)
bus_res24 = pp.create_bus(net4, vn_kv=0.400, index = 3)
bus_res34 = pp.create_bus(net4, vn_kv=0.400, index = 4)
bus_res44 = pp.create_bus(net4, vn_kv=0.400, index = 5)
bus_res54 = pp.create_bus(net4, vn_kv=0.400, index = 6)
 
#Creating hospital, farm and church buses
 
bus_hospital4 = pp.create_bus(net4, vn_kv=0.400, index = 7)
bus_farm4 = pp.create_bus(net4, vn_kv=0.400, index = 1)
 
#Creating lines
 
pp.create_line(net4, from_bus=bus_EcoMoyo4, to_bus=bus_res14, length_km=0.15, std_type="679-AL1/86-ST1A 380.0")
pp.create_line(net4, from_bus=bus_EcoMoyo4, to_bus=bus_res24, length_km=0.15, std_type="679-AL1/86-ST1A 380.0")
pp.create_line(net4, from_bus=bus_EcoMoyo4, to_bus=bus_res34, length_km=0.15, std_type="679-AL1/86-ST1A 380.0")
pp.create_line(net4, from_bus=bus_EcoMoyo4, to_bus=bus_res44, length_km=0.15, std_type="679-AL1/86-ST1A 380.0")
pp.create_line(net4, from_bus=bus_EcoMoyo4, to_bus=bus_res54, length_km=0.15, std_type="679-AL1/86-ST1A 380.0")
pp.create_line(net4, from_bus=bus_EcoMoyo4, to_bus=bus_hospital4, length_km=0.15, std_type="679-AL1/86-ST1A 380.0")
pp.create_line(net4, from_bus=bus_EcoMoyo4, to_bus=bus_farm4, length_km=0.15, std_type="679-AL1/86-ST1A 380.0")
 
#Creating loads and generation, with Eco Moyo as slack bus
 
pp.create_gen(net4, bus=bus_EcoMoyo4, p_mw = 0, slack = True)
 
pp.create_sgen(net4, 8, p_mw = 0, q_mvar=0, name="Eco Moyo gen4", type = "PV")
 
pp.create_load(net4, bus=bus_EcoMoyo4, p_mw=1)
pp.create_load(net4, bus=bus_res14, p_mw=1)
pp.create_load(net4, bus=bus_res24, p_mw=1)
pp.create_load(net4, bus=bus_res34, p_mw=1)
pp.create_load(net4, bus=bus_res44, p_mw=1)
pp.create_load(net4, bus=bus_res54, p_mw=1)
pp.create_load(net4, bus=bus_hospital4, p_mw=1)
pp.create_load(net4, bus=bus_farm4, p_mw=1)


pp.create_storage(net4, 8, p_mw = -discharging_rate, max_p_mw = -6400/10**6, max_e_mwh = battery_capacity, soc_percent= soc)

file_path_loads4 = "data4/Weekly load demands 4.csv"
file_path_generation4 = "data4/MedIncHpousehold_scn3_1week_may"


load_profiles4 = lp.load_profiles(file_path_loads4)
gen_profiles4 = pd.read_csv(file_path_generation4)


mapping_file_path4 = "data4/Test_loads_mapping.csv"
profiles_mapped4 = load_profiles4.map_rel_load_profiles(mapping_file_path4,repr_days)

load_time_series_mapped4 = profiles_mapped4.mul(net4.load['p_mw'])


df_vm_res4 = pd.DataFrame(columns=net4.bus.index)
df_buspower_res4 = pd.DataFrame(columns=net4.bus.index)
df_lineflow_res4 = pd.DataFrame(columns=net4.line.index)


net12 = pp.merge_nets(net,net2)

net34 = pp.merge_nets(net3,net4)
tot_net = pp.merge_nets(net12,net34)

tot_unmet_demand = 0
#print(tot_net)

netList = [net, net2, net3, net4]
gen_profiles_list = [gen_profiles, gen_profiles2, gen_profiles3, gen_profiles4]
profiles_mapped_list = [profiles_mapped, profiles_mapped2, profiles_mapped3, profiles_mapped4]

merge_profiles_mapped_final = pd.concat(profiles_mapped_list, axis = 1)


#load_time_series_mapped_merged = merge_profiles_mapped_final.mul(tot_net.load['p_mw'])

pp.create_bus(tot_net, vn_kv= 0.400, type = 'n', index = 31)

pp.create_gen(tot_net, 31, p_mw = 0, q_mw = 0, slack = True)

for i in range (len(netList)):
    tot_net.gen.at[i, 'in_service'] = False

pp.create_line(tot_net,8,31,length_km= 0.75, std_type= '679-AL1/86-ST1A 380.0')
pp.create_line(tot_net,14,31,length_km= 1.2,std_type= '679-AL1/86-ST1A 380.0' )
pp.create_line(tot_net,18,31,length_km= 0.85, std_type= '679-AL1/86-ST1A 380.0')
pp.create_line(tot_net,26,31,length_km= 1.6, std_type= '679-AL1/86-ST1A 380.0')


df_vm_res = pd.DataFrame(columns=tot_net.bus.index)
df_buspower_res = pd.DataFrame(columns=tot_net.bus.index)
df_lineflow_res = pd.DataFrame(columns=tot_net.line.index)

load_list = []

#print(tot_net['line'])
count = 0
print(tot_net)
print(tot_net.sgen['p_mw'])

csv_file_results_unmet = 'Results_totnet/Unmet_load.csv'
file_path_voltage_results_tot = "Results_totnet/Bus_voltages.csv"
file_path_excess_results_tot = "Results_totnet/Excess_power.csv"
file_path_powerflow_results_tot = "Results_totnet/Line_powerflow.csv"
file_path_power_results_tot = 'Results_totnet/Bus_power.csv'

net_power_lists = []
import_lists = []
export_lists = []
SoC_lists = []

nanogrid_bus_list= [[0,1,2,3,4,5,6,7],[8,9,10,11,12,13],[14,15,16,17,18,19,20,21],[22,23,24,25,26,27,28,29]]

timestamps = []
excess_energy = []
value_list = []



for i in range(len(netList)):
    value_list.append(i+1)
        
            # Write the new line

with open(csv_file_results_unmet, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    header_row = ['timestamp']
    
    for i in value_list:
        header_row.append('Nanogrid '+ str(i))

    csv_writer.writerow(header_row)

    for index, row in merge_profiles_mapped_final.iterrows(): 
        import_list = []
        export_list = []
        timestamp = gen_profiles['date'].iloc[count]
        timestamps.append(timestamp)
        count2 = 1
        unmet_demand_list = []
        unmet_demand_eco_moyo = 0  


        for i in range(len(netList)):
            unmet_demand_list.append(0)



        net4.sgen.at[0, 'p_mw'] =  gen_profiles4['EUseful'][index]/2000
        net3.sgen.at[0, 'p_mw'] =  gen_profiles3['EUseful'][index]/2000
        net2.sgen.at[0, 'p_mw'] =  gen_profiles2['EUseful'][index]/3000
        net.sgen.at[0, 'p_mw'] =  gen_profiles['EUseful'][index]/1000
        tot_net.sgen.at[0,'p_mw'] = gen_profiles['EUseful'][index]/1000
        tot_net.sgen.at[1,'p_mw'] = gen_profiles2['EUseful'][index]/3000
        tot_net.sgen.at[2,'p_mw'] = gen_profiles3['EUseful'][index]/2000
        tot_net.sgen.at[3,'p_mw'] = gen_profiles4['EUseful'][index]/2000


        for i in netList:

            if i.storage['p_mw'].iloc[0] <= -i.storage['soc_percent'].iloc[0]*i.storage['max_e_mwh'].iloc[0]/100:
                i.storage.at[0,'p_mw'] = -i.storage['soc_percent'].iloc[0]*i.storage['max_e_mwh'].iloc[0]/100

        if tot_net.storage.at[0,'p_mw'] <= -tot_net.storage.at[0,'soc_percent']*tot_net.storage.at[0,'max_e_mwh']/100:
            tot_net.storage.at[0,'p_mw'] = -tot_net.storage.at[0,'soc_percent']*tot_net.storage.at[0,'max_e_mwh']/100

        
        if tot_net.storage.at[1,'p_mw'] <= -tot_net.storage.at[1,'soc_percent']*tot_net.storage.at[1,'max_e_mwh']/100:
            tot_net.storage.at[1,'p_mw'] = -tot_net.storage.at[1,'soc_percent']*tot_net.storage.at[1,'max_e_mwh']/100

        
        if tot_net.storage.at[2,'p_mw'] <= -tot_net.storage.at[2,'soc_percent']*tot_net.storage.at[2,'max_e_mwh']/100:
            tot_net.storage.at[2,'p_mw'] = -tot_net.storage.at[2,'soc_percent']*tot_net.storage.at[2,'max_e_mwh']/100

        
        if tot_net.storage.at[3,'p_mw'] <= -tot_net.storage.at[3,'soc_percent']*tot_net.storage.at[3,'max_e_mwh']/100:
            tot_net.storage.at[3,'p_mw'] = -tot_net.storage.at[3,'soc_percent']*tot_net.storage.at[3,'max_e_mwh']/100

        for column_name in profiles_mapped.columns:
            value = row[column_name]
            net.load.at[column_name-1, 'p_mw'] = value/10**6

        for column_name in profiles_mapped2.columns:
            value = row[column_name]
            net2.load.at[column_name-9, 'p_mw'] = value/10**6

        for column_name in profiles_mapped3.columns:
            value = row[column_name]
            net3.load.at[column_name-15, 'p_mw'] = value/10**6
        
        for column_name in profiles_mapped4.columns:
            value = row[column_name]
            net4.load.at[column_name-23, 'p_mw'] = value/10**6

        for column_name in merge_profiles_mapped_final.columns:
            value = row[column_name]
            tot_net.load.at[column_name-1, 'p_mw'] = value/10**6

        print('production: ', tot_net.sgen['p_mw'])
        print('Loads per nano: ', netList[0].load['p_mw'].sum(), netList[1].load['p_mw'].sum(), netList[2].load['p_mw'].sum(), netList[3].load['p_mw'].sum())

        '''print('Loads before correction: ')
        print(tot_net.load['p_mw'])'''

        net_power_flow_sum = 0
        net_power_list = []
        for i in range(len(netList)):
            net_power_flow = tot_net.sgen.at[i,'p_mw'] - netList[i].load['p_mw'].sum()
            net_power_list.append(net_power_flow)
            net_power_flow_sum += net_power_flow

        count8 = 0
        while net_power_flow_sum < 0:
            print('A')
            print(net_power_flow_sum)
            if net_power_flow_sum >= -1/10**8:
                break
            for i in net_power_list:
                if i >= 0:
                    continue
                elif i < 0:
                    if tot_net.sgen.at[count8,'name'] == 'Eco Moyo gen':
                        while i < -0.000000001:
                            for j in nanogrid_bus_list[count8]:
                                if i > -0.000000001:
                                    break
                                if j < 7:
                                    unmet_demand_list[count8] += tot_net.load.at[j,'p_mw']
                                    i += tot_net.load.at[j,'p_mw']
                                    net_power_flow_sum += tot_net.load.at[j,'p_mw']
                                    tot_net.load.at[j,'p_mw'] = 0

                                if j == 7:
                                    if tot_net.storage.at[count8,'soc_percent']*tot_net.storage.at[count8,'max_e_mwh']/100 > tot_net.load.at[j,'p_mw']:
                                        i += tot_net.load.at[j,'p_mw']
                                        net_power_flow_sum += tot_net.load.at[j,'p_mw']

                                    else:
                                        i += tot_net.load.at[j,'p_mw']
                                        net_power_flow_sum += tot_net.load.at[j,'p_mw']
                                        tot_net.load.at[j,'p_mw'] = 0

                    else:
                        if tot_net.storage.at[count8,'soc_percent']*tot_net.storage.at[count8,'max_e_mwh']/100 > -i:
                            net_power_flow_sum += -i
                            print('Battery in nanogrid ', count8, ' relsease ', i, ' W from battery')

                            continue

                        elif tot_net.storage.at[count8,'soc_percent']*tot_net.storage.at[count8,'max_e_mwh']/100 <= np.abs(i):
                            while -i >= tot_net.storage.at[count8,'soc_percent']*tot_net.storage.at[count8,'max_e_mwh']/100:
                                for j in nanogrid_bus_list[count8]:
                                    print('i:', i)
                                    print(j)
                                    print(tot_net.storage.at[count8,'soc_percent']*tot_net.storage.at[count8,'max_e_mwh']/100)
                                    unmet_demand_list[count8] += tot_net.load.at[j,'p_mw']
                                    i += tot_net.load.at[j,'p_mw']
                                    net_power_flow_sum += tot_net.load.at[j,'p_mw']
                                    tot_net.load.at[j,'p_mw'] = 0
                                    print(tot_net.load.at[j,'p_mw'])
                                    if -i <= tot_net.storage.at[count8,'soc_percent']*tot_net.storage.at[count8,'max_e_mwh']/100:
                                        break
                count8 +=1

        '''print('Loads after correction: ')
        print(tot_net.load['p_mw'])'''


        #pp.diagnostic(tot_net)
        #print(tot_net.gen)
        print('Unmet demand list rest: ', unmet_demand_list)
        '''print('Loads after correction: ')
        print(netList[0].load['p_mw'].sum())'''

        p_sum_left = 0
        for i in range(len(netList)):
            p_sum_left += (100 - tot_net.storage.at[i,'soc_percent'])/100*tot_net.storage.at[i,'max_e_mwh']

        intermediate_soc = []
        for i in range(len(netList)):
            intermediate_soc.append(tot_net.storage.at[i,'soc_percent'])

        load_list.append(0)
        load_list2.append(0)
        for i in range (tot_net.bus.shape[0]):
            if i <= 6:
                load_list2[count] += tot_net.load.at[i,'p_mw']    
            if i <= 7:
                load_list[count] += tot_net.load.at[i,'p_mw']
                netList[0].load.at[i,'p_mw'] = tot_net.load.at[i,'p_mw']
            elif i > 7 and i <= 13:
                netList[1].load.at[i-8,'p_mw'] = tot_net.load.at[i,'p_mw']
            elif i > 13 and i <= 21:
                netList[2].load.at[i-14,'p_mw'] = tot_net.load.at[i,'p_mw']
            elif i > 21 and i <= 29:
                netList[3].load.at[i-22,'p_mw'] = tot_net.load.at[i,'p_mw']

        to_other_batteries = 0

        for i in range(len(netList)):
            netList[i].storage.at[0,'p_mw'] = - (netList[i].load['p_mw'].sum() - tot_net.sgen.at[i,'p_mw'])
            tot_net.storage.at[i,'p_mw'] = - (netList[i].load['p_mw'].sum() - tot_net.sgen.at[i,'p_mw'])
            '''if tot_net.storage.at[i,'p_mw'] >= 6400/10**6:
                tot_net.storage.at[i,'p_mw'] = 6400/10**6'''

            if tot_net.storage.at[i,'soc_percent'] == 100:
                if tot_net.storage.at[i,'p_mw'] <= 0:
                    tot_net.storage.at[i,'p_mw'] = tot_net.storage.at[i,'p_mw']

                elif tot_net.storage.at[i,'p_mw'] > 0:
                    to_other_batteries += tot_net.storage.at[i,'p_mw']
                    tot_net.storage.at[i,'p_mw'] = 0
            
            elif tot_net.storage.at[i,'soc_percent'] + (tot_net.sgen.at[i,'p_mw'] - netList[i].load['p_mw'].sum())/tot_net.storage.at[i,'max_e_mwh']*100 > 100:
                to_other_batteries += (tot_net.sgen.at[i,'p_mw'] - netList[i].load['p_mw'].sum()) - (100 - tot_net.storage.at[i,'soc_percent'])*tot_net.storage.at[i,'max_e_mwh']/100
                tot_net.storage.at[i, 'p_mw'] = (100 - tot_net.storage.at[i,'soc_percent'])*tot_net.storage.at[i,'max_e_mwh']/100
                tot_net.storage.at[i,'soc_percent'] = 100




        if to_other_batteries >= p_sum_left:
            to_other_batteries = p_sum_left

        
        while to_other_batteries > 0:
            count7 = 0
            count6 = 0
            p = 100
            print(to_other_batteries)
            print(tot_net.storage['soc_percent'].sum())
            for i in range(len(netList)):
                if tot_net.storage.at[i,'p_mw'] < 0:
                    if tot_net.storage.at[i,'p_mw'] + to_other_batteries < 0:
                        tot_net.storage.at[i,'p_mw'] += to_other_batteries
                        to_other_batteries = 0
                        break

                    elif tot_net.storage.at[i,'p_mw'] + to_other_batteries > 0:
                        to_other_batteries += tot_net.storage.at[i,'p_mw']
                        tot_net.storage.at[i,'p_mw'] += (0 - tot_net.storage.at[i,'p_mw'])

                if tot_net.storage.at[count6,'p_mw'] != 5900/10**6:
                    if  tot_net.storage.at[count6, 'soc_percent'] < p:
                        count7 = count6
                        p = tot_net.storage.at[count6, 'soc_percent']

                count6 += 1

            if tot_net.storage.at[count7,'soc_percent'] + ((tot_net.storage.at[count7,'p_mw']+to_other_batteries)/tot_net.storage.at[count7,'max_e_mwh'])*100 >= 100:
                print(tot_net.storage.at[count7,'soc_percent'])
                power_given_to_nano = ((100 - tot_net.storage.at[count7,'soc_percent'])*tot_net.storage.at[count7,'max_e_mwh'])/100 - tot_net.storage.at[count7,'p_mw']
                if power_given_to_nano  >= 5900/10**6:
                    power_given_to_nano = 5900/10**6
                to_other_batteries -= power_given_to_nano

 
                tot_net.storage.at[count7,'p_mw'] +=  power_given_to_nano
                tot_net.storage.at[count7,'soc_percent'] = 100


                
            elif tot_net.storage.at[count7,'soc_percent'] + ((tot_net.storage.at[count7,'p_mw']+to_other_batteries)/tot_net.storage.at[count7,'max_e_mwh'])*100 < 100:
                print(tot_net.storage.at[count7,'soc_percent'])
                print('A')
                power_given_to_nano = to_other_batteries

                if power_given_to_nano + tot_net.storage.at[count7,'p_mw'] >= 5900/10**6:
                    print('B')
                    power_given_to_nano = 5900/10**6 - tot_net.storage.at[count7,'p_mw']

                to_other_batteries -= power_given_to_nano
                tot_net.storage.at[count7,'p_mw'] += power_given_to_nano
                tot_net.storage.at[count7,'soc_percent'] + (power_given_to_nano/tot_net.storage.at[count7,'max_e_mwh'])*100
                print(tot_net.storage.at[count7,'p_mw'])
                

            print(tot_net.storage['soc_percent'].sum())
            if tot_net.storage['soc_percent'].sum() == len(netList)*100:
                break

        for i in range(len(netList)):
            tot_net.storage.at[i,'soc_percent'] = intermediate_soc[i]
        


        print('Battery charg/discharge: ', tot_net.storage['p_mw'])


        #pp.diagnostic(tot_net)
        pp.runpp(tot_net, run_control = True, numba = False, max_iteration = 50)

        print('------------')
        print('SOC before:')
        print(tot_net.storage['soc_percent'])
        print('--------------')


        #Now for updating the battery parameters. The thought here is that is production is above load --> fill the battery. If the battey is full ---> fill another net battery.
        #If load is above production, see how much energy goes through the lines connecting the nets.

        for i in range (len(netList)):
            tot_net.storage.at[i, 'soc_percent'] += tot_net.storage.at[i, 'p_mw']/tot_net.storage.at[i,'max_e_mwh']*100

        print('------------')
        print('SOC after:')
        print(tot_net.storage['soc_percent'])
        print('--------------')

        storage_soc_list = []
        for i in range (len(netList)):
            x = tot_net.storage.at[i,'soc_percent']
            storage_soc_list.append(x)




        #net_power_list = [net_power_flow_1, net_power_flow_2, net_power_flow_3, net_power_flow_4]


            
        print('------------')
        print('Line flow:')



        for i in range(len(netList)):
            print(tot_net.res_line.at[i+26,'p_from_mw'])
            if tot_net.res_line.at[i+26,'p_from_mw']> 0:
                export_list.append(tot_net.res_line.at[i+26,'p_from_mw'])
                import_list.append(0)
            elif tot_net.res_line.at[i+26,'p_from_mw'] < 0:
                import_list.append(tot_net.res_line.at[i+26,'p_from_mw'])
                export_list.append(0)


        count10 = 3
        export_list_sum_before = sum(export_list)
        abs_gen_sum = np.abs(tot_net.res_gen['p_mw'].sum())

        while abs_gen_sum > 0:
            if tot_net.res_gen['p_mw'].sum() < 0:
                for i in range(len(netList)):

                    if export_list[count10] - abs_gen_sum > 0:
                        export_list[count10] -= abs_gen_sum
                        surplus += abs_gen_sum
                        abs_gen_sum = 0
                        break

                    elif export_list[count10] - abs_gen_sum < 0:
                        surplus += abs_gen_sum - export_list[count10]
                        abs_gen_sum -= export_list[count10]
                        export_list[count10] = 0 
                    
                    count10 -=1 
            else: 
                abs_gen_sum = 0

        
        print(export_list)
        print(import_list)
        print(tot_net.res_gen['p_mw'])

        for i in range(len(netList)):
            continue

        Battery_pmw = []
        for i in range(len(netList)):
            Battery_pmw.append(tot_net.storage.at[i,'p_mw'])

        for idx, vm in tot_net.res_bus['vm_pu'].items(): 
            df_vm_res.loc[index, idx] = vm

        for idx, p in tot_net.res_bus['p_mw'].items(): 
            df_buspower_res.loc[index, idx] = p

        for idx, pf in tot_net.res_line['p_from_mw'].items(): 
            df_lineflow_res.loc[index, idx] = pf

        for i in unmet_demand_list:
            tot_unmet_demand += i
        
        soc_list = []
        '''print(tot_net.res_line['p_from_mw'])'''
        for i in range (len(netList)):
            soc_list.append(tot_net.storage.at[i,'soc_percent'])

        count += 1

        unmet_demand_list.insert(0,timestamp)

        csv_writer.writerow(unmet_demand_list)
        SoC_lists.append(soc_list)
        import_lists.append(import_list)
        export_lists.append(export_list)
        net_power_lists.append(Battery_pmw)

        for idx, pf in tot_net.res_line['p_from_mw'].items():
            df_lineflow_res.loc[index, idx] = pf*10**6




#df_excess_energy = pd.DataFrame({'Timestamp': timestamps, 'Datapoint': excess_energy})

##df_import = pd.DataFrame({'Timestamp': timestamps, 'Datapoint': import_list})
#df_export = pd.DataFrame({'Timestamp': timestamps, 'Datapoint': export_lists})


file_path_battery = 'Results_totnet/Charge_discharge_batt.csv'
file_path_import = 'Results_totnet/imports.csv'
file_path_soc = 'Results_totnet/SoC_battery.csv'

file_path_exports = 'Results_totnet/exports.csv'
print(surplus)
with open(file_path_soc, "w", newline = '') as file:
    writer = csv.writer(file)
    header_row = []
    
    for i in value_list:
        header_row.append('Battery '+ str(i))

    writer.writerow(header_row)


    for row in SoC_lists:
        writer.writerow(row)


with open(file_path_battery, "w", newline = '') as file:
    writer = csv.writer(file)
    header_row = []
    
    for i in value_list:
        header_row.append('Battery '+ str(i))

    writer.writerow(header_row)


    for row in net_power_lists:
        writer.writerow(row)


with open(file_path_import, "w", newline = '') as file:
    writer = csv.writer(file)
    header_row = []
    
    for i in value_list:
        header_row.append('Nanogrid '+ str(i))

    writer.writerow(header_row)


    for row in import_lists:
        writer.writerow(row)


with open(file_path_exports, "w") as file:
    writer = csv.writer(file)
    header_row = []
    
    for i in value_list:
        header_row.append('Nanogrid '+ str(i))
    
    writer.writerow(header_row)

    for row in export_lists:
        writer.writerow(row)


with open(file_path_excess_results_tot, "w") as file:
    writer = csv.writer(file)
    header_row = []
    
    for i in value_list:
        header_row.append('Nanogrid '+ str(i))
    
    writer.writerow(header_row)

    for row in excess_energy:
        writer.writerow(row)


with open(file_path_voltage_results_tot, "w") as file:
    df_vm_res.to_csv(file, index= False)


with open(file_path_powerflow_results_tot, "w") as file:
    df_lineflow_res.to_csv(file, index= False)

with open(file_path_power_results_tot, "w") as file:
    df_buspower_res.to_csv(file, index= False)

file_eco_moyo = 'Results_totnet/eco_moyo_load_met.csv'


data_2d = np.array(load_list).reshape(-1, 1).tolist()

with open(file_eco_moyo, "w",newline = '') as file:
    writer = csv.writer(file)
    header_row = []
    header_row.append('Nanogrid 1')
    writer.writerow(header_row)
    writer.writerows(data_2d)


print('Total unmet demand for the week: ', tot_unmet_demand)




tot_eco_export = 0
tot_eco_import = 0
tot_eco_nano = 0


for i in export_lists:
    tot_eco_export += i[0]

for i in import_lists:
    tot_eco_import += i[0]

for i in load_list2:
    tot_eco_nano += i


print('Total eco moyo nanogrid export: ', tot_eco_export,'. Total Eco moyo import: ',tot_eco_import)
print('Total eco moyo export to own nanogrid: ', tot_eco_nano)
print(tot_eco_export + tot_eco_nano)
        
