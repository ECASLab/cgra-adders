"""
File: adder_sequence.py
Author: Erick Andres Obregon Fonseca
Date: 2025-08-19
Description: Random stimulus generator for N-bit adder verification.
License: MIT.

This module defines the :class:`AdderSequence`, which produces random input
vectors (a, b, c_in) for testing an N-bit adder DUT.
"""
import random

from typing import List, Tuple


class AdderSequence:
    """
    Sequence generator for adder input vectors.

    Parameters
    ----------
    width : int
        Bit-width of the adder under test.

    Attributes
    ----------
    width : int
        Configured width (number of bits) of the adder.
    """

    def __init__(self, width: int) -> None:
        """Constructor for AdderSequence.

        Args:
            width (int): Bit-width of the adder.
        """
        self.width: int = width

    def generate_vectors(self, num_vectors: int = 1) -> List[Tuple[int, int, int]]:
        """
        Generate a list of random input vectors for the adder.

        Each vector is a tuple of three values:
        - ``a`` : int, random operand in [0, 2**width - 1]
        - ``b`` : int, random operand in [0, 2**width - 1]
        - ``c_in`` : int, random carry-in (0 or 1)

        Parameters
        ----------
        num_vectors : int, optional
            Number of vectors to generate. Default is 1.

        Returns
        -------
        List[Tuple[int, int, int]]
            List of (a, b, c_in) input vectors.

        Examples
        --------
        >>> seq = AdderSequence(width=4)
        >>> seq.generate_vectors(2)
        [(7, 12, 0), (3, 5, 1)]
        """
        max_val = (1 << self.width) - 1
        vectors: List[Tuple[int, int, int]] = []

        for _ in range(num_vectors):
            a = random.randint(0, max_val)
            b = random.randint(0, max_val)
            c_in = random.randint(0, 1)
            vectors.append((a, b, c_in))

        return vectors
