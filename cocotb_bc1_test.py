import cocotb
from cocotb.triggers import Timer
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge

### ANIL BUDAK - 2574812

#TRUE for printing signals
DEBUG = True

#CHANGE THE BELOW SIGNAL NAMES TO MATCH YOUR DESIGN!!!!!!!!!!!!!!!!!
def printRegisters(dut):
    dut._log.info(f"T:  {dut.controller.sc.T.value}") # T1
    dut._log.info(f"PC: {dut.PC.value}")
    dut._log.info(f"AR: {dut.AR.value}")
    dut._log.info(f"IR: {dut.IR.value}")
    dut._log.info(f"AC: {dut.AC.value}")
    dut._log.info(f"DR: {dut.DR.value}")
    dut._log.info(f"TR: {dut.data_path.TR.A.value}")
    dut._log.info(f"FGI: {dut.FGI.value}")
    dut._log.info(f"R: {dut.controller.R.value}")
    dut._log.info(f"IEN: {dut.controller.IEN.value}")
    #dut._log.info(f"D: {dut.controller.D.value}")
    #dut._log.info(f"OPSEL: {dut.data_path.OPSEL_ALU.value}")
    #dut._log.info(f"CNTRL: {dut.w_CTRL_SGNLS.value[4]}")
    #dut._log.info(f"E: {dut.data_path.e_ff.E.value}")
    #dut._log.info(f"N: {dut.controller.N.value}")
    #dut._log.info(f"Z: {dut.controller.Z.value}")
    #dut._log.info(f"OVF: {dut.controller.OVF.value}")


@cocotb.test()
async def basic_computer_test(dut):
    """Try accessing the design."""
    A = 562
    B = 3131
    dut.w_IN_ADF.value = A
    dut.FGI.value = 0

    #dut.FGI.value = 0
    #Start the clock
    await cocotb.start(Clock(dut.clk, 10, 'us').start(start_high=False))
    #Get the fallin edge to work with
    clkedge = FallingEdge(dut.clk)
    
    #Check your design for however many cycles, assert at correct clock cycles
    for cycle in range(8):
        await clkedge

        #Log values if debugging
        if DEBUG:
            printRegisters(dut)
            pass
            
        #Sımple match-case structure to test when needed
        #You should modify it according to your sample code
        match cycle:
            case 2:
                #assert dut.IR.value == 0x1234, "IR not loaded properly!"
                #print_my_computer_please(dut)
                dut.w_MWE.value = 1
                dut.w_IN_ADF.value = 12
                dut.w_W_DATA.value = B
                assert dut.w_R_DATA.value == 0, f"RES: {dut.w_R_DATA.value}"

                dut._log.info(f"Cycle count: {cycle} \n")

            case 4: # | 5 | 6 | 7 | 8 | 9
                dut.w_IN_ADF.value = 31
                dut.w_W_DATA.value = 1
                assert dut.w_R_DATA.value == B, f"RES: {dut.w_R_DATA.value}"
                dut._log.info(f"Cycle count: {cycle} \n")

            case 5:
                dut.w_MWE.value = 0
                dut.w_IN_ADF.value = 12
                #dut.w_W_DATA.value = 1
                assert dut.w_R_DATA.value == 1, f"RES: {dut.w_R_DATA.value}"
                dut._log.info(f"Cycle count: {cycle} \n")

            case 6:
                assert dut.w_R_DATA.value == B
                dut._log.info(f"Cycle count: {cycle} \n")
                pass
            case _:
                dut._log.info(f"Cycle count: {cycle} \n")
    
    dut._log.info("BC I test ended successfully!")

@cocotb.test()
async def alu_test(dut):
    dut.AC.value = 64
    dut.DR.value = -32
    dut.E = 1
    dut.OPSEL = 0 
    await Timer(10, units="ns")  # Wait for simulation to stabilize
    
    dut._log.info("************ DUT Signals ***************")
    dut._log.info(f"AC:     {dut.AC.value}")
    dut._log.info(f"DR:     {dut.DR.value}")
    #dut._log.info(f"AC+DR: {dut.AC.value + dut.DR.value}")
    dut._log.info(f"RESULT: {dut.RESULT.value}")
    dut._log.info(f"N: {dut.N.value}")
    dut._log.info(f"Z: {dut.Z.value}")
    dut._log.info(f"OVF: {dut.OVF.value}")
    dut.FGI.value = 0

    assert dut.RESULT.value == dut.AC.value + dut.DR.value 

    
    dut._log.info("BC I test ended successfully!")

@cocotb.test()
async def data_path_test(dut):
    """Try accessing the design."""
    # Initialize values
    dut.WRD.value = 0
    dut.WE_MEM.value = 0  # Disable write initially
    dut.BUS_SEL.value = 0  # Default to AR
    address = 193          # Address to write to
    value_to_write = 31    # Value to write
    dut.FGI.value = 0

    #Start the clock
    await cocotb.start(Clock(dut.clk, 10, 'us').start(start_high=False))
    #Get the fallin edge to work with
    clkedge = FallingEdge(dut.clk)
    
    await clkedge
    # Write operation
    dut._log.info("Starting Write Operation")
    dut.WRD.value = address 
    dut.BUS_SEL.value = 7  # Address into the bus
    await clkedge  # Wait for one clock cycle to latch address and data
    dut._log.info(dut.BUS.value)
    dut.T0.value = 1 
    await clkedge  # Wait for write to complete
    dut._log.info(dut.w_AR.value)
    dut.T0.value = 0
    dut.WRD.value = value_to_write
    await clkedge
    dut._log.info(dut.BUS.value)
    await clkedge
    dut.WE_MEM.value = 1
    await clkedge
    dut.WE_MEM.value = 0
    dut._log.info(dut.w_AR.value)
    await clkedge
    dut.BUS_SEL.value = 6
    dut._log.info(dut.BUS.value)
    await clkedge
    dut.BUS_SEL.value = 7

    # Assert the result
    assert dut.w_MEM.value == value_to_write, f"Read value {dut.w_MEM.value} does not match written value {value_to_write}"
    dut._log.info(f"Read-Back Successful: Address={address}, Value={dut.w_MEM.value}")
    
    
    dut._log.info("BC I test ended successfully!")

@cocotb.test()
async def controller_test(dut):
    """Try accessing the design."""
    # Initialize values
    address = 193          # Address to write to
    value_to_write = 31    # Value to write
    dut.data_path.memory.MEMORY[address].value = 31
    dut.data_path.PC.A.value = address
    dut.FGI.value = 0

    #Start the clock
    await cocotb.start(Clock(dut.clk, 10, 'us').start(start_high=False))
    #Get the fallin edge to work with
    clkedge = FallingEdge(dut.clk)
    
    dut._log.info(f"T: {dut.controller.sc.T.value}") # T0
    dut._log.info(f"PC: {dut.PC.value}")
    dut._log.info(f"AR: {dut.AR.value}")
    await clkedge
    # Write operation
    dut._log.info("Starting Clock Operation")
    dut._log.info(f"T:  {dut.controller.sc.T.value}") # T1
    dut._log.info(f"IR: {dut.IR.value}")
    dut._log.info(f"PC: {dut.PC.value}")
    dut._log.info(f"AR: {dut.AR.value}")
    dut._log.info("CYCLE: 1 --------------")
    #dut._log.info(dut.w_BUS_SEL.value)
    await clkedge  # Wait for one clock cycle to latch address and data
    dut._log.info(f"T:  {dut.controller.sc.T.value}") # T2
    dut._log.info(f"AR: {dut.AR.value}")
    dut._log.info(f"IR: {dut.IR.value}")
    dut._log.info("CYCLE: 2 --------------")
    await clkedge
    dut._log.info(f"T:  {dut.controller.sc.T.value}")
    dut._log.info(f"IR: {dut.IR.value}")
    dut._log.info(dut.controller.sc.T.value)  # T3
    dut._log.info("CYCLE: 3 --------------")
    await clkedge
    dut._log.info(f"T:  {dut.controller.sc.T.value}")
    dut._log.info(f"AR: {dut.AR.value}")
    dut._log.info("CYCLE: 4 --------------")

    # Assert the result
    assert dut.IR.value == value_to_write, f"Read value {dut.w_WRD.value} does not match written value {value_to_write}"
    dut._log.info(f"Read-Back Successful: Address={address}, Value={dut.w_WRD.value}")
    
    
    dut._log.info("BC I test ended successfully!")

