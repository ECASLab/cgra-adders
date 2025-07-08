
//----------------------------------------------------------------------------
// Title        : N-bit Ripple Carry Adder (RCA)
// File         : rca.v
// Date         : 2025-06-04
// Author       : Erick Andrés Obregón Fonseca
// Email        : erickof@ieee.org
// Organization : ECASLAB
// Description  : Parametrizable N-bit ripple carry adder using 1-bit full
//                adder cells. Propagates carry from LSB to MSB sequentially.
// License      : MIT License (see LICENSE file for details)
//----------------------------------------------------------------------------
`include "full_adder.v"

module rca #(
  // Width of the adder
  parameter N = 8
) (
  // N-bit input operand A
  input  wire [N-1:0] a,
  // N-bit input operand B
  input  wire [N-1:0] b,
  // Input carry
  input  wire         c_in,
  // N-bit output sum
  output wire [N-1:0] sum,
  // Carry-out from the MSB
  output wire         c_out
);
  // Internal carry signals (N+1 to include c_in and final c_out)
  wire [N:0] carry;

  // Assign initial carry-in
  assign carry[0] = c_in;

  // Generate N instances of 1-bit full adders
  genvar i;
  generate
    for (i = 0; i < N; i = i + 1) begin: gb_fa
      full_adder fa (
        .a     (a[i]),
        .b     (b[i]),
        .c_in  (carry[i]),
        .sum   (sum[i]),
        .c_out (carry[i+1])
      );
    end
  endgenerate

  // Final carry-out
  assign c_out = carry[N];
endmodule
