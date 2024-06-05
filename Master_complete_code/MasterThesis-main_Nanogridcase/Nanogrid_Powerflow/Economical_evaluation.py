EUR_exrate = 142.87
Energy_price = 27.95
discount_rate = 0.12

numb_PV = 24
numb_batt = 6


PV_price = 20000/EUR_exrate
batt_price = 33000/EUR_exrate
Inv_price = 155000/EUR_exrate
Labor_price = 150000/EUR_exrate
Energy_price_EUR = Energy_price/EUR_exrate


PV_lifetime = 30
batt_lifetime = 5
Inv_lifetime = 15
Project_lifetime = 10

Yearly_export_nano = 15.023*52
Yearly_export_micro = (75.740 + 19.780)*52

yearly_tot_prod_nano =  297.958*52 #137.376*52 
yearly_tot_prod_micro = 0

#print(PV_price, batt_price, Inv_price, Labor_price)

print('############     Nanogrid case    ################')


print('Year 0: investments: ', (PV_price*numb_PV + batt_price*numb_batt + Inv_price + Labor_price)/(1 + discount_rate)**0)
print('Year 5: investments: ', (batt_price*numb_batt)/(1 + discount_rate)**5)
tot_inv = (PV_price*numb_PV + batt_price*numb_batt + Inv_price + Labor_price)/((1 + discount_rate)**0) + (batt_price*numb_batt)/((1 + discount_rate)**5)
print('Total: ', tot_inv)


temp = 0
for i in range(1,Project_lifetime + 1):
    temp += Yearly_export_nano*Energy_price_EUR/(1 + discount_rate)**i
    print(f'Year {i} accumulated earnings: ',temp)

total_earnings = temp

print('Residual value:')

print('PV: ', (numb_PV*PV_price*2/3)/(1 + discount_rate)**10)
print('Inverter: ', (Inv_price/3)/(1 + discount_rate)**10)
tot_res = numb_PV*(PV_price*2/3)/(1 + discount_rate)**10 + (Inv_price/3)/(1 + discount_rate)**10
print('Sum: ', tot_res)


temp = 0
for i in range(1,Project_lifetime + 1):
    temp += yearly_tot_prod_nano /(1 + discount_rate)**i
    print(f'Year {i} production: ', temp)

new_tot_prod = temp

print('')

print('Total investments: ', tot_inv)
print('Total earnings: ', total_earnings)
print('Total residual value: ', tot_res)
print('Total production: ',new_tot_prod)

npv = tot_inv - total_earnings - tot_res
Lcoe = (npv)/new_tot_prod


print('')
print('--------------------')

print('NPC: ', npv)
print('LOCE: ', Lcoe)

print('Percent reduction of LCOE compared to base case: ', 100*(1-Lcoe/0.07800888374625774) )



print('############     Microgrid case    ################')

temp = 0
for i in range(1,Project_lifetime + 1):
    temp += Yearly_export_micro*Energy_price_EUR/(1 + discount_rate)**i
    print(f'Year {i}: earnings: ',temp)

total_earnings = temp


temp = 0
for i in range(1,Project_lifetime + 1):
    temp += yearly_tot_prod_nano/(1 + discount_rate)**i
    print(f'Year {i} production: ', temp)

new_tot_prod = temp

print('')

print('Total investments: ', tot_inv)
print('Total earnings: ', total_earnings)
print('Total residual value: ', tot_res)
print('Total production: ',new_tot_prod)

npv = tot_inv - total_earnings - tot_res
Lcoe = (npv)/new_tot_prod


print('')
print('--------------------')

print('NPC: ', npv)
print('LOCE: ', Lcoe)
print('Percent reduction of LCOE compared to base case: ', 100*(1-Lcoe/0.07800888374625774) )