@cocotb.test()
async def CLA_test(dut):
    """Try accessing the design."""
    # Initialize values
    instruction = 30720 # CLA
    address = 193          # Address to write to
    ac_value = 132         # Initial AC to be cleared by CLA 
    dut.data_path.memory.MEMORY[address].value = instruction
    dut.data_path.PC.A.value = address
    dut.data_path.AC.A.value = ac_value
    dut.FGI.value = 0

    #Start the clock
    await cocotb.start(Clock(dut.clk, 10, 'us').start(start_high=False))
    clkedge = FallingEdge(dut.clk)

    for cycle in range(8):
        await clkedge

        #Logging the values if debugging
        if DEBUG:
            printRegisters(dut)
            pass
            
        match cycle:
            case 0 | 1 | 2: ### FETCH
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.AC.value == ac_value, f"Read value {dut.AC.value} does not match the AC value {ac_value}"
            ### ENDFETCH

            case 3: ### EXECUTE CLA
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.AC.value == ac_value, f"Read value {dut.AC.value} does not match the written AC value {ac_value}"
            
            case 4: 
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.AC.value == 0, f"The AC: {dut.AC.value} is not cleared"
            ### ENDEXECUTE 

            case _:
                dut._log.info(f"Cycle count: {cycle} ----------\n")
    
    dut._log.info("BC I test ended successfully!")

@cocotb.test()
async def CLE_test(dut):
    """Try accessing the design."""
    # Initialize values
    instruction = 29696 # CLE
    address = 193          # Address to write to
    e_value = 1         # Initial E to be cleared by CLE 
    dut.data_path.memory.MEMORY[address].value = instruction
    dut.data_path.PC.A.value = address
    dut.data_path.e_ff.E.value = e_value
    dut.FGI.value = 0

    #Start the clock
    await cocotb.start(Clock(dut.clk, 10, 'us').start(start_high=False))
    clkedge = FallingEdge(dut.clk)

    for cycle in range(8):
        await clkedge

        #Logging the values if debugging
        if DEBUG:
            printRegisters(dut)
            pass
            
        match cycle:
            case 0 | 1 | 2: ### FETCH
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.data_path.e_ff.E.value == e_value, f"Read value {dut.data_path.e_ff.E.value} does not match the E value {e_value}"
            ### ENDFETCH

            case 3: ### EXECUTE CLA
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.data_path.e_ff.E.value == e_value, f"Read value {dut.data_path.e_ff.E.value} does not match the written E value {e_value}"
            
            case 4: 
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.data_path.e_ff.E.value == 0, f"The E: {dut.data_path.e_ff.E.value} is not cleared"
            ### ENDEXECUTE CLA

            case _:
                dut._log.info(f"Cycle count: {cycle} ----------\n")
    
    dut._log.info("BC I test ended successfully!")

@cocotb.test()
async def CMA_test(dut):
    """Try accessing the design."""
    # Initialize values
    instruction = 29184 # CMA
    address = 1002          # Address to write to
    ac_value = 876         # Initial AC to be complemented
    cmp_ac_value = 2**16-1-ac_value
    dut.data_path.memory.MEMORY[address].value = instruction
    dut.data_path.PC.A.value = address
    dut.data_path.AC.A.value = ac_value
    dut.FGI.value = 0

    #Start the clock
    await cocotb.start(Clock(dut.clk, 10, 'us').start(start_high=False))
    clkedge = FallingEdge(dut.clk)

    for cycle in range(8):
        await clkedge

        #Logging the values if debugging
        if DEBUG:
            printRegisters(dut)
            pass
            
        match cycle:
            case 0 | 1 | 2: ### FETCH
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.data_path.AC.A.value == ac_value, f"Read value {dut.data_path.AC.A.value} does not match the written AC value {ac_value}"
            ### ENDFETCH

            case 3: ### EXECUTE CMA
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.data_path.AC.A.value == ac_value, f"Read value {dut.data_path.AC.A.value} does not match the written AC value {ac_value}"
            
            case 4: 
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.data_path.AC.A.value == cmp_ac_value, f"The AC: {dut.data_path.AC.A.value} is not complemented to {cmp_ac_value}"
            ### ENDEXECUTE

            case _:
                dut._log.info(f"Cycle count: {cycle} ----------\n")
    
    dut._log.info("BC I test ended successfully!")

@cocotb.test()
async def CME_test(dut):
    """Try accessing the design."""
    # Initialize values
    instruction = 28928 # CME
    address = 1876          # Address to write to
    e_value = 0         # Initial e to be complemented
    cmp_e_value = 1-e_value
    dut.data_path.memory.MEMORY[address].value = instruction
    dut.data_path.memory.MEMORY[address+1].value = instruction # 2 CME Instructions
    dut.data_path.PC.A.value = address
    dut.data_path.e_ff.E.value = e_value
    dut.FGI.value = 0

    #Start the clock
    await cocotb.start(Clock(dut.clk, 10, 'us').start(start_high=False))
    clkedge = FallingEdge(dut.clk)

    for cycle in range(12):
        await clkedge

        #Logging the values if debugging
        if DEBUG:
            printRegisters(dut)
            pass
            
        match cycle:
            case 0 | 1 | 2: ### FETCH
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.data_path.e_ff.E.value == e_value, f"Read value {dut.data_path.e_ff.E.value} does not match the written E value {e_value}"
            ### ENDFETCH

            case 3: ### EXECUTE CME
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.data_path.e_ff.E.value == e_value, f"Read value {dut.data_path.e_ff.E.value} does not match the written E value {e_value}" 
            ### ENDEXECUTE
    
            case 4 | 5 | 6: ### FETCH
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.data_path.e_ff.E.value == cmp_e_value, f"Read value {dut.data_path.e_ff.E.value} does not match the written E value {cmp_e_value}"
            ### ENDFETCH

            case 7: ### EXECUTE CME #2
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.data_path.e_ff.E.value == cmp_e_value, f"Read value {dut.data_path.e_ff.E.value} does not match the written E value {cmp_e_value}"
            
            case 8: 
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.data_path.e_ff.E.value == e_value, f"The E: {dut.data_path.e_ff.E.value} is not complemented to {e_value}"
            ### ENDEXECUTE CLA

            case _:
                dut._log.info(f"Cycle count: {cycle} ----------\n")
    
    dut._log.info("BC I test ended successfully!")

