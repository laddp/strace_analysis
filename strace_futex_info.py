#!/usr/bin/python
import sys
from pprint import pprint

ops = {}
retcodes = {}
rettimes = {}
call_count = 0
return_count = 0
linenum = 0

timed_wait = 0
untimed_wait = 0

with open(sys.argv[1]) as stracef:
    for line in stracef:
        linenum += 1
        if 'resumed' not in line and 'killed by' not in line and 'exited with' not in line and '--- SIG' not in line:
            call = line.split()[2].split('(')[0]

            if call != "futex":
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
                call = line.split()[3]

                if call != "futex":
                    continue
                
                return_count += 1
                retcode = line.split()[4]

            except:
                print("parse error at line", linenum)
                print(line)

#pprint(calls)
ops = dict(sorted(ops.items(), key=lambda item: item[1], reverse=True))
for op, count in ops.items():
    print(op, count, f"{(count/call_count * 100):.1f}%")
print("Returned:", return_count)
print("Timed waits:", timed_wait, "Untimed waits:", untimed_wait)
