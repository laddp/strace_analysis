#!/usr/bin/python
import sys
from pprint import pprint

ops = {}
retcodes = {}
rettimes = {}
call_count = 0
return_count = 0
linenum = 0

with open(sys.argv[1]) as stracef:
    for line in stracef:
        if 'resumed' not in line and 'killed by' not in line and 'exited with' not in line and '--- SIG' not in line:
            call = line.split()[2].split('(')[0]

            if call != "futex":
                continue

            call_count += 1
            futex_op = line.split()[3]
            if futex_op in ops:
                ops[futex_op] = ops[futex_op] + 1
            else:
                ops[futex_op] = 1
        if 'resumed' in line:
            try:
                call = line.split()[3]

                if call != "futex":
                    continue

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

                retcode = line.split()[4]

            except:
                print("parse error at line", linenum)
                print(line)

#pprint(calls)
ops = dict(sorted(ops.items(), key=lambda item: item[1], reverse=True))
for op, count in ops.items():
    print(op, count, f"{(count/call_count * 100):.1f}%")