@cocotb.test()
async def CIR_test(dut):
    """Try accessing the design."""
    # Initialize values
    instruction = 28800 # CIR
    address = 100          # Address to write to
    ac_value = 1723         # Initial AC
    e_value = 1
    dut.data_path.memory.MEMORY[address].value = instruction
    dut.data_path.memory.MEMORY[address+1].value = instruction # 2 CIR Instructions
    dut.data_path.PC.A.value = address
    dut.data_path.AC.A.value = ac_value
    dut.data_path.e_ff.E.value = e_value # Initial E value 
    flag = 1
    dut.FGI.value = 0
    

    #Start the clock
    await cocotb.start(Clock(dut.clk, 10, 'us').start(start_high=False))
    clkedge = FallingEdge(dut.clk)

    for cycle in range(12):
        await clkedge

        #Logging the values if debugging
        if DEBUG:
            printRegisters(dut)
            pass
            
        match cycle:
            case 0 | 1 | 2: ### FETCH
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.AC.value == ac_value, f"Read value {dut.AC.value} does not match the written AC value {ac_value}"
                assert dut.data_path.e_ff.E.value == e_value, f"Cycle {cycle}: E mismatch. Expected {e_value}, got {dut.data_path.e_ff.E.value}"

            ### ENDFETCH

            case 3: ### EXECUTE CIR
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.AC.value == ac_value, f"Read value {dut.AC.value} does not match the written cir AC value {ac_value}" 
                assert dut.data_path.e_ff.E.value == e_value, f"Cycle {cycle}: E mismatch. Expected {e_value}, got {dut.data_path.e_ff.E.value}"
            ### ENDEXECUTE
            
            case 4 | 5 | 6: ### FETCH
                if (flag):
                    lsb = ac_value & 1  # Extract LSB of AC
                    e_value = lsb  # Update E to LSB             
                    ac_value = (ac_value >> 1) | (e_value << (dut.AC.value.n_bits - 1))  # Right shift AC with E as MSB
                    flag = 0

                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.AC.value == ac_value, f"Cycle {cycle}: AC mismatch. Expected {ac_value}, got {dut.AC.value}"
                assert dut.data_path.e_ff.E.value == e_value, f"Cycle {cycle}: E mismatch. Expected {e_value}, got {dut.data_path.e_ff.E.value}"
            ### ENDFETCH

            case 7: ### EXECUTE CIR #2
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.AC.value == ac_value, f"Cycle {cycle}: AC mismatch. Expected {ac_value}, got {dut.AC.value}"
                assert dut.data_path.e_ff.E.value == e_value, f"Cycle {cycle}: E mismatch. Expected {e_value}, got {dut.data_path.e_ff.E.value}"
            
            case 8:
                lsb = ac_value & 1  # Extract LSB of AC
                e_value = lsb  # Update E to LSB
                ac_value = (ac_value >> 1) | (e_value << (dut.AC.value.n_bits - 1))  # Right shift AC with E as MSB

                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.AC.value == ac_value, f"Cycle {cycle}: AC mismatch. Expected {ac_value}, got {dut.AC.value}"
                assert dut.data_path.e_ff.E.value == e_value, f"Cycle {cycle}: E mismatch. Expected {e_value}, got {dut.data_path.e_ff.E.value}"

            ### ENDEXECUTE CLA

            case _:
                dut._log.info(f"Cycle count: {cycle} ----------\n")
    
    dut._log.info("BC I test ended successfully!")

@cocotb.test()
async def CIL_test(dut):
    """Test the Circular Left (CIL) operation."""
    # Initialize values
    instruction = 28736  # CIL instruction encoding (modify to your design's encoding for CIL)
    address = 100  # Memory address to start
    ac_value = 3965  # Initial AC value
    e_value = 1  # Initial E value
    flag = 1

    dut.data_path.memory.MEMORY[address].value = instruction  # CIL instruction
    dut.data_path.memory.MEMORY[address + 1].value = instruction  # Another CIL instruction
    dut.data_path.PC.A.value = address  # Set PC to instruction start address
    dut.data_path.AC.A.value = ac_value  # Set initial AC value
    dut.data_path.e_ff.E.value = e_value  # Set initial E value
    dut.FGI.value = 0

    # Start the clock
    await cocotb.start(Clock(dut.clk, 10, 'us').start(start_high=False))
    clkedge = FallingEdge(dut.clk)

    # Perform 12 cycles of test
    for cycle in range(12):
        await clkedge  # Wait for the next clock cycle

        # Debugging output
        if DEBUG:
            dut._log.info(f"Cycle: {cycle}, PC: {dut.PC.value}, AC: {dut.AC.value}, E: {dut.data_path.e_ff.E.value}")

        # Execution logic per cycle
        match cycle:
            case 0 | 1 | 2:  # FETCH (Instruction fetch cycles)
                dut._log.info(f"Cycle count: {cycle} ----------")
                assert dut.AC.value == ac_value, f"Cycle {cycle}: AC mismatch. Expected {ac_value}, got {dut.AC.value}"
                assert dut.data_path.e_ff.E.value == e_value, f"Cycle {cycle}: E mismatch. Expected {e_value}, got {dut.data_path.e_ff.E.value}"

            case 3:  # EXECUTE CIL (First instruction)
                dut._log.info(f"Cycle count: {cycle} ----------")
                assert dut.AC.value == ac_value, f"Cycle {cycle}: AC mismatch. Expected {ac_value}, got {dut.AC.value}"
                assert dut.data_path.e_ff.E.value == e_value, f"Cycle {cycle}: E mismatch. Expected {e_value}, got {dut.data_path.e_ff.E.value}"

            case 4 | 5 | 6:  # FETCH (Second instruction fetch cycles)
                if (flag):
                    msb = (ac_value >> (dut.AC.value.n_bits - 1)) & 1  # Extract MSB of AC
                    ac_value = ((ac_value << 1) | e_value) & ((1 << dut.AC.value.n_bits) - 1)  # Left shift AC with E as LSB
                    e_value = msb  # Update E to MSB
                    flag = 0
                dut._log.info(f"Cycle count: {cycle} ----------")
                assert dut.AC.value == ac_value, f"Cycle {cycle}: AC mismatch. Expected {ac_value}, got {dut.AC.value}"
                assert dut.data_path.e_ff.E.value == e_value, f"Cycle {cycle}: E mismatch. Expected {e_value}, got {dut.data_path.e_ff.E.value}"

            case 7:  # EXECUTE CIL (Second instruction)
                dut._log.info(f"Cycle count: {cycle} ----------")
                assert dut.AC.value == ac_value, f"Cycle {cycle}: AC mismatch. Expected {ac_value}, got {dut.AC.value}"
                assert dut.data_path.e_ff.E.value == e_value, f"Cycle {cycle}: E mismatch. Expected {e_value}, got {dut.data_path.e_ff.E.value}"

            case 8:  # Post-Second CIL Execution
                msb = (ac_value >> (dut.AC.value.n_bits - 1)) & 1  # Extract MSB of AC
                ac_value = ((ac_value << 1) | e_value) & ((1 << dut.AC.value.n_bits) - 1)  # Left shift AC with E as LSB
                e_value = msb  # Update E to MSB

                dut._log.info(f"Cycle count: {cycle} ----------")
                assert dut.AC.value == ac_value, f"Cycle {cycle}: AC mismatch. Expected {ac_value}, got {dut.AC.value}"
                assert dut.data_path.e_ff.E.value == e_value, f"Cycle {cycle}: E mismatch. Expected {e_value}, got {dut.data_path.e_ff.E.value}"

            case _:  # Default for unused cycles
                dut._log.info(f"Cycle count: {cycle}: No specific operation.")
    dut._log.info("BC I test ended successfully!")

@cocotb.test()
async def INC_test(dut):
    """Try accessing the design."""
    # Initialize values
    instruction = 28704 # CMA
    address = 1002          # Address to write to
    ac_value = 876         # Initial AC to be complemented
    dut.data_path.memory.MEMORY[address].value = instruction
    dut.data_path.PC.A.value = address
    dut.data_path.AC.A.value = ac_value
    dut.FGI.value = 0

    #Start the clock
    await cocotb.start(Clock(dut.clk, 10, 'us').start(start_high=False))
    clkedge = FallingEdge(dut.clk)

    for cycle in range(8):
        await clkedge

        #Logging the values if debugging
        if DEBUG:
            printRegisters(dut)
            
        match cycle:
            case 0 | 1 | 2: ### FETCH
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.data_path.AC.A.value == ac_value, f"Read value {dut.data_path.AC.A.value} does not match the written AC value {ac_value}"
            ### ENDFETCH

            case 3: ### EXECUTE CMA
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.data_path.AC.A.value == ac_value, f"Read value {dut.data_path.AC.A.value} does not match the written AC value {ac_value}"
            
            case 4: 
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.data_path.AC.A.value == ac_value+1, f"The AC: {dut.data_path.AC.A.value} is not incremented to {ac_value+1}"
            ### ENDEXECUTE

            case _:
                dut._log.info(f"Cycle count: {cycle} ----------\n")
    
    dut._log.info("BC I test ended successfully!")

