RAM = [0] * 256
REGISTERS = {'R0': 0, 'R1': 0, 'R2': 0, 'R3': 0}
PC = 0
IR = None
MAR = None
MDR = None
RUNNING = True


PROGRAM = [
    "LOAD R1, 10",  
    "LOAD R2, 11",  
    "ADD R1, R2",      
    "STORE R1, 12",   
    "HLT"              
]

RAM[10] = 7
RAM[11] = 5

def fetch():
    global PC, IR, MAR, MDR
    MAR = PC
    MDR = PROGRAM[MAR]
    IR = MDR
    print("[Instruction Fetch]")
    print("MAR ← PC")
    print(f"MDR ← Memory[{MAR}]")
    print("IR  ← MDR")
    print("PC  ← PC + 1")
    PC += 1

def decode_and_execute():
    global IR, MAR, MDR, RUNNING

    parts = IR.split()
    instr = parts[0]

    if instr == "LOAD":
        reg = parts[1].rstrip(',')
        addr = int(parts[2])
        print(f"[Execute] Instruction: {IR}")
        MAR = addr
        MDR = RAM[MAR]
        REGISTERS[reg] = MDR
        print(f"MicroOps: MAR ← {addr}, MDR ← RAM[{addr}] = {MDR}, {reg} ← MDR")

    elif instr == "STORE":
        reg = parts[1].rstrip(',')
        addr = int(parts[2])
        print(f"[Execute] Instruction: {IR}")
        MAR = addr
        MDR = REGISTERS[reg]
        RAM[MAR] = MDR
        print(f"MicroOps: MAR ← {addr}, MDR ← {reg} = {MDR}, RAM[{addr}] ← MDR")

    elif instr == "ADD":
        reg1 = parts[1].rstrip(',')
        reg2 = parts[2]
        print(f"[Execute] Instruction: {IR}")
        ALU_result = REGISTERS[reg1] + REGISTERS[reg2]
        REGISTERS[reg1] = ALU_result
        print(f"MicroOps: ALU ← {reg1} + {reg2} = {ALU_result}, {reg1} ← ALU")

    elif instr == "HLT":
        print(f"[Execute] Instruction: {IR}")
        print("MicroOps: Halt the CPU")
        RUNNING = False

def run_cpu():
    global RUNNING
    print("=== CPU Execution Start ===")
    while RUNNING:
        fetch()
        decode_and_execute()
        print(f"Registers: {REGISTERS}")
        print("-" * 40)
    print("=== CPU Execution End ===")
    print(f"Final RAM[12] = {RAM[12]}")

run_cpu()
