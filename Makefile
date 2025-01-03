# Makefile

# defaults
SIM ?= icarus
TOPLEVEL_LANG ?= verilog

#Add your sources one by one as below or use *.v to add all verilog files
VERILOG_SOURCES += $(PWD)/BC_I.v
VERILOG_SOURCES += $(PWD)/ALU.v
VERILOG_SOURCES += $(PWD)/mux8to1.v
VERILOG_SOURCES += $(PWD)/E_FF.v
VERILOG_SOURCES += $(PWD)/RwLRI.v
VERILOG_SOURCES += $(PWD)/M.v
VERILOG_SOURCES += $(PWD)/DATA_PATH.v
VERILOG_SOURCES += $(PWD)/SC.v
VERILOG_SOURCES += $(PWD)/CONTROLLER.v

# ANIL BUDAK - 2574812

# TOPLEVEL is the name of the toplevel module in your Verilog or VHDL file
#Should be the name of the basic computer module for you
TOPLEVEL = BC_I #BC_I

# MODULE is the basename of the Python test file
#Name of your python file
MODULE = cocotb_bc1_test

#TESTCASE = basic_computer_test

# Register Reference Instructions
testCLA:
	$(MAKE) sim TOPLEVEL=$(TOPLEVEL) MODULE=$(MODULE) TESTCASE=CLA_test

testCLE:
	$(MAKE) sim TOPLEVEL=$(TOPLEVEL) MODULE=$(MODULE) TESTCASE=CLE_test

testCMA:
	$(MAKE) sim TOPLEVEL=$(TOPLEVEL) MODULE=$(MODULE) TESTCASE=CMA_test

testCME:
	$(MAKE) sim TOPLEVEL=$(TOPLEVEL) MODULE=$(MODULE) TESTCASE=CME_test

testCIR:
	$(MAKE) sim TOPLEVEL=$(TOPLEVEL) MODULE=$(MODULE) TESTCASE=CIR_test

testCIL:
	$(MAKE) sim TOPLEVEL=$(TOPLEVEL) MODULE=$(MODULE) TESTCASE=CIL_test

testINC:
	$(MAKE) sim TOPLEVEL=$(TOPLEVEL) MODULE=$(MODULE) TESTCASE=INC_test

testSPA:
	$(MAKE) sim TOPLEVEL=$(TOPLEVEL) MODULE=$(MODULE) TESTCASE=SPA_test

testSNA:
	$(MAKE) sim TOPLEVEL=$(TOPLEVEL) MODULE=$(MODULE) TESTCASE=SNA_test

testSZA:
	$(MAKE) sim TOPLEVEL=$(TOPLEVEL) MODULE=$(MODULE) TESTCASE=SZA_test

testSZE:
	$(MAKE) sim TOPLEVEL=$(TOPLEVEL) MODULE=$(MODULE) TESTCASE=SZE_test

testHLT:
	$(MAKE) sim TOPLEVEL=$(TOPLEVEL) MODULE=$(MODULE) TESTCASE=HLT_test

# Memory Reference Instructions
testAND:

	$(MAKE) sim TOPLEVEL=$(TOPLEVEL) MODULE=$(MODULE) TESTCASE=AND_test
testADD:
	$(MAKE) sim TOPLEVEL=$(TOPLEVEL) MODULE=$(MODULE) TESTCASE=ADD_test

testLDA:
	$(MAKE) sim TOPLEVEL=$(TOPLEVEL) MODULE=$(MODULE) TESTCASE=LDA_test

testSTA:
	$(MAKE) sim TOPLEVEL=$(TOPLEVEL) MODULE=$(MODULE) TESTCASE=STA_test

testBUN:
	$(MAKE) sim TOPLEVEL=$(TOPLEVEL) MODULE=$(MODULE) TESTCASE=BUN_test

testBSA:
	$(MAKE) sim TOPLEVEL=$(TOPLEVEL) MODULE=$(MODULE) TESTCASE=BSA_test

testISZ:
	$(MAKE) sim TOPLEVEL=$(TOPLEVEL) MODULE=$(MODULE) TESTCASE=ISZ_test

# Interrupt Test
testR:
	$(MAKE) sim TOPLEVEL=$(TOPLEVEL) MODULE=$(MODULE) TESTCASE=R_test

# Final Test Case
testFinal:
	$(MAKE) sim TOPLEVEL=$(TOPLEVEL) MODULE=$(MODULE) TESTCASE=FINAL_test

clear:
	rm -rf sim_build results.xml *.vcd

# Force recompilation and run specific tests (accepts test case as an argument)
run: clear
	$(MAKE) $(TESTCASE)

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim