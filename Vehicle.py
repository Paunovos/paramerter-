class Vehicle:

    def __init__(self, name, fuel, emissions, typ, consumption):
        self.name = name
        self.fuel = fuel
        self.emissions = emissions
        self.typ = typ
        self.consumption = consumption
        self.real_energy_need = None
        self.real_emissions   = None
        self.energy_sum       = None
        self.ev_adoption      = None
        #self.energy_sum_car = None
        #self.energy_sum_bus = None


#multiply energy consumption with with "PEF"
def calc_energy_needs(vehicles, consume_table, year):
    dic = {}
    for v in vehicles[:-1]:
        v.real_energy_need = v.consumption * consume_table.at[v.fuel, year]
        dic[v.name] = v.real_energy_need
    dic["sum"] = sum(dic.values())
    return dic

#multiply energy needs with with "stages"
#multiply EMISSIONS  with with "stages"
def calc_share(vehicles, consume_table, stage):
    dic = {}
    for v in vehicles[:-1]:
        v.ev_adoption = v.real_energy_need * consume_table.at[v.name, stage]
        dic[v.name] = v.ev_adoption
    dic["sum"] = sum(dic.values())
    return dic
#multiply EV-adoption with with "Scenario"
#multiply EMISSIONS2 with with "scenarios"

def calc_energy(vehicles, consume_table, scenario):
    dic = {}
    for v in vehicles[:-1]:
        v.energy_sum = v.ev_adoption * consume_table.at[v.typ, scenario]
        dic[v.name] = v.energy_sum
    dic["sum"] = sum(dic.values())
    return dic

#EMISSION
def calc_emissions(vehicles, consume_table, year):
    dic = {}
    for v in vehicles:
        v.real_emissions = v.consumption * consume_table.at[v.fuel, year] * v.emissions
        dic[v.name] = v.real_emissions
    return dic

def calc_emission_share(vehicles, table, stage):
    dic = {}
    for v in vehicles:
        v.ev_adoption2 = v.real_emissions * table.at[v.name, stage]
        dic[v.name] = v.ev_adoption2
    return dic

def calc_emission_scen(vehicles, table, scenario):
    dic = {}
    for v in vehicles:
        b = v.ev_adoption2 * table.at[v.typ, scenario]
        dic[v.name] = b
    return dic


#ADDITION
def addition_energy (vehicles,table scenario)
    dic = {}
    v.energy_sum_car = 0
    v.energy_sum_bus = 0
    v.energy_sum_people_mover = 0
    for v in vehicles:
        if v.type == "car":
            v.energy_sum_car += v.energy_sum
            dic[v.typ] =car
        elif v.type == 'bus':
            v.energy_sum_bus += v.energy_sum
            dic[v.typ] =bus
        elif v.type == 'people_mover':
            v.energy_sum_people_mover += v.energy_sum
            dic[v.typ] = movr
    return dic
    #total_energy_need = v.energy_sum_car + v.energy_sum_bus + v.energy_sum_people_mover
