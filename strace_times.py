#!/usr/bin/python
import sys
from pprint import pprint

calls = {}
call_count = 0
linenum = 0

resumed_string = " resumed>) = "

with open(sys.argv[1]) as stracef:
    for line in stracef:
        linenum += 1
        if 'resumed' in line:
            try:
                call = line.split()[3]
                call_count += 1

                call_time = line.split(' ')[-1]

                if call_time == "?\n":
                    continue
                else:
                    call_time = float(call_time[1:-2])

                if call in calls:
                    newmin = min(call_time, calls[call][2])
                    newmax = max(call_time, calls[call][3])
                    calls[call] = ( calls[call][0] + 1, calls[call][1] + call_time, newmin, newmax )
                else:
                    calls[call] = ( 1, call_time, call_time, call_time )
            except:
                print("parse error at line", linenum)
                print(line)

#pprint(calls)
calls = dict(sorted(calls.items(), key=lambda item: item[1][0], reverse=True))
for call, call_data in calls.items():
    print(call, call_data[0], f"{call_data[1]:.8f}", f"{call_data[2]:.8f}", f"{call_data[3]:.8f}", f"{(call_data[1]/call_data[0]):.8f}")
