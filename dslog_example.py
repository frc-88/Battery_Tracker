from dslogs.dslogstream import DsLogStream

with open("2024_01_04 20_48_11 Thu.dslog", 'rb') as file:
    for entry in DsLogStream(file):
        print(entry.voltage, entry.pdp_data.currents)
