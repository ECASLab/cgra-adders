//----------------------------------------------------------------------------
// Title        : Kogge Stone Adder (KSA)
// File         : ksa.v
// Date         : 2025-07-08
// Author       : Erick Andrés Obregón Fonseca
// Email        : erickof@ieee.org
// Organization : ECASLAB
// Description  : Kogge Stone adder, a parallel prefix adder that computes
//                the sum and carry-out of two n-bit operands using a tree
//                structure to reduce delay compared to ripple-carry and
//                other adder architectures. This implementation is
//                parameterized for N-bit inputs but can be extended to
//                support wider operands by increasing the parameter N.
// License      : MIT License (see LICENSE file for details)
//----------------------------------------------------------------------------
`timescale 1ns / 1ps

module ksa #(
  parameter int N = 4
) (
  input  wire [N-1:0] a,
  input  wire [N-1:0] b,
  input  wire         c_in,
  output wire [N-1:0] sum,
  output wire         c_out
);
  // bitwise generate/propagate (using XOR propagate form)
  wire [N-1:0] g0 = a & b;
  wire [N-1:0] p0 = a ^ b;

  localparam int STAGES = $clog2(N);

  // prefix matrices
  wire [N-1:0] g [0:STAGES];
  wire [N-1:0] p [0:STAGES];

  // stage 0 seeds
  assign g[0] = g0;
  assign p[0] = p0;

  genvar stage, i;
  generate
    for (stage = 0; stage < STAGES; stage = stage + 1) begin : gb_stage
      for (i = 0; i < N; i = i + 1) begin : gen_g_p
        if (i < (1 << stage)) begin
          // pass-through (gray cell / buffer)
          assign g[stage + 1][i] = g[stage][i];
          assign p[stage + 1][i] = p[stage][i];
        end else begin
          // black cell combine
          assign g[stage + 1][i] = g[stage][i] | (p[stage][i] & g[stage][i - (1 << stage)]);
          assign p[stage + 1][i] = p[stage][i] & p[stage][i - (1 << stage)];
        end
      end
    end
  endgenerate

  // Final prefix results are G/P over [i:0]
  wire [N-1:0] G = g[STAGES];
  wire [N-1:0] P = p[STAGES];

  // Per-bit carries (carry into bit i+1). Incorporate c_in.
  wire [N-1:0] c = G | (P & {N{c_in}});

  // Sums: sum[0] uses c_in; sum[i] uses carry into bit i, which is c[i-1]
  assign sum[0] = p0[0] ^ c_in;

  genvar j;
  generate
    for (j = 1; j < N; j = j + 1) begin : gen_sum
      assign sum[j] = p0[j] ^ c[j-1];
    end
  endgenerate

  assign c_out = c[N-1];
endmodule // ksa
