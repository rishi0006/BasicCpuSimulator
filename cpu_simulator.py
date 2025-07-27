import sys

#RAM
RAM=[0]*256
# RAM=bytearray(256)    #To have actually 256Bytes RAM

print("Size of RAM is",sys.getsizeof(RAM),"bytes")
print("Size of 1 cell in RAM is",sys.getsizeof(RAM[0]),'bytes')

#Registers
# Number of Registers depends on CPU architecture, say 8 bit CPU has 4-8 registers
registers={'R0':0,'R1':0,'R2':0,"R3":0}

ACC=0
PC=0
IR=None
MAR=None
MDR=None

Running=True

Program=["LOAD R1, 10",
         "LOAD R2, 11",
         "ADD R1, R2",  #Store addition in R1
         "STORE R1, 12",  #Store R1's value in Mem[12]
         "HLT"]

#Initialize the RAM with random values
RAM[5]=11
RAM[10]=2
RAM[11]=5

#Instruction Cycle
def fetch():
    global PC,MAR,MDR,IR
    MAR=PC
    MDR=Program[MAR]
    IR=MDR
    PC+=1
    print(f"Instruction {PC-1} Fetched")

    print("MAR <- PC")
    print(f"MDR <- Memory[{MAR}]")
    print("IR <- MDR")
    print("PC <- PC+1")

def decode():
    global IR,MDR,MAR,Running

    instruction=IR.split()  #['LOAD', 'R1,', '10']
    mcInstructions=instruction[0]

    if mcInstructions=="LOAD":
        reg=instruction[1].rstrip(',')
        addr=instruction[2]
        if addr.lstrip('#')=='#':
            #Is Value
            addr=addr.rstrip('#')
            value=int(addr)
            print("Executing Instruction \n\t",IR)

            #Do R1=10
            MDR=value
            registers[reg]=MDR

            print(f"MDR <- {value}\n{reg} <- {MDR}")
        else:
            #Is Memory Address
            print("Executing Instruction \n\t",IR)

            #Do R1=M[10]
            MAR=int(addr)
            MDR=RAM[MAR]
            registers[reg]=MDR

            print(f"MAR <- {addr}\nMDR <- M[{MAR}]\n{reg} <- {MDR}")
    
    elif mcInstructions=="STORE":
        reg=instruction[1].rstrip(',')
        addr=int(instruction[2])
        print("Executing Instruction \n\t",IR)

        #Storing value of R1(=2) into M[12]
        MAR=addr
        MDR=registers[reg]
        RAM[MAR]=MDR
        print(f"MAR <- {addr}\nMDR <- reg\nM[{MAR}] <- {MDR}")
        
    elif mcInstructions=="ADD":
        reg1= instruction[1].rstrip(',')
        reg2= instruction[2]
        print(f"[Execute] Instruction: \n\t{IR}")

        ALU_Res=registers[reg1]+registers[reg2]
        registers[reg1]=ALU_Res

        print(f"ALU <- {reg1} + {reg2}\n{reg1} <- ALU")

    elif mcInstructions=="HLT":
        print(f"[Execute] Instruction: \n\t{IR}")
        print("MicroOps: Halt the CPU")
        Running = False

def runCPU():
    global Running
    print("=== CPU Execution Start ===")
    while Running:
        fetch()
        decode()
        print("Registers", registers)
        print('-'*40)
    print("=== CPU Execution End ===")
    print(f"Final RAM[12] = {RAM[12]}")

runCPU()
