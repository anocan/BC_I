module RwLRI #(
    parameter WIDTH=16)
(
    input clk,
    input WE,       // Write enable
    input RST,    //  Synchronous reset
    input INC,     // Increment     
    input [WIDTH-1:0] DATA,  // Parallel load input
    output reg [WIDTH-1:0] A // Register output        
);

always @(posedge clk) begin
    if (RST) begin
        A <= 1'b0;
    end else if (WE) begin
        A <= DATA; 
    end else if (INC) begin
        A <= A + 1;  
    end else begin
        A <= A;
    end
end

endmodule
