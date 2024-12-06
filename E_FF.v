module E_FF (
    input clk,
    input LOAD,            // E <- 0
    input CMP,       // E <- E'
    input RST,    // Circular Right operation
    output reg E                 
);

initial begin
    E = 0;
end

always @(posedge clk) begin
    if (RST) begin
        E <= 1'b0;
    end else if (LOAD) begin
        E <= 1'b1; 
    end else if (CMP) begin
        E <= ~E;  
    end 
end

endmodule
