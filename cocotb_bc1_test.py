import cocotb
from cocotb.triggers import Timer
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge

#TRUE for printing signals
DEBUG = True

#CHANGE THE BELOW SIGNAL NAMES TO MATCH YOUR DESIGN!!!!!!!!!!!!!!!!!
def print_my_computer_please(dut):
    #Log whatever signal you want from the datapath, called before positive clock edge
    dut._log.info("************ DUT Signals ***************")
    """ dut._log.info(f" PC: {dut.PC.value}\t {hex(dut.PC.value)}\n\
    AR: {dut.AR.value}\t {hex(dut.AR.value)}\n\
    IR: {dut.IR.value}\t {hex(dut.IR.value)}\n\
    AC: {dut.AC.value}\t {hex(dut.AC.value)}\n\
    DR: {dut.DR.value}\t {hex(dut.DR.value)}\n") 
    dut._log.info(f"IN: {dut.IN.value}")
    dut._log.info(f"DR: {dut.DRI.value}")
    dut._log.info(f"RES:{dut.RES.value}")
    dut._log.info(f"CO: {dut.w_CO.value}")
    dut._log.info(f"Z: {dut.Z.value}")
    dut._log.info(f"N: {dut.N.value}")
    dut._log.info(f"OVF: {dut.OVF.value}")
    dut._log.info(f"E: {dut.w_E.value}")
    dut._log.info(f"SEL: {dut.SELECT.value}") 
    dut._log.info(f"w_R_DATA: {dut.w_R_DATA.value}")
    dut._log.info(f"w_IN_ADF: {dut.w_IN_ADF.value}")
    dut._log.info(f"w_MWE: {dut.w_MWE.value}")
    dut._log.info(f"w_W_DATA: {dut.w_W_DATA.value}") """


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
            print_my_computer_please(dut)
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