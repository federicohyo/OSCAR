`default_nettype none

module bin2onehot #(parameter N=64)
(
  input wire [$clog2(N)-1:0] in,
  output wire [N-1:0] out
);
  genvar i;
  generate
    for (i = 0; i < 64; i = i + 1) begin
      assign out[i] = (in == i);
    end
  endgenerate
endmodule
