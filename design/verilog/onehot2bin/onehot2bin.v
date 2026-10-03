`default_nettype none

module onehot2bin #(parameter N = 64)
(
  input logic [N-1:0] in,
  output logic [$clog2(N)-1:0] out
);

  always_comb begin
	  out = 0;
	  for (int i = 0; i < N; i++) begin
		  if (in[i])
			  out = i;
	  end
  end
endmodule
