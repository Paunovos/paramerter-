import pandas
import pandas as pd
from Vehicle import *
import csv
import pandas as pd
import numpy as np


def load_data(filename, column_names=None):
    csv = pd.read_csv(f"data/{filename}.csv", delimiter=";", decimal=",", index_col=0)
    if column_names:
        csv.columns = column_names
    return csv


consumption_col_names = ["consumption", "fuel", "emission","typ"]
pef_col_names     = ["2014", "2022", "2025"]
scenarios_col_names    = ["scenario0", "scenario1", "scenario2"]
stages_col_names       = ['stage0', 'stage1', 'stage2', 'stage3']

# load csv data/können die Namen der Spalten nicht aus der CSV gelesen werden?

pf = load_data("primaer_faktoren", column_names=pef_col_names)
sc = load_data("simple_consum", column_names=consumption_col_names)
ms = load_data("modal_split", column_names=scenarios_col_names)
es = load_data("electric_share", column_names=stages_col_names)

#print(sc)

vehicles_ = []
for i, vehicle_ in sc.iterrows():
    # append to list
    vehicles_.append(
        # create a new vehicle with name = row_name and
        # corresponding consumption and fuel typ
        Vehicle(i, vehicle_[consumption_col_names[1]],
                   vehicle_[consumption_col_names[2]],
                   vehicle_[consumption_col_names[3]],
                   vehicle_[consumption_col_names[0]]))

year     = ['2014','2022','2025']
scenario = ["scenario0", "scenario1", "scenario2"]
stage    = ['stage0','stage1','stage2', 'stage3']
#WeitereVariable =['X','Y','Z']

sums = {}
df_results = sc.copy()
for y in year:
    dic = calc_energy_needs(vehicles_, pf, y)
    #df = pd.DataFrame(dic.items(), columns=['x', 'y'])
    #df_results['energy_needs_%s' %y] = df['y'].values
    for s in stage:
        dic2 = calc_share(vehicles_, es, s)
        #df2 = pd.DataFrame(dic2.items(), columns=['x', 'y'])
        #df_results['ev_adoption_%s_%s' %(y,s)] = df2['y'].values
        for z in scenario:
            dic3 =calc_energy(vehicles_,ms,z)
            sums[f"sum_ev_share_{y}_{s}_{z}"] = sum(dic3.values())
            df3 = pd.DataFrame(dic3.items(), columns=['x','y'])
            df_results['ev_share_%s_%s_%s' %(y,s,z)] = df3['y'].values

#Emissionen der einzelnen Fahrzeuge mit Primärenergeifaktoren gewichten.
#Emissioen nach Energieträgern sind in Simple_Consum und die Primärenergiefaktoren sind in primar_faktoren.


for y in year:
    dic =calc_emissions(vehicles_, pf,y)
    df = pd.DataFrame(dic.items(), columns=['x','y'])
    df_results['emissions_%s'%y] =df['y'].values
    for s in stage:
        dic2 =calc_emission_share(vehicles_, es, s)
        df2 = pd.DataFrame(dic2.items(), columns=['x', 'y'])
        df_results['emissions_%s_%s' %(y,s)] = df2['y'].values
        for z in scenario:
            dic3 = calc_emission_scen(vehicles_, ms, z)
            sums[f"sum_emissions_{y}_{s}_{z}"] = sum(dic3.values())
            df_results['emission_share_%s_%s_%s' %(y,s,z)] = df3['y'].values


#print(df_results.round(3))
dfr = df_results.round(3)


print(dfr)
with open('Summen_von_Teilszenarien.csv', 'w') as f:
    for key in sums.keys():
        f.write("%s;%s\n"%(key,sums[key]))
dfr.to_csv('RESULTS.csv', decimal='.', sep=';')
print(sums)
import matplotlib.pyplot as plt

# #df_results.plot(y=["ev_share_2025_stage2_scen3", "ev_share_2014_stage2_scen3"], kind="bar")
# #df_results.plot(y=["emissions_2014","emissions_2022", 'emissions_2025'], kind="bar")
# df_results.plot(y=["energy_needs_2022", 'emissions_2022'], kind="bar")
# df_results.plot(y=["emissions_2022", 'emissions_2025'], kind="bar")
#
# #df_results[["ev_adoption_2022_stage0", "ev_adoption_2022_stage1", "ev_adoption_2014_stage2",
#            # 'ev_adoption_2014_stage3']].plot(kind="bar")
# plt.xlabel('Vehicle typ')
# plt.ylabel('THG-Emissionen in kg/100Pkm')
# plt.title('Treibhausgasemissioen')
# plt.show()