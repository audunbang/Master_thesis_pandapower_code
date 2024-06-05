"""
#Creating the EcoMoyo bus 
bus_EcoMoyo = pp.create_bus(net, vn_kv=23, index = 1, name = 1)

#Creating residental load buses
bus_res1 = pp.create_bus(net, vn_kv=23, index = 2, name = 2)
bus_res2 = pp.create_bus(net, vn_kv=23, index = 3, name = 3)
bus_res3 = pp.create_bus(net, vn_kv=23, index = 4, name = 4)
bus_res4 = pp.create_bus(net, vn_kv=23, index = 5, name = 5)
bus_res5 = pp.create_bus(net, vn_kv=23, index = 6, name = 6)

#Creating hospital, farm and church buses

bus_hospital = pp.create_bus(net, vn_kv=23, index = 7, name = 7)
bus_farm = pp.create_bus(net, vn_kv=23, index = 8, name = 8)
bus_church = pp.create_bus(net, vn_kv=23, index = 9, name = 9)

#Creating lines

pp.create_line(net, from_bus=bus_EcoMoyo, to_bus=bus_res1, length_km=0.15, std_type="679-AL1/86-ST1A 220.0")
pp.create_line(net, from_bus=bus_EcoMoyo, to_bus=bus_res2, length_km=0.15, std_type="679-AL1/86-ST1A 220.0")
pp.create_line(net, from_bus=bus_EcoMoyo, to_bus=bus_res3, length_km=0.15, std_type="679-AL1/86-ST1A 220.0")
pp.create_line(net, from_bus=bus_EcoMoyo, to_bus=bus_res4, length_km=0.15, std_type="679-AL1/86-ST1A 220.0")
pp.create_line(net, from_bus=bus_EcoMoyo, to_bus=bus_res5, length_km=0.15, std_type="679-AL1/86-ST1A 220.0")
pp.create_line(net, from_bus=bus_EcoMoyo, to_bus=bus_hospital, length_km=0.15, std_type="679-AL1/86-ST1A 220.0")
pp.create_line(net, from_bus=bus_EcoMoyo, to_bus=bus_farm, length_km=0.15, std_type="679-AL1/86-ST1A 220.0")
pp.create_line(net, from_bus=bus_EcoMoyo, to_bus=bus_church, length_km=0.15, std_type="679-AL1/86-ST1A 220.0")

#Creating loads and generation, with Eco Moyo as slack bus

pp.create_gen(net, bus=bus_EcoMoyo, p_mw = 1, slack = True)
pp.create_load(net, bus=bus_EcoMoyo, p_mw=1)
pp.create_load(net, bus=bus_res1, p_mw=1)
pp.create_load(net, bus=bus_res2, p_mw=1)
pp.create_load(net, bus=bus_res3, p_mw=1)
pp.create_load(net, bus=bus_res4, p_mw=1)
pp.create_load(net, bus=bus_res5, p_mw=1)
pp.create_load(net, bus=bus_hospital, p_mw=1)
pp.create_load(net, bus=bus_farm, p_mw=1)
pp.create_load(net, bus=bus_church, p_mw=1)
"""