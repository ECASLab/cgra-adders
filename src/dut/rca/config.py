"""
File: config.py
Author: Erick Andres Obregon Fonseca
Date: 2025-08-19
Description: Configuration dictionary for the Ripple-Carry Adder (RCA).
License: MIT.

This file defines the ``CONFIG`` dictionary, which provides metadata and build
information for the cocotb test environment.

Structure
---------
CONFIG : dict
    'name' : str
        Identifier for the DUT (e.g., "rca").
    'top_module' : str
        Name of the Verilog top-level module for the DUT.
    'rtl_files' : list[str]
        List of relative paths to the RTL source files.
    'parameters' : dict[str, Any]
        Parameter overrides for the DUT (e.g., bit-width N).
    'ports' : dict[str, str]
        Mapping of logical signal names (used in tests) to DUT port names.

Notes
-----
- The parameter ``N`` (adder width) is chosen randomly from [4, 8, 16, 32] at
  import time. This ensures variability in tests but also means simulations
  may run with different widths on different runs.
- For reproducibility, consider fixing a random seed or replacing the random
  choice with a fixed value during regression.
"""
import random


CONFIG = {
    "name": "rca",
    "top_module": "rca",
    "rtl_files": [
        "rtl/full_adder.v",
        "rtl/rca.v",
    ],
    "parameters": {
        # Bit-width of the adder; randomized at import time
        "N": random.choice([4, 8, 16, 32]),
    },
    "ports": {
        # Mapping of logical names (used in tests) to DUT port names
        "a": "a",
        "b": "b",
        "c_in": "c_in",
        "sum": "sum",
        "c_out": "c_out",
    },
}
