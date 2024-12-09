module mux8to1 #(
     parameter WIDTH=16)
    (
	  input	[WIDTH-1:0] MUX_INPUT [0:7],
	  input [2:0] SELECT,
	  output reg [WIDTH-1:0] MUX_OUT
    );
	 
// ANIL BUDAK - 2574812
always@(*) begin
	case(SELECT)
		3'b000: MUX_OUT = MUX_INPUT[0];
		3'b001: MUX_OUT = MUX_INPUT[1];
		3'b010: MUX_OUT = MUX_INPUT[2];
		3'b011: MUX_OUT = MUX_INPUT[3];
		3'b100: MUX_OUT = MUX_INPUT[4];
		3'b101: MUX_OUT = MUX_INPUT[5];
		3'b110: MUX_OUT = MUX_INPUT[6];
		3'b111: MUX_OUT = MUX_INPUT[7];
		default: MUX_OUT = {WIDTH{1'b0}};
	endcase
end
	 
endmodule	 