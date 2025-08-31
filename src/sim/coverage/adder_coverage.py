"""
File: adder_coverage.py
Author: Erick Andres Obregon Fonseca
Date: 2025-08-19
Description: Functional coverage collector for an N-bit adder.
License: MIT.

This module defines the :class:`AdderCoverage`, which tracks unique input
combinations (a, b, c_in) applied to the DUT. It supports saving, loading,
merging, and reporting coverage data.
"""
import json

from typing import Set, Tuple


class AdderCoverage:
    """
    Collect and manage functional coverage for adder input vectors.

    Coverage Model
    --------------
    - Each sample is represented as a tuple (a, b, c_in).
    - Coverage is measured as the set of unique input combinations seen.
    - Supports persistence (save/load to JSON) and merging with other coverage
      objects.

    Attributes
    ----------
    covered : set[tuple[int, int, int]]
        Set of all unique input vectors observed.
    """

    def __init__(self) -> None:
        """Initialize an empty coverage set."""
        self.covered: Set[Tuple[int, int, int]] = set()

    def sample(self, a: int, b: int, cin: int) -> None:
        """
        Record a new input vector into the coverage set.

        Parameters
        ----------
        a : int
            Operand A.
        b : int
            Operand B.
        cin : int
            Carry-in bit (0 or 1).
        """
        key = (a, b, cin)
        self.covered.add(key)

    def save(self, filename: str) -> None:
        """
        Save coverage data to a JSON file.

        Parameters
        ----------
        filename : str
            Path to the output JSON file.
        """
        data = list(self.covered)
        with open(filename, "w") as f:
            json.dump(data, f)

    def load(self, filename: str) -> None:
        """
        Load coverage data from a JSON file.

        Parameters
        ----------
        filename : str
            Path to the input JSON file.

        Notes
        -----
        Overwrites the current coverage set.
        """
        with open(filename, "r") as f:
            self.covered = set(tuple(x) for x in json.load(f))

    def merge(self, other_coverage: "AdderCoverage") -> None:
        """
        Merge coverage data from another :class:`AdderCoverage` object.

        Parameters
        ----------
        other_coverage : AdderCoverage
            Another coverage object whose samples will be added.
        """
        self.covered.update(other_coverage.covered)

    def report(self) -> None:
        """
        Print a summary of collected coverage.

        Notes
        -----
        Currently reports only the total number of unique combinations.
        """
        print(f"[Coverage] Total unique input combinations: {len(self.covered)}")