@cocotb.test()
async def SPA_test(dut):
    """Try accessing the design."""
    # Initialize values
    instruction = 28688 # SPA
    address = 1002          # Address to write to
    ac_value = 2**15-1         # Initial AC to be complemented
    dut.data_path.memory.MEMORY[address].value = instruction
    dut.data_path.PC.A.value = address
    dut.data_path.AC.A.value = ac_value
    dut.FGI.value = 0

    #Start the clock
    await cocotb.start(Clock(dut.clk, 10, 'us').start(start_high=False))
    clkedge = FallingEdge(dut.clk)

    for cycle in range(8):
        await clkedge

        #Logging the values if debugging
        if DEBUG:
            printRegisters(dut)
            
        match cycle:
            case 0 | 1 | 2: ### FETCH
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                #assert dut.data_path.AC.A.value == ac_value, f"Read value {dut.data_path.AC.A.value} does not match the written AC value {ac_value}"
            ### ENDFETCH

            case 3: ### EXECUTE SPA
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.PC.value == address+1, f"Read value {dut.PC.value} does not match the PC+1 value {address+1}"
            
            case 4: 
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.PC.value == address+2, f"Read value {dut.PC.value} does not match the PC+2 value {address+2}"
            ### ENDEXECUTE

            case _:
                dut._log.info(f"Cycle count: {cycle} ----------\n")
    
    dut._log.info("BC I test ended successfully!")

@cocotb.test()
async def SNA_test(dut):
    """Try accessing the design."""
    # Initialize values
    instruction = 28680 # SPA
    address = 1002          # Address to write to
    ac_value = 2**15         # Initial AC
    dut.data_path.memory.MEMORY[address].value = instruction
    dut.data_path.PC.A.value = address
    dut.data_path.AC.A.value = ac_value
    dut.FGI.value = 0

    #Start the clock
    await cocotb.start(Clock(dut.clk, 10, 'us').start(start_high=False))
    clkedge = FallingEdge(dut.clk)

    for cycle in range(8):
        await clkedge

        #Logging the values if debugging
        if DEBUG:
            printRegisters(dut)
            
        match cycle:
            case 0 | 1 | 2: ### FETCH
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                #assert dut.data_path.AC.A.value == ac_value, f"Read value {dut.data_path.AC.A.value} does not match the written AC value {ac_value}"
            ### ENDFETCH

            case 3: ### EXECUTE SNA
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.PC.value == address+1, f"Read value {dut.PC.value} does not match the PC+1 value {address+1}"
            
            case 4: 
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.PC.value == address+2, f"Read value {dut.PC.value} does not match the PC+2 value {address+2}"
            ### ENDEXECUTE

            case _:
                dut._log.info(f"Cycle count: {cycle} ----------\n")
    
    dut._log.info("BC I test ended successfully!")

@cocotb.test()
async def SZA_test(dut):
    """Try accessing the design."""
    # Initialize values
    instruction = 28676 # SPA
    address = 1002          # Address to write to
    ac_value = 0         # Initial AC
    dut.data_path.memory.MEMORY[address].value = instruction
    dut.data_path.PC.A.value = address
    dut.data_path.AC.A.value = ac_value
    dut.FGI.value = 0

    #Start the clock
    await cocotb.start(Clock(dut.clk, 10, 'us').start(start_high=False))
    clkedge = FallingEdge(dut.clk)

    for cycle in range(8):
        await clkedge

        #Logging the values if debugging
        if DEBUG:
            printRegisters(dut)
            
        match cycle:
            case 0 | 1 | 2: ### FETCH
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                #assert dut.data_path.AC.A.value == ac_value, f"Read value {dut.data_path.AC.A.value} does not match the written AC value {ac_value}"
            ### ENDFETCH

            case 3: ### EXECUTE SNA
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.PC.value == address+1, f"Read value {dut.PC.value} does not match the PC+1 value {address+1}"
            
            case 4: 
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.PC.value == address+2, f"Read value {dut.PC.value} does not match the PC+2 value {address+2}"
            ### ENDEXECUTE

            case _:
                dut._log.info(f"Cycle count: {cycle} ----------\n")
    
    dut._log.info("BC I test ended successfully!")

@cocotb.test()
async def SZE_test(dut):
    """Try accessing the design."""
    # Initialize values
    instruction = 28674 # SZE
    address = 1002          # Address to write to
    e_value = 0         # Initial E
    dut.data_path.memory.MEMORY[address].value = instruction
    dut.data_path.PC.A.value = address
    dut.data_path.e_ff.E.value = e_value
    dut.FGI.value = 0

    #Start the clock
    await cocotb.start(Clock(dut.clk, 10, 'us').start(start_high=False))
    clkedge = FallingEdge(dut.clk)

    for cycle in range(8):
        await clkedge

        #Logging the values if debugging
        if DEBUG:
            printRegisters(dut)
            
        match cycle:
            case 0 | 1 | 2: ### FETCH
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                #assert dut.data_path.AC.A.value == ac_value, f"Read value {dut.data_path.AC.A.value} does not match the written AC value {ac_value}"
            ### ENDFETCH

            case 3: ### EXECUTE SNA
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.PC.value == address+1, f"Read value {dut.PC.value} does not match the PC+1 value {address+1}"
            
            case 4: 
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.PC.value == address+2, f"Read value {dut.PC.value} does not match the PC+2 value {address+2}"
            ### ENDEXECUTE

            case _:
                dut._log.info(f"Cycle count: {cycle} ----------\n")
    
    dut._log.info("BC I test ended successfully!")

@cocotb.test()
async def HLT_test(dut):
    """Try accessing the design."""
    # Initialize values
    instruction = 28673 # SZE
    address = 1002          # Address to write to
    dut.data_path.memory.MEMORY[address].value = instruction
    dut.data_path.PC.A.value = address
    dut.FGI.value = 0

    #Start the clock
    await cocotb.start(Clock(dut.clk, 10, 'us').start(start_high=False))
    clkedge = FallingEdge(dut.clk)

    for cycle in range(8):
        await clkedge

        #Logging the values if debugging
        if DEBUG:
            printRegisters(dut)
            
        match cycle:
            case 0 | 1 | 2: ### FETCH
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                #assert dut.data_path.AC.A.value == ac_value, f"Read value {dut.data_path.AC.A.value} does not match the written AC value {ac_value}"
            ### ENDFETCH

            case 3: ### EXECUTE HLT
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                #assert dut.PC.value == address+1, f"Read value {dut.PC.value} does not match the value {address+1}"
            
            case 4 | 5 | 6 | 7: 
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.controller.T.value == 2**3, f"Read value {dut.controller.T.value} does not match the T = T3 value {2}"
            ### ENDEXECUTE

            case _:
                dut._log.info(f"Cycle count: {cycle} ----------\n")
    
    dut._log.info("BC I test ended successfully!")

