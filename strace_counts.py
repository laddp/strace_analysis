#!/usr/bin/python
import sys
from pprint import pprint
from datetime import datetime

start_time = 0
end_time = 0
linenum = 0

calls = {}
call_count = 0

with open(sys.argv[1]) as stracef:
    for line in stracef:
        linenum += 1
        if linenum == 1:
            start_time = line.split()[1]
        end_time = line.split()[1]

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
start = datetime.fromtimestamp(float(start_time))
end = datetime.fromtimestamp(float(end_time))
elapsed_time = end - start
print("Trace start:", start, "Trace end:", end, "Duration:", elapsed_time, "\n")

calls = dict(sorted(calls.items(), key=lambda item: item[1], reverse=True))
print("call", "count", "%total", "per_sec")
for call, count in calls.items():
    print(call, count, f"{(count/call_count * 100):.1f}%", f"{(count/elapsed_time.seconds):.2f}")
