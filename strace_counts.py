#!/usr/bin/python
import sys
from pprint import pprint

calls = {}
call_count = 0
with open(sys.argv[1]) as stracef:
    for line in stracef:
        if 'resumed' not in line and 'killed by' not in line and 'exited with' not in line and '--- SIG' not in line:
            call = line.split()[2].split('(')[0]
            call_count += 1
            # if call == '---' or call == '+++':
            #     print(line)
            if call in calls:
                calls[call] = calls[call] + 1
            else:
                calls[call] = 1

#pprint(calls)
calls = dict(sorted(calls.items(), key=lambda item: item[1], reverse=True))
for call, count in calls.items():
    print(call, count, f"{(count/call_count * 100):.1f}%")
