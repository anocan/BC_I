module SC(
    input clk,          
    input CLR,       
    input INR,
    input S,  
    output reg [15:0] T    
);

// ANIL BUDAK - 2574812
reg [3:0] SQ;  
    
initial begin
    SQ = 4'b0;
    T = 16'b0;
end   

always @(posedge clk) begin
    if (S) begin
        if (CLR)
            SQ <= 4'b0000;  
        else if (INR)
            SQ <= SQ + 1'b1;
    end   
end

always @(*) begin
    T = 16'b0;      
    T[SQ] = 1'b1;        
end

endmodule
