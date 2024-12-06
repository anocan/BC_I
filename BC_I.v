//Don't change the module I/O
module BC_I #(
     parameter WIDTH=16)
(
    input clk,
    input FGI,
    output [11:0] PC,
    output [11:0] AR,
    output [15:0] IR,
    output [15:0] AC,
    output [15:0] DR
);


// Declare inputs and output
wire [2:0] SELECT;               // 3-bit select signal

wire [WIDTH-1:0] IN; //{ 1'b0, {(WIDTH-6){1'b0}}, {(WIDTH-11){1'b1}} };
wire [WIDTH-1:0] DRI; //b1111111111110110
wire [WIDTH-1:0] RES;
wire Z;
wire N;
wire OVF; 

wire w_E;
wire w_CO;

wire w_WE;
wire w_RST;
wire w_INC;
wire [WIDTH-1:0] w_DATA;
wire w_A;

wire w_MWE;
wire [15:0] w_W_DATA;  
wire [11:0] w_IN_ADF;
wire [15:0] w_R_DATA;   


initial begin
end

//mux8to1 muxff(.MUX_INPUT(MUX_INPUT), .SELECT(SELECT), .MUX_OUT(MUX_OUT));
ALU alu(.AC(IN),
.DR(DRI),
.E(w_E),
.OPSEL(SELECT),
.CO(w_CO),
.OVF(OVF),
.N(N),
.Z(Z),
.RESULT(RES)
);

E_FF e_ff(
.clk(clk),
.LOAD(),          
.CMP(),      
.RST(),    
.E(w_E)   
);

RwLRI ac_r(
.clk(clk),
.WE(w_WE),       
.RST(w_RST), 
.INC(w_INC),          
.DATA(w_DATA),  
.A(AC) 
);

M memory(
.clk(clk),
.WE(w_MWE),       
.W_DATA(w_W_DATA),  
.IN_ADF(w_IN_ADF),
.R_DATA(w_R_DATA)    
);



endmodule