@cocotb.test()
async def AND_test(dut):
    """Try accessing the design."""
    # --- Test Setup ---
    instruction_direct = 0b0000000000000100  # AND with direct addressing mode
    instruction_indirect = 0b1000000000000100  # AND with indirect addressing mode
    target_address = 4  # Memory address to perform AND
    memory_value = 0b1010101010101010  # Value in memory to AND with
    memory_value_2 = 0b1110100011101011
    ac_initial_value = 0b1100110011001100  # Initial AC value
    expected_result_direct = ac_initial_value & memory_value
    expected_result_indirect = expected_result_direct & memory_value_2

    # Direct addressing mode setup
    dut.FGI.value = 0
    dut.data_path.memory.MEMORY[target_address].value = memory_value  # Set memory value
    dut.data_path.memory.MEMORY[1002].value = instruction_direct  # Load instruction in memory
    dut.data_path.memory.MEMORY[1003].value = instruction_indirect  # Load instruction in memory
    dut.data_path.memory.MEMORY[2730].value = memory_value_2  # Load instruction in memory
    dut.data_path.AC.A.value = ac_initial_value  # Initialize AC
    dut.data_path.PC.A.value = 1002  # Set PC to instruction address

    #Start the clock
    await cocotb.start(Clock(dut.clk, 10, 'us').start(start_high=False))
    clkedge = FallingEdge(dut.clk)

    for cycle in range(14):
        await clkedge

        #Logging the values if debugging
        if DEBUG:
            printRegisters(dut)
            
        match cycle:
            case 0 | 1 | 2: ### FETCH
                dut._log.info(f"Cycle count: {cycle} ----------\n")
            ### ENDFETCH

            case 4: ### EXECUTE AND
                dut._log.info(f"Cycle count: {cycle} ----------\n")
            
            case 5: 
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.DR.value == memory_value, f"Read value {dut.DR.value} does not match the expected value {memory_value}"
            ### ENDEXECUTE #1
            case 6 | 7 | 8:  ### FETCH #2
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.AC.value == expected_result_direct, f"Read value {dut.AC.value} does not match the expected value {expected_result_direct}"
            ### ENDFETCH #2

            case 9: ### INDIRECT
                dut._log.info(f"Cycle count: {cycle} ----------\n")            
            case 10: ### EXECUTE AND #2
                dut._log.info(f"Cycle count: {cycle} ----------\n")
            case 11:
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.DR.value == memory_value_2, f"Read value {dut.DR.value} does not match the expected value {memory_value_2}"
            case 12:
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.AC.value == expected_result_indirect, f"Read value {dut.AC.value} does not match the expected value {expected_result_indirect}"
            ### ENDEXECUTE #2

            case _:
                dut._log.info(f"Cycle count: {cycle} ----------\n")
    
    dut._log.info("BC I test ended successfully!")

@cocotb.test()
async def ADD_test(dut):
    """Try accessing the design."""
    # --- Test Setup ---
    instruction_direct = 0b0001000000000100  # ADD with direct addressing mode
    instruction_indirect = 0b1001000000000100  # ADD with indirect addressing mode
    target_address = 4  # Memory address to perform ADD
    memory_value = 0b0010101010101010  # Value in memory to ADD with 
    memory_value_2 = 0b1110100011101011
    ac_initial_value = 0b1100110011001100  # Initial AC value
    expected_result_direct = ac_initial_value + memory_value
    expected_result_indirect = expected_result_direct + memory_value_2
    e_value = 1

    # Direct addressing mode setup
    dut.data_path.memory.MEMORY[target_address].value = memory_value  # Set memory value
    dut.data_path.memory.MEMORY[1002].value = instruction_direct  # Load instruction in memory
    dut.data_path.memory.MEMORY[1003].value = instruction_indirect  # Load instruction in memory
    dut.data_path.memory.MEMORY[2730].value = memory_value_2  # Load instruction in memory
    dut.data_path.AC.A.value = ac_initial_value  # Initialize AC
    dut.data_path.PC.A.value = 1002  # Set PC to instruction address
    dut.data_path.e_ff.E.value = e_value
    dut.FGI.value = 0

    #Start the clock
    await cocotb.start(Clock(dut.clk, 10, 'us').start(start_high=False))
    clkedge = FallingEdge(dut.clk)

    for cycle in range(14):
        await clkedge

        #Logging the values if debugging
        if DEBUG:
            printRegisters(dut)
            
        match cycle:
            case 0 | 1 | 2: ### FETCH
                dut._log.info(f"Cycle count: {cycle} ----------\n")
            ### ENDFETCH

            case 4: ### EXECUTE ADD
                dut._log.info(f"Cycle count: {cycle} ----------\n")
            
            case 5: 
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                ovf = dut.data_path.OVF.value
                assert dut.DR.value == memory_value, f"Read value {dut.DR.value} does not match the expected value {memory_value}"
            ### ENDEXECUTE #1
            case 6 | 7 | 8:  ### FETCH #2
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                if (dut.data_path.e_ff.E.value == 1): # If there is carry out
                    expected_result_indirect = expected_result_indirect & 0b01111111111111111 # This eliminates the python's result of the python calculation 17th bit to match AC size of 16 bits
                assert dut.AC.value == expected_result_direct, f"Read value {dut.AC.value} does not match the expected value {expected_result_direct}, check if Overflow occurs: {ovf}"
            ### ENDFETCH #2

            case 9: ### INDIRECT
                dut._log.info(f"Cycle count: {cycle} ----------\n")            
            case 10: ### EXECUTE ADD #2
                dut._log.info(f"Cycle count: {cycle} ----------\n")
            case 11:
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.DR.value == memory_value_2, f"Read value {dut.DR.value} does not match the expected value {memory_value_2}"
            case 12:
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                ovf = dut.data_path.OVF.value
                if (dut.data_path.e_ff.E.value == 1): # If there is carry out
                    expected_result_indirect = expected_result_indirect & 0b01111111111111111 # This eliminates the python's result of the python calculation 17th bit to match AC size of 16 bits
                assert dut.AC.value  == expected_result_indirect, f"Read value {dut.AC.value} does not match the expected value {expected_result_indirect}, check if Overflow occurs: {ovf}"
            ### ENDEXECUTE #2

            case _:
                dut._log.info(f"Cycle count: {cycle} ----------\n")
    
    dut._log.info("BC I test ended successfully!")

@cocotb.test()
async def LDA_test(dut):
    """Try accessing the design."""
    # --- Test Setup ---
    instruction_direct = 0b0010000000000110  # LDA with direct addressing mode
    instruction_indirect = 0b1010000000000110  # LDA with indirect addressing mode
    target_address = 6  # Memory address to perform ADD
    memory_value = 0b0010101010101010  # Value in memory to ADD with 
    memory_value_2 = 0b1110100011101011
    expected_result_direct = memory_value
    expected_result_indirect = memory_value_2

    # Direct addressing mode setup
    dut.data_path.memory.MEMORY[target_address].value = memory_value  # Set memory value
    dut.data_path.memory.MEMORY[1002].value = instruction_direct  # Load instruction in memory
    dut.data_path.memory.MEMORY[1003].value = instruction_indirect  # Load instruction in memory
    dut.data_path.memory.MEMORY[2730].value = memory_value_2  # Load instruction in memory
    dut.data_path.PC.A.value = 1002  # Set PC to instruction address
    dut.FGI.value = 0

    #Start the clock
    await cocotb.start(Clock(dut.clk, 10, 'us').start(start_high=False))
    clkedge = FallingEdge(dut.clk)

    for cycle in range(14):
        await clkedge

        #Logging the values if debugging
        if DEBUG:
            printRegisters(dut)
            
        match cycle:
            case 0 | 1 | 2: ### FETCH
                dut._log.info(f"Cycle count: {cycle} ----------\n")
            ### ENDFETCH

            case 4: ### EXECUTE LDA
                dut._log.info(f"Cycle count: {cycle} ----------\n")
            
            case 5: 
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.DR.value == memory_value, f"Read value {dut.DR.value} does not match the expected value {memory_value}"
            ### ENDEXECUTE #1
            case 6 | 7 | 8:  ### FETCH #2
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.AC.value == expected_result_direct, f"Read value {dut.AC.value} does not match the expected value {expected_result_direct}"
            ### ENDFETCH #2

            case 9: ### INDIRECT
                dut._log.info(f"Cycle count: {cycle} ----------\n")            
            case 10: ### EXECUTE LDA #2
                dut._log.info(f"Cycle count: {cycle} ----------\n")
            case 11:
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.DR.value == memory_value_2, f"Read value {dut.DR.value} does not match the expected value {memory_value_2}"
            case 12:
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.AC.value  == expected_result_indirect, f"Read value {dut.AC.value} does not match the expected value {expected_result_indirect}"
            ### ENDEXECUTE #2

            case _:
                dut._log.info(f"Cycle count: {cycle} ----------\n")
    
    dut._log.info("BC I test ended successfully!")

