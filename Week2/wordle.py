from pwn import *
chars=list()

#creating the dictionary of possible letters
for i in range(ord('A'),ord('Z')+1):
    chars.append(chr(i))
for i in range(ord('a'),ord('z')+1):
    chars.append(chr(i))
for i in range(ord('0'),ord('9')+1):
    chars.append(chr(i))
chars.extend('_')



length=30 #password in 30 characters long

string=chars[0]*30
print(string)
pwd=""
countCurr=0
countPrev=0


for i in range(length):
    for ch in chars:
        sh=process('./notwordle')
        guess=pwd+ch+string[i+1:] #creating the guess for the password
        sh.sendline(guess.encode('utf-8'))
        response=sh.recvline(timeout=1).decode('utf-8') #receives all lines from input
        sh.close()
        ind=response.find('/') #find index of this symbol
        countCurr=int(response[ind-3]+response[ind-2]) #for 2 digit numbers
        if (countCurr>countPrev):
            countPrev=countCurr #already checked that all As do not match
            pwd=pwd+ch #adding elements to the correct password
            break

print("Correct password:",pwd)
            
        
        
