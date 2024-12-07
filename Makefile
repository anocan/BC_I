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

# TOPLEVEL is the name of the toplevel module in your Verilog or VHDL file
#Should be the name of the basic computer module for you
TOPLEVEL = BC_I #BC_I

# MODULE is the basename of the Python test file
#Name of your python file
MODULE = cocotb_bc1_test

#TESTCASE = basic_computer_test
test1:
	$(MAKE) sim TOPLEVEL=$(TOPLEVEL) MODULE=$(MODULE) TESTCASE=basic_computer_test

test2:
	$(MAKE) sim TOPLEVEL=$(TOPLEVEL) MODULE=$(MODULE) TESTCASE=alu_test

test3:
	$(MAKE) sim TOPLEVEL=$(TOPLEVEL) MODULE=$(MODULE) TESTCASE=data_path_test

test4:
	$(MAKE) sim TOPLEVEL=$(TOPLEVEL) MODULE=$(MODULE) TESTCASE=controller_test

clear:
	rm -rf sim_build results.xml *.vcd

# Force recompilation and run specific tests (accepts test case as an argument)
run: clear
	$(MAKE) $(TESTCASE)

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim