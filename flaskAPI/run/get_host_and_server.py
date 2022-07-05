import json

setup = json.load(open('/home/onos/Downloads/flaskSDN/flaskAPI/set_up/set_up_topo.json'))


not_sw = sum(setup['bridges'], [])

# sw_full = ['s'+str(i) for i in range(1, 92)]

for ctl in setup["controllers"]:
    for sw in ctl['switches']:
        if sw not in not_sw:
            print(sw)