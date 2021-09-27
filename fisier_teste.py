idd = "pompa"
values = {'motor': 0, 'heater':0, 'pompa': 0}
if idd in values:
    print("ham")

values[idd] = not values[idd]
