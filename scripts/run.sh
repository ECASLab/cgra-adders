#!/bin/bash
#==============================================================================
# Title         : Adder Synthesis and Evaluation Flow
# File          : run_flow.sh
# Date          : 2025-06-04
# Author        : Erick Andres Obregon Fonseca
# Email         : erickof@ieee.org/erickof@estudiantec.cr
# Description   : Full automation script for adder synthesis, metrics
#                 extraction, and plotting of results.
# License       : MIT.
#
# This script automates the verification & synthesis flow for multiple adders:
# 1. Sources required tools and Python environment.
# 2. Defines which adders, building blocks, and bit widths to evaluate.
# 3. Runs Synopsys Design Compiler (dc_shell) with the TCL flow script.
# 4. Extracts results and generates consolidated CSV metrics.
# 5. Prints a formatted summary of results.
# 6. Produces plots for area, delay, and power metrics.
#
# Usage:
#   ./run_flow.sh
#
# Notes:
# - Requires `tools.sh` to be present for tool setup.
# - Requires Python virtual environment in `./env/`.
# - Expects `run.tcl`, `generate_metrics.py`, and `plot_metrics.py` scripts.
#==============================================================================

#-----------------------------------------------------------------------------
# Source tools setup and Python virtual environment
#-----------------------------------------------------------------------------
source ./tools.sh
source ./env/bin/activate

#-----------------------------------------------------------------------------
# Define environment variables for adders, building blocks, and bit widths
#-----------------------------------------------------------------------------
export ADDERS="rca cla"
export BUILDING_BLOCK="full_adder cla4"
export BIT_WIDTHS="4 8 16 32 64"

#-----------------------------------------------------------------------------
# Step 1: Run synthesis with Design Compiler
#-----------------------------------------------------------------------------
dc_shell -f ./run.tcl

#-----------------------------------------------------------------------------
# Step 2: Extract results and generate consolidated metrics
#-----------------------------------------------------------------------------
python3 generate_metrics.py

#-----------------------------------------------------------------------------
# Step 3: Print report summary in table format
#-----------------------------------------------------------------------------
column -s, -t report_summary.csv

#-----------------------------------------------------------------------------
# Step 4: Plot metrics (area, delay, power) using Python scripts
#-----------------------------------------------------------------------------
python3 plot_metrics.py
