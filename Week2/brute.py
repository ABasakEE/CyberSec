from pwn import *
#importing pwntools

file = 'wordlist.txt'

lines=list()

with open(file,'r') as f:
    while True:
        line=f.readline()
        if not line:
            break
        lines.append(line.strip())

n=len(lines)
print("Size:",n)

#sort the strings lexicographically
lines=sorted(lines)
print("Done sorting")

#start interacting with the ELF file
low,high=0,n-1
#start binary search

while (low<=high):
    sh=process('./bruteforcer')
    mid=(low+high)//2
    pwd=lines[mid]
    sh.sendline(pwd.encode('utf-8'))
    response=sh.recvline(timeout=1).decode('utf-8')
    sh.close()
    if ('high' in response): #target is lower
        high=mid-1
    elif ('low' in response): #target is higher
        low=mid+1
    else:
        print("Correct password:",pwd)
        break



