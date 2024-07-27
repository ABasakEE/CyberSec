# flag{f34r1355_5ud0ku_c0nqu3r0r}
# Final flag obtained

from pwn import *

sh=process('./sudoku')

lines=[]
ans=[]

def getBox(row,column)->int:
    #takes row and column value and returns a mapping to the box number 
    #boxes are numbered 0,1,2,3, ... starting from the top left
    x=row//3
    y=column//3
    
    #   0 | 1 | 2
    # 0| 0  1   2
    # 1| 3  4   5   
    # 2| 6  7   8
    
    return x*3+y

def generateHashmaps(sudoku)->list:
    #generate the hashmaps first
    base=list()
    for i in range(10):
        base.append(-1)
        
    rows=list()
    columns=list()
    boxes=list()   
    
    for i in range(9):   
        rows.append(list(base))#nine rows
        columns.append(list(base)) #nine columns
        boxes.append(list(base)) #nine boxes
    
    
    for i in range(9):
        for j in range(9):
            elem=sudoku[i][j]
            if elem==0:
                continue #we need to fill them later for the solutions
            if rows[i][elem]==-1:
                rows[i][elem]=1 #the element is present in the ith row
            if columns[j][elem]==-1: 
                columns[j][elem]=1 #the element is present in the jth column
            box=getBox(i,j)
            if boxes[box][elem]==-1:
                boxes[box][elem]=1 #the element is present in this box
    
    
    #start the recursive call
    solveSudoku(sudoku,rows,columns,boxes)
    return ans
    
    
def findEmptyCell(board):   
    flag=False
    row,column=-1,-1
    for i in range(9):
        for j in range(9):
            if board[i][j]==0: #empty cell found
                flag=True
                row=i
                column=j
                break
        if flag:
            break  
    return (row,column)

answerBoard=list()

def solveSudoku(board,rows,columns,boxes)->bool:
    #use backtracking and recursion to solve the question
    #keep track of allowed states by using a hashmap
    
    #find an empty cell first
    row,column=findEmptyCell(board)
    
    
    if row==column==-1: #no empty cell found, means we have a solution  
        return True
        #copy contents of board to list and then return
        
   #that is not the case, we can iterate through 1-9 and see if any of them fit here
    box=getBox(row,column)
    for i in range(1,10):
        if rows[row][i]==1: #that element is present in the row
            continue
        if columns[column][i]==1: #that element is present in the column
            continue
        if boxes[box][i]==1: #that element is present in the box
            continue 
        
        #none of these cases, we can place the element in this cell
        #try this combination        
        #print("Tried at",row,column)
        board[row][column]=i
        rows[row][i]=1
        columns[column][i]=1
        boxes[box][i]=1
        
        if solveSudoku(board,rows,columns,boxes): #found solution
            return True
        
        #solution not found
        #now empty this for another element try
        board[row][column]=0
        rows[row][i]=-1
        columns[column][i]=-1
        boxes[box][i]=-1
    
    #no valid solution found till now
    return False       
        
        
    
answers=list()
sudoku=list()

count=420 #number of games

while (count>0):
    input=sh.recvuntil("):",timeout=0.5)
    if len(input)==0:
        continue
    strings=input.decode('utf-8').split('\n')
    
    #create the sudoku board    
    sudoku.clear()
    
    for line in strings:
        row=list() #create the row array            
        if '-' in line: #skip these lines, they are the bordering ones
            continue
        #process only if length of lines is 25 characters        
        for char in line:
            if char=='.':
                row.append(0)
            elif ord('0')<=ord(char)<=ord('9'): #check if it is a number
                row.append(int(char))
        if len(row)==9: #further check if the row is non empty and then append
            sudoku.append(row)
    
    if len(sudoku)==9:
        #keep track of which cells to fill here
        answers.clear()
        
        for i in range(9):
            for j in range(9):
                if sudoku[i][j]==0:
                    #append the required answer position tuple to the list
                    answers.append((i,j))
        generateHashmaps(sudoku)
        
        #send out all the lines
        for indices in answers:
            row,column=indices[0],indices[1]
            solution=sudoku[row][column]
            line=str(row)+" "+str(column)+" "+str(solution)+chr(10)
            sh.sendline(line.encode('utf-8'))
        #use this to prepare the terminal for the next input
        sh.recvuntil("solved!",timeout=0.5)
    print("Game Count",count)    
    count-=1       

l=sh.recvline_contains('flag',timeout=0.5)
f=l.decode('utf-8')
ind=f.find("{") #start of flag
print("Final output:\n",f)
flag=f[ind:]
print("Flag:",flag)