//----------------------------------------------------------------------------
// Title       : N-bit Carry Lookahead Adder (CLA)
// File        : cla.v
// Date        : 2025-06-04
// Author      : Erick Andrés Obregón Fonseca
// Email       : erickof@ieee.org
// Organization: ECASLAB
// Description : Parametrizable carry lookahead adder constructed from
//               multiple 4-bit CLA blocks (cla4). Reduces carry propagation
//               delay by computing intermediate group carries in parallel.
// License     : MIT License (see LICENSE file for details)
//----------------------------------------------------------------------------
`include "cla4.v"

module cla #(
  // Adder width (must be a multiple of 4)
  parameter N = 8 
) (
  // N-bit input operand A
  input  wire [N-1:0] a,
  // N-bit input operand B
  input  wire [N-1:0] b,
  // Input carry
  input  wire         c_in,
  // N-bit sum output
  output wire [N-1:0] sum,
  // Final carry-out
  output wire         c_out
);

  // Number of 4-bit CLA blocks required
  localparam ADDERS = N / 4;

  // Carry wires between each CLA block (ADDERS+1 to include c_in and c_out)
  wire [ADDERS:0] carry;

  // Initial carry-in assignment
  assign carry[0] = c_in;

  // Generate ADDERS instances of 4-bit CLA blocks (cla4)
  genvar i;
  generate
    for (i = 0; i < ADDERS; i = i + 1) begin: gb_cla4
      cla4 adder (
        // Slice bits [4i+3:4i] for operand A and B
        .a    (a[4*i+3: 4*i]),
        .b    (b[4*i+3: 4*i]),
        // Carry-in for this block
        .c_in (carry[i]),
        // Sum bits [4i+3:4i]
        .sum  (sum[4*i+3: 4*i]),
        // Carry-out to the next block
        .c_out(carry[i+1])
      );
    end
  endgenerate

  // Final carry-out from the last CLA block
  assign c_out = carry[ADDERS];

endmodule
