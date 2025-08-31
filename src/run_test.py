"""
File: run_test.py
Author: Erick Andres Obregon Fonseca
Date: 2025-08-19
Description: Command-line entry point for launching cocotb testbenches.
License: MIT

This script provides a command-line interface to run a cocotb testbench
against a specified Design Under Test (DUT).

Usage
-----
Example:
    python run_test.py --dut rca --test test_add_basic

Parameters
----------
--dut : str
    Name of the DUT.
--test : str
    Name of the cocotb test module located under ``sim/tests/``.

Notes
-----
- The ``run_cocotb`` utility is imported from
  ``sim.utils.cocotb_runner`` and is responsible for test execution.
- The test name is automatically expanded to include the module
  namespace ``sim.tests.<test>``.
"""
import argparse

from sim.utils.cocotb_runner import run_cocotb


def main(argv: list[str] | None = None) -> None:
    """
    Parse command-line arguments and execute the cocotb test.

    Parameters
    ----------
    argv : list[str] | None, optional
        Command-line arguments excluding the program name. If None,
        ``argparse`` will use ``sys.argv[1:]``.

    Raises
    ------
    SystemExit
        If required arguments are missing or invalid.
    """
    parser = argparse.ArgumentParser(description="Run cocotb testbench")
    parser.add_argument(
        "--dut",
        required=True,
        help="Name of the Design Under Test (DUT)"
    )
    parser.add_argument(
        "--test",
        required=True,
        help="Name of the cocotb test module (under sim/tests/)"
    )

    args = parser.parse_args(argv)

    # Run the cocotb test, prefixing the test with the sim.tests namespace
    run_cocotb(dut_name=args.dut, test_name=f"sim.tests.{args.test}")


if __name__ == "__main__":
    main()
