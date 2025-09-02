//----------------------------------------------------------------------------
// Title        : Full Adder
// File         : full_adder.v
// Date         : 2025-06-04
// Author       : Erick Andrés Obregón Fonseca
// Email        : erickof@ieee.org
// Organization : ECASLAB
// Description  : 1-bit full adder module used for ripple-carry and other
//                adder architectures. Computes sum and carry-out from inputs
//                a, b, and carry-in.
// License      : MIT License (see LICENSE file for details)
//----------------------------------------------------------------------------
`timescale 1ns / 1ps

module full_adder (
  // 1-bit input operand A
  input  wire a,
  // 1-bit input operand B
  input  wire b,
  // Carry-in input
  input  wire c_in,
  // 1-bit output sum
  output wire sum,
  // Carry-out output
  output wire c_out
);
  assign sum = a ^ b ^ c_in;
  assign c_out = (a & b) | (b & c_in) | (a & c_in);
endmodule
