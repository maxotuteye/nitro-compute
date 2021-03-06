from re import M
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

root = Tk()
root.title("NitroCompute Assembler")
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

def Assemble():
    global outputs
    global instructionNum
    global counter
    instructionNum=0
    counter=1
    outputs="v2.0 raw\n"+"F000\t"
         
    f = open("Test.txt","r")
    for i in f:
        if (instructionNum<127):
            i=i.strip()
            if ("HALT" in i) or ("NOP" in i):
                cInstructions(i)
                continue
            else:
                try:
                    opcode,registers=i.split()
                except:
                    messagebox.showerror("Error","Cannot assemble trailing spaces.\nDelete all trailing spaces and save file")
                    return
                registers=list(registers.split(","))
                if len(registers)==3:
                    aluInstruction(opcode,registers)
                elif len(registers)==2:
                    iInstructions(opcode,registers)
                elif len(registers)==1:
                    jInstructions(opcode,registers)
    if instructionNum>=127:
        messagebox.showwarning("Limit","Exceed 127 instructions!")
        instructionNum=0
        return
                 
    #string is displayed in text file       
    print(outputs)
    w = open("Output.txt","w")
    if w.write(outputs):
        messagebox.showinfo("Success","Assembly was successful.\nHexcode in Output.txt")

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

#opens the file dialog
def our_command():
    text_file = filedialog.askopenfilename(initialdir="C:/Users/Dev/Desktop", title="Open Text File",filetypes=(("Text Files","*.txt"),))
    text_file = open(text_file, 'r')
    stuff = text_file.read()

    my_text.insert(END,stuff)
    text_file.close()

my_menu = Menu(root)
root.config(menu=my_menu)

file_menu = Menu(my_menu)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open",command= our_command)
file_menu.add_command(label="Exit Program",command= root.quit)

save_menu = Menu(my_menu)
my_menu.add_cascade(label="Save",menu=save_menu)
save_menu.add_command(label="Save File", command= save_txt)


assemble_menu = Menu(my_menu)
my_menu.add_cascade(label="Assemble",menu=assemble_menu )
assemble_menu.add_command(label="Assemble File", command= Assemble)

#converts instructions with 3 operands into hexcode
def aluInstruction(opcode,registers):
    global instructionNum
    word=""
    registerO=[]
    #ADDC is a coagulated instruction consisting of 2 immediate value
    #moves and an add instruction
    if "ADDC" in opcode:
        if len(registers[0])==1:
                registers[0]="0"+registers[0]
        if len(registers[1])==1:
            registers[1]="0"+registers[1]
        word+=Opcode["MOVI"]+registersA["R14"]+registers[0]+"\t"
        word+=Opcode["MOVI"]+registersA["R15"]+registers[1]+"\t"
        word+=Opcode["ADD"]+registersA["R14"]+registersA["R15"]+registersA[registers[2]]+"\t"
        instructionNum+=3
        output(word)
        return
    for i in range(len(registers)):
            registerO.append(registersA[registers[i]])
    word+=Opcode[opcode]
    for i in registerO:
            word+=i    
    word+="\t"
    instructionNum+=1
    output(word)
    
#converts instructions with 2 operands into hex code
def iInstructions(opcode,registers):
    global instructionNum
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

    #to compensate for the 2 kinds of store instructions
    #one with 2 register operands and the other with a register and address operand
    elif opcode=="STORE":
        word+=Opcode[opcode]
        if "R" in registers[1]:
            word+=registersA[registers[0]]+"0"+registersA[registers[1]]+"\t"
        else:
            word+=registersA[registers[0]]+registers[1]+"\t"
    #coagulated exchange instruction       
    elif opcode=="XCHNG":
        word+=Opcode["MOVR"]+registersA["R15"]+registersA[registers[0]]+"0\t"
        word+=Opcode["MOVR"]+registersA[registers[0]]+registersA[registers[1]]+"0\t"
        word+=Opcode["MOVR"]+registersA[registers[1]]+registersA["R15"]+"0\t"
        instructionNum+=3
        output(word)
        return
    else:
        word+=Opcode[opcode]
        word+=registersA[registers[0]]
        if len(registers[1])==1:
            word+="0"
        word+=registers[1]
        for i in registerO:
            word+=i
        word+="\t"
    instructionNum+=1
    output(word)

#converts instructions with 1 operand into hexcode
def jInstructions(opcode,registers):
    global instructionNum
    word=""
    word+=Opcode[opcode]
    if len(registers[0])==1:
        word+="0"
    word+=registers[0]
    word+="\t"
    instructionNum+=1
    output(word)

#converts HALT and NOP instructions into hexcode
def cInstructions(opcode):
    global instructionNum
    word=""
    if "HALT" in opcode:
        word+="FFFF"
    else:
        word+="F000"
    word+="\t"
    instructionNum+=1
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
# def Assemble():
#     global outputs
#     global instructionNum
#     global counter
#     instructionNum=0
#     counter=1
#     outputs="v2.0 raw\n"+"F000\t"
         
#     f = open("Test.txt","r")
#     for i in f:
#         if (instructionNum<127):
#             i=i.strip()
#             if ("HALT" in i) or ("NOP" in i):
#                 cInstructions(i)
#                 continue
#             else:
#                 opcode,registers=i.split()
#                 registers=list(registers.split(","))
#                 if len(registers)==3:
#                     aluInstruction(opcode,registers)
#                 elif len(registers)==2:
#                     iInstructions(opcode,registers)
#                 elif len(registers)==1:
#                     jInstructions(opcode,registers)
         
#     if instructionNum>=127:
#         messagebox.showwarning("Limit","Exceed 127 instructions!")
#         instructionNum=0
#         return
                 
#     #string is displayed in text file       
#     print(outputs)
#     w = open("Output.txt","w")
#     if w.write(outputs):
#         messagebox.showinfo("","")
    
    

my_text = Text(root, width=40, height=10, font=("Helvetica",16))
my_text.pack(pady=20)




root.mainloop()