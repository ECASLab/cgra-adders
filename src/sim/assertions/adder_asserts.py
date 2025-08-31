"""
File: adder_asserts.py
Author: Erick Andres Obregon Fonseca
Date: 2025-08-19
Description: Assertion helpers for verifying N-bit adder outputs.
License: MIT.

This module provides reusable assertion functions for checking the correctness
of adder outputs in cocotb-based testbenches.
"""
from cocotb.handle import HierarchyObject


def assert_adder_sum(dut: HierarchyObject, expected_sum: int) -> None:
    """
    Assert that the DUT's sum output matches the expected value.

    Parameters
    ----------
    dut : HierarchyObject
        Cocotb handle to the DUT (must expose a ``sum`` signal).
    expected_sum : int
        Expected value of the sum output.

    Raises
    ------
    AssertionError
        If the DUT's ``sum`` signal does not equal the expected value.
    """
    sum_val = int(dut.sum.value)
    assert sum_val == expected_sum, (
        f"Sum mismatch: got {sum_val}, expected {expected_sum}"
    )


def assert_adder_c_out(dut: HierarchyObject, expected_c_out: int) -> None:
    """
    Assert that the DUT's carry-out output matches the expected value.

    Parameters
    ----------
    dut : HierarchyObject
        Cocotb handle to the DUT (must expose a ``c_out`` signal).
    expected_c_out : int
        Expected value of the carry-out output (0 or 1).

    Raises
    ------
    AssertionError
        If the DUT's ``c_out`` signal does not equal the expected value.
    """
    c_out_val = int(dut.c_out.value)
    assert c_out_val == expected_c_out, (
        f"C_out mismatch: got {c_out_val}, expected {expected_c_out}"
    )
