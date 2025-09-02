"""
File: cocotb_runner.py
Author: Erick Andres Obregon Fonseca
Date: 2025-08-19
Description: Utility for launching cocotb testbenches via Makefile.
License: MIT

This module defines a helper function to construct and run a cocotb
simulation command line using the DUT configuration file.

Notes
-----
- Expects a configuration Python file at ``dut/<dut_name>/config.py`` with a
  global dictionary named ``CONFIG``.
- The ``CONFIG`` dictionary must define:
    * ``rtl_files`` : list[str]
        RTL source files (relative paths).
    * ``top_module`` : str
        Name of the DUT's top-level module.
    * ``parameters`` : dict[str, str] (optional)
        Verilog parameters to pass at compile-time.
- Invokes the simulator using ``make`` and a cocotb-compatible Makefile.
"""
import os

from typing import Any

from cocotb_test.simulator import run


def run_cocotb(dut_name: str, test_name: str) -> None:
    """
    Run a cocotb testbench for a given DUT.

    Parameters
    ----------
    dut_name : str
        Name of the DUT (corresponds to subdirectory under ``dut/``).
    test_name : str
        Full Python module name of the test (e.g., ``sim.tests.test_add_basic``).

    Notes
    -----
    - Loads configuration dynamically from ``dut/<dut_name>/config.py``.
    - Constructs a ``make`` command line with:
        * TOPLEVEL (DUT top module),
        * MODULE (test Python module),
        * EXTRA_COMPILE_ARGS (parameters),
        * VERILOG_SOURCES (list of RTL files).
    - Prints the constructed command before executing it.

    Raises
    ------
    ImportError
        If the DUT config module cannot be found.
    KeyError
        If required keys are missing in the config dictionary.
    subprocess.CalledProcessError
        If the simulation fails during execution.
    """
    # Import configuration dictionary dynamically from
    # dut/<dut_name>/config.py
    cfg: dict[str, Any] = __import__(
        f"dut.{dut_name}.config", fromlist=["CONFIG"]
    ).CONFIG

    # Build list of RTL sources
    rtl_files = [os.path.join("dut", dut_name, f) for f in cfg["rtl_files"]]

    # Get parameter dictionary
    parameters = cfg.get("parameters", {})

    # Run cocotb simulation
    run(verilog_sources=rtl_files,
        toplevel=cfg["top_module"],
        module=test_name,
        parameters=parameters)
