"""
File: test_add_basic.py
Author: Erick Andres Obregon Fonseca
Date: 2025-08-19
Description: Basic cocotb test for an N-bit adder.
License: MIT

This test applies a small sequence of input vectors to the DUT adder, waits
one simulation step, and checks both the sum and carry-out against a Python
reference model. Functional coverage is collected for the exercised input
space.

Assumptions
-----------
- The DUT exposes ports named in ``CONFIG["ports"]``:
  ``a``, ``b``, ``c_in``, ``sum``, ``c_out`` (names may be remapped).
- Output is registered or becomes stable within 1 ns after inputs change.
- The adder width ``N`` is taken from ``CONFIG["parameters"]["N"]``.

Usage
-----
This test is picked up by cocotb via the @cocotb.test decorator and can be run
with the repository's Makefile through the helper CLI:

    python run_test.py --dut cla --test test_add_basic
"""
from __future__ import annotations

import cocotb

from cocotb.handle import HierarchyObject
from cocotb.triggers import Timer

from sim.sequences.adder_sequence import AdderSequence
from sim.assertions.adder_asserts import assert_adder_sum, assert_adder_c_out
from sim.coverage.adder_coverage import AdderCoverage
from dut.cla.config import CONFIG


@cocotb.test()
async def test_adder_basic(dut: HierarchyObject) -> None:
    """
    Sanity test for the parameterized N-bit adder.

    Steps
    -----
    1. Read ``N`` and port names from the DUT configuration.
    2. Generate a set of (a, b, c_in) vectors from :class:`AdderSequence`.
    3. Drive the DUT inputs and wait 1 ns for outputs to settle.
    4. Compute the expected result using a Python reference model:
       ``sum = (a + b + c_in) & ((1 << N) - 1)``, ``c_out = >> N``.
    5. Check results with assertion helpers and sample functional coverage.
    6. Print a coverage report at the end.

    Timing
    ------
    Uses :class:`~cocotb.triggers.Timer`(1 ns). If the DUT is fully
    synchronous, consider replacing with a clocked trigger (e.g.,
    ``await RisingEdge(clk)``) and documenting the handshake.

    Raises
    ------
    AssertionError
        If the observed outputs do not match the reference model.
    """
    # Extract configuration
    N: int = dut.N.value
    ports: dict[str, str] = CONFIG["ports"]

    # Test infrastructure
    sequence = AdderSequence(N)
    coverage = AdderCoverage()

    mask = (1 << N) - 1

    for a, b, c_in in sequence.generate_vectors():
        # Drive DUT inputs using the configured port names
        getattr(dut, ports["a"]).value = a
        getattr(dut, ports["b"]).value = b
        getattr(dut, ports["c_in"]).value = c_in

        # Allow signals to propagate / outputs to settle
        await Timer(1, units="ns")

        # Python reference model (wrap-around on N bits + carry-out)
        total = a + b + c_in
        expected_sum = total & mask
        expected_c_out = total >> N

        # Assertions (read outputs inside helpers)
        assert_adder_sum(dut, expected_sum)
        assert_adder_c_out(dut, expected_c_out)

        # Functional coverage
        coverage.sample(a, b, c_in)

    # Emit functional coverage report
    coverage.report()
