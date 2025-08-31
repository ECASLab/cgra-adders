#=============================================================================
# File: Makefile
# Author: Erick Andres Obregon Fonseca
# Date: 2025-08-19
# Description: Top-level Makefile for running cocotb simulations with Icarus.
# License: MIT.
#
# This Makefile is used by cocotb to build and run RTL simulations.
# It requires the following variables to be defined at invocation time:
#
#   MODULE          : Name of the cocotb Python test module
#   TOPLEVEL        : Name of the Verilog top-level module
#   VERILOG_SOURCES : List of Verilog source files for the DUT
#
# Example:
#   make MODULE=sim.tests.test_add_basic TOPLEVEL=rca \
#        VERILOG_SOURCES="dut/rca/rtl/full_adder.v dut/rca/rtl/rca.v"
#
# Notes:
# - This Makefile assumes Verilog sources and Icarus Verilog as simulator.
# - The cocotb helper `cocotb-config` is used to locate Makefile.sim.
#=============================================================================

TOPLEVEL_LANG = verilog
SIM = icarus

#-----------------------------------------------------------------------------
# Input validation: ensure required variables are defined
#-----------------------------------------------------------------------------
ifeq ($(MODULE),)
$(error MODULE is not defined. Use MODULE=<python.test.module>)
endif

ifeq ($(TOPLEVEL),)
$(error TOPLEVEL is not defined. Use TOPLEVEL=<dut_top_module>)
endif

ifeq ($(VERILOG_SOURCES),)
$(error VERILOG_SOURCES is not defined. Use VERILOG_SOURCES="file1.v file2.v ...")
endif

#-----------------------------------------------------------------------------
# Include cocotb's default simulation rules
#-----------------------------------------------------------------------------
include $(shell cocotb-config --makefiles)/Makefile.sim
