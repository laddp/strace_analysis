#!/usr/bin/python
import sys
from datetime import datetime

linenum = 0
start_time = 0
end_time = 0

call_count = 0
ops = {}
timed_wait = 0
untimed_wait = 0

return_count = 0
retcodes = {}
minret = 9999999999999999999999999.9
maxret = 0.0
total_time = 0.0

with open(sys.argv[1]) as stracef:
    for line in stracef:
        linenum += 1
        if linenum == 1:
            start_time = line.split()[1]
        end_time = line.split()[1]

        if 'resumed' not in line and 'killed by' not in line and 'exited with' not in line and '--- SIG' not in line:
            rettime = line.split()[2].split('(')[0]

            if rettime != "futex":
                continue

            call_count += 1
            futex_op = line.split()[3][:-1]
            if futex_op in ops:
                ops[futex_op] = ops[futex_op] + 1
            else:
                ops[futex_op] = 1

            if futex_op == "FUTEX_WAIT_PRIVATE":
                if line.split()[5] == "NULL":
                    untimed_wait += 1
                else:
                    timed_wait += 1

        if 'resumed' in line:
            try:
                rettime = line.split()[3]

                if rettime != "futex":
                    continue
                
                call_time = line.split(' ')[-1]

                if call_time == "?\n":
                    continue
                else:
                    call_time = float(call_time[1:-2])

                minret = min(call_time, minret)
                maxret = max(call_time, maxret)
                total_time += call_time

                return_count += 1
                retcode = line.split()[6]

                if retcode in retcodes:
                    retcodes[retcode] += 1
                else:
                    retcodes[retcode] = 1

            except:
                print("parse error at line", linenum)
                print(line)

start = datetime.fromtimestamp(float(start_time))
end = datetime.fromtimestamp(float(end_time))
elapsed_time = end - start
print("Trace start:", start, "Trace end:", end, "Duration:", elapsed_time, "\n")

print("futex opcodes:")
print("call count:", call_count)
ops = dict(sorted(ops.items(), key=lambda item: item[1], reverse=True))
for op, count in ops.items():
    print(op, count, f"{(count/call_count * 100):.1f}%")
print("Timed waits:", timed_wait, "Untimed waits:", untimed_wait)

print("\nReturned:", return_count)
for retcode, count in retcodes.items():
    print(retcode, count)
print("Total times:", total_time, "Min:", f"{minret:.8f}", "Max:", f"{maxret:.8f}", "Average:", f"{(total_time/return_count):.8f}")
print("Calls/sec:", call_count / elapsed_time.seconds)
print()