from tkinter import *

root = Tk()
root.title("Assembly")
#root.iconbitmap('')
root.geometry("500x450")

registersA={
        "R0":"0","R1":"1","R2":"2","R3":"3",
        "R4":"4","R5":"5","R6":"6","R7":"7",
        "R8":"8","R9":"9","R10":"A","R11":"B",
        "R12":"C","R13":"D","R14":"E","R15":"F",
    }

Opcode = {
        "ADD":'0', "SUB":'1', "MULT":'2',"DIV":'3',
        "SHL":'4', "SHR":'5',"AND":'6', "OR":'7',
        "MOVR":'8',"MOVI":'9', "LOAD":'A', "STORE":'B',
        "JMP":'C', "JMPZ":'D', "JMPN":'E'
        }
counter=1
outputs="v2.0 raw\n"+"0000\t"

def click_me():
    pass

def open_txt():
    global outputs
    text_file = open("Test.txt", "r")
    stuff = text_file.read()

    my_text.insert(END,stuff)
    text_file.close()

def save_txt():
    text_file = open("Test.txt", "w")
    text_file.write(my_text.get(1.0,END))

def aluInstruction(opcode,registers):
    word=""
    registerO=[]
    for i in range(len(registers)):
        registerO.append(registersA[registers[i]])
    word+=Opcode[opcode]
    for i in registerO:
        word+=i
    word+="\t"
    output(word)
    

def iInstructions(opcode,registers):
    word=""
    registerO=[]
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
        registerO.append(registersA[registers[0]])
        registerO.append(registers[1])
        for i in registerO:
            word+=i
        word+="\t"
    output(word)

def jInstructions(opcode,registers):
    word=""
    word+=Opcode[opcode]
    word+="0"
    word+=registers[0]
    word+="\t"
    output(word)
    

def output(word):
    global counter
    global outputs
    if  counter<8:
        outputs+=word
        counter+=1
    elif counter==8 or counter>8:
        outputs+="\n"
        counter=0
        

def Assemble():
    global outputs
    
    f = open("Test.txt","r")


    for i in f:
        opcode,registers=i.split()
        registers=list(registers.split(","))
        if len(registers)==3:
            aluInstruction(opcode,registers)
        elif len(registers)==2:
            iInstructions(opcode,registers)
        elif len(registers)==1:
            jInstructions(opcode,registers)
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