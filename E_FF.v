module E_FF (
    input clk,
    input [1:0] CNTRL_E, // CNTRL_E==10 = LOAD_E, CNTRL_E==01 = RST_E, CNTRL_E==00,11 = NOP
    input LOAD,   // E <- 1
    input CMP,    // E <- E'
    input RST,    // E <- 0
    output reg E                 
);

initial begin
    E = 0;
end

always @(posedge clk) begin
    if (RST || CNTRL_E == 2'b01) begin
        E <= 1'b0;
    end else if (LOAD || CNTRL_E == 2'b10) begin
        E <= 1'b1; 
    end else if (CMP) begin
        E <= ~E;  
    end 
end

endmodule