@cocotb.test()
async def STA_test(dut):
    """Try accessing the design."""
    # --- Test Setup ---
    instruction_indirect = 0b1011000000000110  # STA with indirect addressing mode
    target_address = 6  # Memory address to perform STA
    memory_value = 0b0010101010101010  # Value in memory to STA with 
    memory_value_2 = 0b1110100011101011
    ac_value = 0b1011101011100010

    # Direct addressing mode setup
    dut.data_path.memory.MEMORY[target_address].value = memory_value  # Set memory value
    dut.data_path.memory.MEMORY[1003].value = instruction_indirect  # Load instruction in memory
    dut.data_path.memory.MEMORY[2730].value = memory_value_2  # Load instruction in memory
    dut.data_path.AC.A.value = ac_value  # Set PC to instruction address
    dut.data_path.PC.A.value = 1003  # Set PC to instruction address
    dut.FGI.value = 0

    #Start the clock
    await cocotb.start(Clock(dut.clk, 10, 'us').start(start_high=False))
    clkedge = FallingEdge(dut.clk)

    for cycle in range(8):
        await clkedge

        #Logging the values if debugging
        if DEBUG:
            printRegisters(dut)
            
        match cycle:
            case 0 | 1 | 2: ### FETCH
                dut._log.info(f"Cycle count: {cycle} ----------\n")
            ### ENDFETCH

            case 4: ### EXECUTE STA
                dut._log.info(f"Cycle count: {cycle} ----------\n")
            
            case 5: 
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.data_path.memory.MEMORY.value[2730] == ac_value, f"Read value {dut.data_path.memory.MEMORY.value[2730]} does not match the expected value {ac_value}"
            ### ENDEXECUTE #1

            case _:
                dut._log.info(f"Cycle count: {cycle} ----------\n")
    
    dut._log.info("BC I test ended successfully!")

@cocotb.test()
async def BUN_test(dut):
    """Try accessing the design."""
    # --- Test Setup ---
    instruction_indirect = 0b1100000000000110  # BUN with indirect addressing mode
    target_address = 6  # Memory address to perform BUN
    memory_value = 0b0010101010101010  # Value in memory to BUN with 
    expected_pc = 0b101010101010

    # Direct addressing mode setup
    dut.data_path.memory.MEMORY[target_address].value = memory_value  # Set memory value
    dut.data_path.memory.MEMORY[1003].value = instruction_indirect  # Load instruction in memory
    dut.data_path.PC.A.value = 1003  # Set PC to instruction address
    dut.FGI.value = 0

    #Start the clock
    await cocotb.start(Clock(dut.clk, 10, 'us').start(start_high=False))
    clkedge = FallingEdge(dut.clk)

    for cycle in range(8):
        await clkedge

        #Logging the values if debugging
        if DEBUG:
            printRegisters(dut)
            
        match cycle:
            case 0 | 1 | 2: ### FETCH
                dut._log.info(f"Cycle count: {cycle} ----------\n")
            ### ENDFETCH

            case 4: ### EXECUTE STA
                dut._log.info(f"Cycle count: {cycle} ----------\n")
            
            case 5: 
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.PC.value == expected_pc, f"Read value {dut.PC.value} does not match the expected value {expected_pc}"
            ### ENDEXECUTE #1

            case _:
                dut._log.info(f"Cycle count: {cycle} ----------\n")
    
    dut._log.info("BC I test ended successfully!")

@cocotb.test()
async def BSA_test(dut):
    """Try accessing the design."""
    # --- Test Setup ---
    instruction_indirect = 0b1101000000000110  # BSA with indirect addressing mode
    target_address = 6  # Memory address to perform BSA
    memory_value = 0b0010101010101010  # Value in memory to BSA with 
    pc = 0b001101010011
    effective_address = 0b101010101010

    # Direct addressing mode setup
    dut.data_path.memory.MEMORY[target_address].value = memory_value  # Set memory value
    dut.data_path.memory.MEMORY[pc].value = instruction_indirect  # Load instruction in memory
    dut.data_path.PC.A.value = pc  # Set PC to instruction address
    dut.FGI.value = 0

    #Start the clock
    await cocotb.start(Clock(dut.clk, 10, 'us').start(start_high=False))
    clkedge = FallingEdge(dut.clk)

    for cycle in range(9):
        await clkedge

        #Logging the values if debugging
        if DEBUG:
            printRegisters(dut)
            
        match cycle:
            case 0 | 1 | 2: ### FETCH
                dut._log.info(f"Cycle count: {cycle} ----------\n")
            ### ENDFETCH

            case 4: ### EXECUTE BSA
                dut._log.info(f"Cycle count: {cycle} ----------\n")
            
            case 5: 
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.data_path.memory.MEMORY.value[effective_address] == pc+1, f"Read value {dut.data_path.memory.MEMORY.value[effective_address]} does not match the expected value {pc+1}"
                assert dut.AR.value == effective_address + 1
            
            case 6:
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.PC.value == effective_address + 1, f"Read value {dut.PC.value} does not match the expected value {effective_address + 1}"              
            ### ENDEXECUTE #1
            case _:
                dut._log.info(f"Cycle count: {cycle} ----------\n")
    
    dut._log.info("BC I test ended successfully!")

@cocotb.test()
async def ISZ_test(dut):
    """Try accessing the design."""
    # --- Test Setup ---
    instruction_indirect = 0b1110000000000110  # ISZ with indirect addressing mode
    target_address = 6  # Memory address to perform ISZ
    memory_value = 0b0010101010101010  # Value in memory to ISZ with 
    memory_value_2 = 0b1111111111111111
    pc = 0b001101010011
    effective_address = 0b101010101010

    # Direct addressing mode setup
    dut.data_path.memory.MEMORY[target_address].value = memory_value  # Set memory value
    dut.data_path.memory.MEMORY[effective_address].value = memory_value_2  # Set memory value
    dut.data_path.memory.MEMORY[pc].value = instruction_indirect  # Load instruction in memory
    dut.data_path.PC.A.value = pc  # Set PC to instruction address
    dut.FGI.value = 0

    #Start the clock
    await cocotb.start(Clock(dut.clk, 10, 'us').start(start_high=False))
    clkedge = FallingEdge(dut.clk)

    for cycle in range(9):
        await clkedge

        #Logging the values if debugging
        if DEBUG:
            printRegisters(dut)
            
        match cycle:
            case 0 | 1 | 2: ### FETCH
                dut._log.info(f"Cycle count: {cycle} ----------\n")
            ### ENDFETCH

            case 4: ### EXECUTE ISZ
                dut._log.info(f"Cycle count: {cycle} ----------\n")
            
            case 5: 
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                prev_dr_value = dut.DR.value
                assert dut.DR.value == dut.data_path.memory.MEMORY.value[effective_address], f"Read value {dut.DR.value} does not match the expected value {dut.data_path.memory.MEMORY.value[effective_address]}"
            
            case 6:
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                first_sixteen_bits_of_dr_value = (prev_dr_value + 1) & 0b01111111111111111
                assert dut.DR.value == first_sixteen_bits_of_dr_value, f"Read value {dut.DR.value} does not match the expected value {first_sixteen_bits_of_dr_value}"      

            case 7:
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.data_path.memory.MEMORY.value[effective_address] == dut.DR.value, f"Read value {dut.data_path.memory.MEMORY.value[effective_address]} does not match the expected value {dut.DR.value}"
                if (dut.DR.value == 0): pc = pc + 1
                assert dut.PC.value == pc + 1, f"Read value {dut.PC.value} does not match the expected value {pc + 1}"                    
            ### ENDEXECUTE #1
            case _:
                dut._log.info(f"Cycle count: {cycle} ----------\n")
    
    dut._log.info("BC I test ended successfully!")

