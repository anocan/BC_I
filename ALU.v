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
    output reg [1:0] CNTRL_E, // CNTRL_E==10 = LOAD_E, CNTRL_E==01 = RST_E, CNTRL_E==00,11 = NOP
    output reg [WIDTH-1:0] RESULT
);

initial begin
    CO = 0;
    OVF = 0;
end

always@(*) begin
    CO = 0; 
    OVF = 0;
    CNTRL_E = 2'b11;

	case(OPSEL)
        3'b000: begin // AC <- AC + DR
            {CO,RESULT} = AC + DR;
            OVF = ( ~AC[WIDTH-1] && ~DR[WIDTH-1] && RESULT[WIDTH-1] || 
            AC[WIDTH-1] && DR[WIDTH-1] && ~RESULT[WIDTH-1]);
            CNTRL_E = {CO,~CO};
        end    
        3'b001: RESULT = AC & DR; // AC <- AC ∧ DR   
        3'b010: RESULT = DR; // AC <- DR     
        3'b011: RESULT = ~AC; // AC <- AC'
        3'b100: begin // AC <- {E, shr[AC]}   
            CO = AC[0];
            RESULT = (AC >> 1);
            RESULT[WIDTH-1] = E; 
            CNTRL_E = {CO,~CO};
        end
        3'b101: begin // AC <- {shl[AC], E}   
            CO = AC[WIDTH-1];
            RESULT = (AC << 1);
            RESULT[0] = E;
            CNTRL_E = {CO,~CO};
        end
        3'b111: RESULT = RESULT; // NOP
        default: RESULT = RESULT; // NOP
	endcase
    Z = RESULT == 0;
    N = RESULT[WIDTH-1];
end
	 
endmodule	 