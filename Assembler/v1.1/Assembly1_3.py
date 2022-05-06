
from tkinter import *
from tkinter import messagebox
from tokenize import String

root = Tk()
root.title("Assembly")
#root.iconbitmap('')
root.geometry("500x450")

#register locations in the cpu
registersA={
        "R0":"0","R1":"1","R2":"2","R3":"3",
        "R4":"4","R5":"5","R6":"6","R7":"7",
        "R8":"8","R9":"9","R10":"A","R11":"B",
        "R12":"C","R13":"D","R14":"E","R15":"F",
    }

#16 instructions present in ISA and additional instructions
Opcode = {
        "ADD":'0', "SUB":'1', "MULT":'2',"DIV":'3',
        "SHL":'4', "SHR":'5',"AND":'6', "OR":'7',
        "MOVR":'8',"MOVI":'9', "LOAD":'A', "STORE":'B',
        "JMP":'C', "JMPZ":'D', "JMPN":'E', "HALT": 'F',
        "NOP":'F',
        }

#counter for aligning output
counter=1
outputs="v2.0 raw\n"+"F000\t"
instructionNum=0

#function to open file
def open_txt():
    global outputs
    text_file = open("Test.txt", "r")
    stuff = text_file.read()

    my_text.insert(END,stuff)
    text_file.close()

#function to save edits to file content
def save_txt():
    text_file = open("Test.txt", "w")
    text_file.write(my_text.get(1.0,END))

#converts instructions with 3 operands into hexcode
def aluInstruction(opcode,registers):
    word=""
    registerO=[]
    #ADDC is a coagulated instruction consisting of 2 immediate value
    #moves and an add instruction
    if "ADDC" in opcode:
        if len(registers[0])==1:
                registers[0]="0"+registers[0]
        if len(registers[1])==1:
            registers[1]="0"+registers[1]
        word+=Opcode["MOVI"]+registersA["R1"]+registers[0]+"\t"
        word+=Opcode["MOVI"]+registersA["R2"]+registers[1]+"\t"
        word+=Opcode["ADD"]+registersA["R1"]+registersA["R2"]+registersA[registers[2]]+"\t"
        output(word)
        return
    for i in range(len(registers)):
            registerO.append(registersA[registers[i]])
    word+=Opcode[opcode]
    for i in registerO:
            word+=i    
    word+="\t"
    output(word)
    
#converts instructions with 2 operands into hex code
def iInstructions(opcode,registers):
    word=""
    registerO=[]
    #MOVR has 2 operands but does  not make use of the last 4 bits
    #in the instruction and hence is converted separately
    if(opcode=="MOVR"):
        word+=Opcode[opcode]
        for i in range(len(registers)):
            registerO.append(registersA[registers[i]])
        for i in registerO:
            word+=i
        word+="0"
        word+="\t"
    
    else:
        word+=Opcode[opcode]
        word+=registersA[registers[0]]
        if len(registers[1])==1:
            word+="0"
        word+=registers[1]
        for i in registerO:
            word+=i
        word+="\t"
    output(word)

#converts instructions with 1 operand into hexcode
def jInstructions(opcode,registers):
    word=""
    word+=Opcode[opcode]
    if len(registers[0])==1:
        word+="0"
    word+=registers[0]
    word+="\t"
    output(word)

#converts HALT and NOP instructions into hexcode
def cInstructions(opcode):
    word=""
    if "HALT" in opcode:
        word+="FFFF"
    else:
        word+="F000"
    word+="\t"
    output(word)

#concatenates all hexcodes into a single string to be displayed in a file
def output(word):
    global counter
    global outputs
    if  counter<8:
        outputs+=word
        counter+=1
    elif counter>=8:
        outputs+="\n"
        outputs+=word
        counter=1
        
#function triggered on button press which runs all the required functions
#convert the instructions into hexcode
def Assemble():
    global outputs
    global instructionNum    
    f = open("Test.txt","r")
    for i in f:
        if (instructionNum<127):
            instructionNum+=1
            i=i.strip()
            if ("HALT" in i) or ("NOP" in i):
                cInstructions(i)
                continue
            else:
                opcode,registers=i.split()
                registers=list(registers.split(","))
                if len(registers)==3:
                    aluInstruction(opcode,registers)
                elif len(registers)==2:
                    iInstructions(opcode,registers)
                elif len(registers)==1:
                    jInstructions(opcode,registers)

            
                 
    #string is displayed in text file       
    print(outputs)
    w = open("Output.txt","w")
    w.write(outputs)  

my_text = Text(root, width=40, height=10, font=("Helvetica",16))
my_text.pack(pady=20)

open_button = Button(root, text="Open Text File",command= open_txt)
open_button.pack(pady=20)

save_button = Button(root, text="Save File", command=save_txt)
save_button.pack(pady=20)

myButton = Button(root, text="Assemble", command=Assemble )
myButton.pack()


root.mainloop()