@cocotb.test()
async def R_test(dut):
    """Try accessing the design."""
    # --- Test Setup ---
    instruction_direct = 0b0010000000000110  # LDA with direct addressing mode
    instruction_indirect = 0b1010000000000110  # LDA with indirect addressing mode
    target_address = 6  # Memory address to perform ADD
    memory_value = 0b0010101010101010  # Value in memory to ADD with 
    memory_value_2 = 0b1110100011101011
    expected_result_direct = memory_value
    bun_0 = 0xC000

    interrupt_instruction = 0b0000000000011111

    # Direct addressing mode setup
    dut.data_path.memory.MEMORY[target_address].value = memory_value  # Set memory value
    dut.data_path.memory.MEMORY[1].value =  interrupt_instruction
    dut.data_path.memory.MEMORY[2].value =  bun_0
    dut.data_path.memory.MEMORY[interrupt_instruction].value = 0b0101010101010101
    dut.data_path.memory.MEMORY[1002].value = instruction_direct  # Load instruction in memory
    dut.data_path.memory.MEMORY[1003].value = instruction_indirect  # Load instruction in memory
    dut.data_path.memory.MEMORY[2730].value = memory_value_2  # Load instruction in memory
    dut.data_path.PC.A.value = 1002  # Set PC to instruction address
    dut.data_path.AC.A.value = 0b0011001100110110
    dut.FGI.value = 0

    #Start the clock
    await cocotb.start(Clock(dut.clk, 10, 'us').start(start_high=False))
    clkedge = FallingEdge(dut.clk)

    for cycle in range(24):
        await clkedge

        #Logging the values if debugging
        if DEBUG:
            printRegisters(dut)
            
        match cycle:
            case 0 | 1 | 2: ### FETCH
                if cycle == 1: dut.FGI.value = 1
                dut._log.info(f"Cycle count: {cycle} ----------\n")
            ### ENDFETCH

            case 4: ### EXECUTE LDA
                dut._log.info(f"Cycle count: {cycle} ----------\n")
            
            case 5: 
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.DR.value == memory_value, f"Read value {dut.DR.value} does not match the expected value {memory_value}"
            ### ENDEXECUTE #1
            case 6 | 7 | 8:  ### FETCH INTERRUPT
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.AC.value == expected_result_direct, f"Read value {dut.AC.value} does not match the expected value {expected_result_direct}"
            ### ENDFETCH INTERRUPT

            case 9: # DIRECT ADDRESSING
                dut._log.info(f"Cycle count: {cycle} ----------\n")            
            case 10 | 11: ### EXECUTE INTERRUPT AND
                dut._log.info(f"Cycle count: {cycle} ----------\n")
            case 12:
                dut.controller.IEN.value = 1; 
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.AR.value == interrupt_instruction & 0b0000111111111111, f"Read value {dut.AR.value} does not match the expected value {interrupt_instruction & 0b0000111111111111}"
            case 14: # DIRECT ADDRESSING
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.DR.value  == 0b0101010101010101, f"Read value {dut.DR.value} does not match the expected value {0b0101010101010101}"
            case 15:
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.AC.value  == memory_value & dut.DR.value, f"Read value {dut.AC.value} does not match the expected value {memory_value & dut.DR.value}"
            ### ENDEXECUTE INTERRUPT AND

            case _:
                dut._log.info(f"Cycle count: {cycle} ----------\n")
    
    dut._log.info("BC I test ended successfully!")

