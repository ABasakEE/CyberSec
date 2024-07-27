#include <stdio.h>
#include <stdlib.h>

#define TAPE_SIZE 30000
#define STACK_SIZE 10000

void execute_brainfuck(const char *code) {
    char tape[TAPE_SIZE] = {0};
    char *ptr = tape;
    const char *pc = code;
    const char *start = code; //store the address of the first char in the char[] array

    int stack[STACK_SIZE]; //create a stack for storing jump instructions for []
    int *stackPtr = stack;
    int pointer=0;


    //first create the dictionary of jump instructions 
    int left[STACK_SIZE];
    int right[STACK_SIZE]; 

    for (int i=0;i<STACK_SIZE;i++){
        stack[i]=-1;
        left[i]=-1;
        right[i]=-1;
    }

    //we assume that a correct brainfuck program has been passed to the user
    //i.e. all brackets will be matched by the end of the program
    int index=0;
    while (*pc)
    {
        index=pc-start; //index from the start of the char[] array
        //printf("Index %d\n",index);
        switch(*pc)
        {
            case '[':
            *stackPtr=index;
            //printf("Pushing %d at pos %p\n",index, (void *)stackPtr);
            stackPtr++;
            break;

            case ']':
            stackPtr--;
            int pos=*stackPtr; //the position of the last [ stored at the previous pos
            //printf("Storing left %d and right %d\n",pos,index);
            left[pos]=index;
            right[index]=pos;

            //pop the element from stack
            //the pointer is now one move address away from the top of the stack
            *stackPtr=-1;
            break;

        }
        pc++;
    }
    /*printf("Printing dicts\n");
    for (int i=0;i<TAPE_SIZE;i++)
        {if (left[i]!=-1)
            printf("%d ",left[i]);
        if (right[i]!=-1)
            printf("%d ",right[i]);}
    printf("Finished Printing\n");*/


    pc=code; //restart the traversal

    while (*pc) {
        index=pc-start;
        //printf("Index %d\n",index);
        switch (*pc) {
            case '>':
                //move the tape pointer ahead by one
                ptr++;
                break;
            case '<':
                //move the tape pointer back by one
                ptr--;
                break;
            case '+':
                //increase the value at that pointer by one
                (*ptr)++;
                break;
            case '-':
                //decrease the value at that pointer by one
                (*ptr)--;
                break;
            case '.':
                //print the value at that pointer to stdout
                putchar(*ptr);
                break;
            case ',':
                //accept a character from the user and store it at that pointer
                *ptr=getchar();
                break;
            case '[':
                //use the dictionary to jump to the next ] statement if the value is zero
                if (*ptr==0)
                    pc=start+left[index];
                break;
            case ']':
                // use the dictionary to jump to the previous [ statement is value is non zero
                if (*ptr!=0)
                    pc=start+right[index];
                break;
            default:
                break;
        }
        //printf("%p\n",(void *)pc);
        ++pc;
    }
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s \"<brainfuck code>\"\n", argv[0]);
        return 1;
    }

    execute_brainfuck(argv[1]);

    return 0;
}