import cocotb
from cocotb.triggers import Timer
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge

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
    #dut._log.info(f"OPSEL: {dut.data_path.OPSEL_ALU.value}")
    #dut._log.info(f"CNTRL: {dut.w_CTRL_SGNLS.value[20]}")
    dut._log.info(f"E: {dut.data_path.e_ff.E.value}")


@cocotb.test()
async def basic_computer_test(dut):
    """Try accessing the design."""
    A = 562
    B = 3131
    dut.w_IN_ADF.value = A

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
    e_value = 0         # Initial AC to be complemented
    cmp_e_value = 1-e_value
    dut.data_path.memory.MEMORY[address].value = instruction
    dut.data_path.memory.MEMORY[address+1].value = instruction # 2 CME Instructions
    dut.data_path.PC.A.value = address
    dut.data_path.e_ff.E.value = e_value

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