#!/bin/bash
# Source tools
source ./tools.sh
# Source Python virtual environment
source ./env/bin/activate

# Adders to run
export ADDERS="rca cla"
# Building block for each adder
export BUILDING_BLOCK="full_adder cla4"
# Size of the adder
export BIT_WIDTHS="4 8 16 32 64"

# Run Design Compiler
dc_shell -f ./run.tcl

# Extract the results and generate metrics
python3 generate_metrics.py

# Print report summary
column -s, -t report_summary.csv

# Plot the metrics
python3 plot_metrics.py
