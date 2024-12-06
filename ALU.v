module ALU #(
    parameter WIDTH=16)
(
	input [WIDTH-1:0] AC,
	input [WIDTH-1:0] DR,
    input E,
    input [2:0] OPSEL,
	output reg  CO,
    output reg  OVF,
    output reg  N,
    output reg  Z,
    output reg [WIDTH-1:0] RESULT
);

initial begin
    CO = 0;
    OVF = 0;
end

always@(*) begin
    CO = 0; 
    OVF = 0;

	case(OPSEL)
        3'b000: begin
            {CO,RESULT} = AC + DR;
            OVF = ( ~AC[WIDTH-1] && ~DR[WIDTH-1] && RESULT[WIDTH-1] || 
            AC[WIDTH-1] && DR[WIDTH-1] && ~RESULT[WIDTH-1]);
        end    
        3'b001: RESULT = AC & DR;   
        3'b010: RESULT = DR;   
        3'b011: RESULT = ~AC;   
        3'b100: begin 
            CO = AC[0];
            RESULT = (AC >> 1);
            RESULT[WIDTH-1] = E; 
        end
        3'b101: begin 
            CO = AC[WIDTH-1];
            RESULT = (AC << 1);
            RESULT[0] = E; 
        end
	endcase
    Z = RESULT == 0;
    N = RESULT[WIDTH-1];
end
	 
endmodule	 