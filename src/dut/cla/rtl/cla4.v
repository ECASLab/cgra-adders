//----------------------------------------------------------------------------
// Title        : 4-bit Carry Lookahead Adder (CLA)
// File         : cla4.v
// Date         : 2025-06-04
// Author       : Erick Andrés Obregón Fonseca
// Email        : erickof@ieee.org
// Organization : ECASLAB
// Description  : 4-bit carry lookahead adder. Computes sum and carry-out with
//                reduced delay compared to ripple-carry by anticipating
//                carries.
// License      : MIT License (see LICENSE file for details)
//----------------------------------------------------------------------------
module cla4 (
  // 4-bit input operand A
  input  wire [3:0] a,
  // 4-bit input operand B
  input  wire [3:0] b,
  // Carry-in input
  input  wire       c_in,
  // 4-bit output sum
  output wire [3:0] sum,
  // Carry-out output
  output wire       c_out
);
  wire [3:0] carry;

  // Carry[0] is the input carry
  assign carry[0] = c_in;

  // Compute internal carry signals using lookahead logic
  assign carry[0] = c_in;
  assign carry[1] = (a[0] & b[0]) | ((a[0] ^ b[0]) & carry[0]);
  assign carry[2] = (a[1] & b[1]) | ((a[1] ^ b[1]) & ((a[0] & b[0]) | ((a[0] ^ b[0]) & carry[0])));
  assign carry[3] = (a[2] & b[2]) | ((a[2] ^ b[2]) & ((a[1] & b[1]) | ((a[1] ^ b[1]) & ((a[0] & b[0]) | ((a[0] ^ b[0]) & carry[0])))));

  // Final carry-out computation
  assign c_out = (a[3] & b[3]) | ((a[3] ^ b[3]) & ((a[2] & b[2]) | ((a[2] ^ b[2]) & ((a[1] & b[1]) | ((a[1] ^ b[1]) & ((a[0] & b[0]) | ((a[0] ^ b[0]) & carry[0])))))));

  // Compute the 4-bit sum
  assign sum = a ^ b ^ carry;
endmodule
