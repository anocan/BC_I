//Don't change the module I/O
module BC_I #(
    parameter WIDTH=16,
    parameter CTRL_LNGTH = 21)
(
    input clk,
    input FGI,
    output [11:0] PC,
    output [11:0] AR,
    output [15:0] IR,
    output [15:0] AC,
    output [15:0] DR
);
 
wire [15:0] w_WRD;

wire [2:0] w_BUS_SEL;
wire [2:0] w_CTRL_SGNLS [0:CTRL_LNGTH-1];
wire [WIDTH-1:0] w_IR, w_DR, w_AC;
wire [11:0] w_AR, w_PC;

initial begin
end

assign PC = w_PC;
assign AR = w_AR;
assign IR = w_IR;
assign AC = w_AC;
assign DR = w_DR;

DATA_PATH data_path(
.clk(clk),            
.BUS_SEL(w_BUS_SEL),   
.CTRL_SGNLS(w_CTRL_SGNLS),
.PC_OUT(w_PC),
.AR_OUT(w_AR),
.IR_OUT(w_IR),
.AC_OUT(w_AC),
.DR_OUT(w_DR),
.WRD(w_WRD)   
);

CONTROLLER controller(
.clk(clk),
.IR(w_IR),
.BUS_SEL(w_BUS_SEL), 
.CTRL_SGNLS(w_CTRL_SGNLS)
);


endmodule