@cocotb.test()
async def FINAL_test(dut):
    # --- Test Setup --- #
    PC = 0x100
    dut.FGI.value = 0
    
    dut.data_path.memory.MEMORY[0x0001].value = 0x0050
    dut.data_path.memory.MEMORY[0x0002].value = 0xC000

    dut.data_path.memory.MEMORY[0x0030].value = 0xAAA9
    dut.data_path.memory.MEMORY[0x0050].value = 0xA030
    dut.data_path.memory.MEMORY[0x0060].value = 0x0FFF

    dut.data_path.memory.MEMORY[0x0ADD].value = 0xAAA9
    dut.data_path.memory.MEMORY[0x0AFF].value = 0xABCD
    dut.data_path.memory.MEMORY[0x0FFF].value = 0xAAAA

    dut.data_path.memory.MEMORY[PC].value   = 0xA050 #LDA
    dut.data_path.memory.MEMORY[PC+1].value = 0x7200 #CMA
    dut.data_path.memory.MEMORY[PC+2].value = 0x1ADD #ADD
    dut.data_path.memory.MEMORY[PC+3].value = 0x7020 #INC
    dut.data_path.memory.MEMORY[PC+4].value = 0x7004 #SZA
    dut.data_path.memory.MEMORY[PC+5].value = 0x5100 #BSA
    dut.data_path.memory.MEMORY[PC+6].value = 0x4111 #BUN
    # INTERRUPT #1 
    dut.data_path.memory.MEMORY[0x111].value = 0xF080 #ION
    dut.data_path.memory.MEMORY[0x112].value = 0xBFFF #STA
    # INTERRUPT #2
    dut.data_path.memory.MEMORY[0x113].value = 0x7001 #HLT

    dut.data_path.PC.A.value = PC

    #Start the clock
    await cocotb.start(Clock(dut.clk, 10, 'us').start(start_high=False))
    clkedge = FallingEdge(dut.clk)

    for cycle in range(70):
        await clkedge

        if DEBUG:
            printRegisters(dut)
            
        match cycle:
            case 0: ### FETCH LDA
                dut._log.info(f"Cycle count: {cycle} ----------\n")
            case 1:
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.PC.value == PC, f"Read value {dut.PC.value} does not match the expected value {PC}"
            case 2:
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.IR.value == dut.data_path.memory.MEMORY[PC].value, f"Read value {dut.IR.value} does not match the expected value {dut.data_path.memory.MEMORY[PC].value}"
                assert dut.PC.value == PC+1, f"Read value {dut.PC.value} does not match the expected value {PC+1}"
            case 3:
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.AR.value == dut.IR.value & 0b0000_1111_1111_1111, f"Read value {dut.AR.value} does not match the expected value {0b0000_1111_1111_1111}"
            ### ENDFETCH

            case 4: ### INDIRECT ADDRESSING
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.AR.value == 0x030, f"Read value {dut.AR.value} does not match the expected value {0x030}"
            case 5: ### EXECUTE LDA
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.DR.value == 0xAAA9, f"Read value {dut.DR.value} does not match the expected value {0xAAA9}"
            case 6: 
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.AC.value == dut.DR.value, f"Read value {dut.AR.value} does not match the expected value {dut.DR.value}"
            ### ENDEXECUTE 

            case 7:
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.PC.value == PC+1, f"Read value {dut.PC.value} does not match the expected value {PC+1}"
            case 8:
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.IR.value == dut.data_path.memory.MEMORY[PC+1].value, f"Read value {dut.IR.value} does not match the expected value {dut.data_path.memory.MEMORY[PC+1].value}"
                assert dut.PC.value == PC+2, f"Read value {dut.PC.value} does not match the expected value {PC+2}"
            case 9:
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.AR.value == dut.IR.value & 0b0000_1111_1111_1111, f"Read value {dut.AR.value} does not match the expected value {0b0000_1111_1111_1111}"
            ### ENDFETCH

            case 10: ### EXECUTE CMA
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.AC.value == 0x5556, f"Read value {dut.AC.value} does not match the expected value {0x5556}"
            ### ENDEXECUTE

            case 11: ### FETCH LDA
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.PC.value == PC+2, f"Read value {dut.PC.value} does not match the expected value {PC+2}"
            case 12:
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.IR.value == dut.data_path.memory.MEMORY[PC+2].value, f"Read value {dut.IR.value} does not match the expected value {dut.data_path.memory.MEMORY[PC+2].value}"
                assert dut.PC.value == PC+3, f"Read value {dut.PC.value} does not match the expected value {PC+3}"
            case 13:
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.AR.value == dut.IR.value & 0b0000_1111_1111_1111, f"Read value {dut.AR.value} does not match the expected value {0b0000_1111_1111_1111}"
            ### ENDFETCH 

            # From now on, Fetch and Decode cycles are not going to be checked as it is proven that it works from the previous test cases.

            case 14: ### DIRECT ADDRESSING
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.AR.value == 0x0ADD, f"Read value {dut.AR.value} does not match the expected value {0x0ADD}"
            case 15: ### EXECUTE ADD
                dut._log.info(f"Cycle count: {cycle} ----------\n") 
                assert dut.DR.value == 0xAAA9, f"Read value {dut.DR.value} does not match the expected value {0xAAA9}"
            case 16: 
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.AC.value == 0xFFFF, f"Read value {dut.AC.value} does not match the expected value {0xFFFF}"
            ### ENDEXECUTE

            case 17 | 18 | 19:  ### FETCH INC
                dut._log.info(f"Cycle count: {cycle} ----------\n")
            ### ENDFETCH

            case 20: ### EXECUTE INC
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.AC.value == 0x0000, f"Read value {dut.AC.value} does not match the expected value {0x0000}"
            ### ENDEXECUTE

            case 21 | 22 | 23:  ### FETCH SZA
                dut.FGI.value = 1 # FGI = 1, BUT INTERRUPT SETS AFTER FETCH AND DECODE AND INTERRUPT HAPPENS AFTER EXECUTE OF THE CURRENT INSTRUCTIONS
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.controller.R.value == 0, f"Read value {dut.controller.R.value} does not match the expected value {0}"
            ### ENDFETCH            

            case 24: ### EXECUTE SZA
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.controller.R.value == 1, f"Read value {dut.controller.R.value} does not match the expected value {1}"
                assert dut.PC.value == PC+6, f"Read value {dut.AC.value} does not match the expected value {PC+6}"
            ### ENDEXECUTE

            case 25:  ### INTERRUPT CYCLE
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.AR.value == 0x000, f"Read value {dut.AR.value} does not match the expected value {0x000}"
                assert dut.data_path.TR.A.value == PC+6, f"Read value {dut.data_path.TR.A.value} does not match the expected value {PC+6}"
            case 26:
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.PC.value == 0x000, f"Read value {dut.PC.value} does not match the expected value {0x000}"
                assert dut.data_path.memory.MEMORY.value[dut.AR.value] == dut.data_path.TR.A.value, f"Read value {dut.data_path.memory.MEMORY.value[dut.AR.value]} does not match the expected value {dut.data_path.TR.A.value}"
            case 27:
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.PC.value == 0x001, f"Read value {dut.PC.value} does not match the expected value {0x001}"
                assert dut.controller.IEN.value == 0x000, f"Read value {dut.controller.IEN.value} does not match the expected value {0x000}"
                assert dut.controller.R.value == 0x000, f"Read value {dut.controller.R.value} does not match the expected value {0x000}"
            ### ENDINTERRUPT CYCLE
        
            case 28 | 29 | 30: # FETCH DECODE of INTERRUPT OPERATION #1
                dut._log.info(f"Cycle count: {cycle} ----------\n")
            case 31: # DIRECT ADDRESING OF INTERRUPT #1 AND
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                prev_ac = dut.AC.value
            case 32: #EXECUTE OF INTERRUPT #1 AND
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.DR.value == dut.data_path.memory.MEMORY.value[dut.AR.value], f"Read value {dut.DR.value} does not match the expected value {dut.data_path.memory.MEMORY.value[dut.AR.value]}"
            case 33:
                assert dut.AC.value == prev_ac & dut.data_path.memory.MEMORY.value[dut.AR.value], f"Read value {dut.AC.value} does not match the expected value {prev_ac & dut.data_path.memory.MEMORY.value[dut.AR.value]}"
            ### ENDEXECUTE OF INTERRUPT #1 AND

            case 34 | 35 | 36: # FETCH INDIRECT BUN
                dut._log.info(f"Cycle count: {cycle} ----------\n")
            ### ENDFETCH

            case 37: # EXECUTE INDIRECT BUN
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.AR.value == PC+6, f"Read value {dut.AR.value} does not match the expected value {PC+6}"
            #ENDEXECUTE 

            # Note that BSA is skipped due to SZA operation

            case 38 | 39 | 40: # FETCH BUN
                dut.FGI.value = 0 # No interrupt
                dut._log.info(f"Cycle count: {cycle} ----------\n")
            #ENDFETCH

            case 41 | 42: # DIRECT ADDRESING & EXECUTE BUN
                dut._log.info(f"Cycle count: {cycle} ----------\n")
            #ENDEXECUTE

            case 43:
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.PC.value == dut.AR.value, f"Read value {dut.PC.value} does not match the expected value {dut.AR.value}"
            
            case 44 | 45 | 46: # FETCH 
                dut._log.info(f"Cycle count: {cycle} ----------\n")
            #ENDFETCH
            case 47: # EXECUTE ION 
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.controller.IEN.value == 1, f"Read value {dut.controller.IEN.value} does not match the expected value {1}"
            #ENDEXECUTE

            case 48 | 49 | 50: # FETCH STA
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                dut.FGI.value = 1 # INTERRUPT PENDING
            #ENDFETCH
            case 51: # GETTING THE EFFECTIVE ADDRESS 
                dut._log.info(f"Cycle count: {cycle} ----------\n")
            case 52: # EXECUTE STA
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.data_path.memory.MEMORY.value[dut.AR.value] == dut.AC.value, f"Read value {dut.data_path.memory.MEMORY.value[dut.AR.value]} does not match the expected value {dut.AC.value}"
            #ENDEXECUTE
            
            case 53:  ### INTERRUPT CYCLE
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.AR.value == 0x000, f"Read value {dut.AR.value} does not match the expected value {0x000}"
                assert dut.data_path.TR.A.value == 0x111 + 2, f"Read value {dut.data_path.TR.A.value} does not match the expected value {0x111 + 2}"
            case 54:
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.PC.value == 0x000, f"Read value {dut.PC.value} does not match the expected value {0x000}"
                assert dut.data_path.memory.MEMORY.value[dut.AR.value] == dut.data_path.TR.A.value, f"Read value {dut.data_path.memory.MEMORY.value[dut.AR.value]} does not match the expected value {dut.data_path.TR.A.value}"
            case 55:
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.PC.value == 0x001, f"Read value {dut.PC.value} does not match the expected value {0x001}"
                assert dut.controller.IEN.value == 0x000, f"Read value {dut.controller.IEN.value} does not match the expected value {0x000}"
                assert dut.controller.R.value == 0x000, f"Read value {dut.controller.R.value} does not match the expected value {0x000}"
            ### ENDINTERRUPT CYCLE
        
            case 56 | 57 | 58: # FETCH DECODE of INTERRUPT OPERATION #2
                dut._log.info(f"Cycle count: {cycle} ----------\n")
            case 59: # DIRECT ADDRESING OF INTERRUPT #2 AND
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                prev_ac = dut.AC.value
            case 60: #EXECUTE OF INTERRUPT #2 AND
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.DR.value == dut.data_path.memory.MEMORY.value[dut.AR.value], f"Read value {dut.DR.value} does not match the expected value {dut.data_path.memory.MEMORY.value[dut.AR.value]}"
            case 61:
                assert dut.AC.value == prev_ac & dut.data_path.memory.MEMORY.value[dut.AR.value], f"Read value {dut.AC.value} does not match the expected value {prev_ac & dut.data_path.memory.MEMORY.value[dut.AR.value]}"
            ### ENDEXECUTE OF INTERRUPT #1 AND

            case 62 | 63 | 64: ### FETCH HLT
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                #assert dut.data_path.AC.A.value == ac_value, f"Read value {dut.data_path.AC.A.value} does not match the written AC value {ac_value}"
            ### ENDFETCH

            case 65: ### EXECUTE HLT
                dut._log.info(f"Cycle count: {cycle} ----------\n")            
            case 66: 
                dut._log.info(f"Cycle count: {cycle} ----------\n")
                assert dut.controller.T.value == 0b0000000000000001, f"Read value {dut.controller.T.value} does not match the T = T0 value {0b0000000000000001}"
            ### ENDEXECUTE

            case _:
                dut._log.info(f"Cycle count: {cycle} ----------\n")
    
    dut._log.info("BC I test ended successfully!")