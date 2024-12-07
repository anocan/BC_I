module DATA_PATH #(
    parameter WIDTH=16,
    parameter CTRL_LNGTH = 21)
(
    input clk,             // Clock signal
    input [2:0] BUS_SEL,   // Bus select (3-bit)
    input [2:0] CTRL_SGNLS [0:CTRL_LNGTH-1],
    input [15:0] WRD,
    output [11:0] PC_OUT,
    output [11:0] AR_OUT,
    output [WIDTH-1:0] IR_OUT,
    output [WIDTH-1:0] AC_OUT,
    output [WIDTH-1:0] DR_OUT
);

wire [WIDTH-1:0] MUX_ARRAY [0:7]; // Array of 8 inputs, each 16-bit wide

// Define internal wires
wire [WIDTH-1:0] BUS;          // Common bus
wire [WIDTH-1:0] w_AC, w_DR, w_MEM; // Register outputs
wire [11:0] w_AR, w_PC;          // Address register outputs
wire [WIDTH-1:0] w_ALU;   // ALU result
wire [WIDTH-1:0] w_TR, w_IR;
wire w_E;
wire [1:0] w_CNTRL_E;

assign PC_OUT = w_PC;
assign AR_OUT = w_AR;
assign IR_OUT = w_IR;
assign AC_OUT = w_AC;
assign DR_OUT = w_DR;

initial begin
   
end

// Control Signals
wire LD_AR, // CTRL_SGNLS[0]
INR_AR,     // CTRL_SGNLS[1]
CLR_AR,     // CTRL_SGNLS[2]
LD_PC,      // CTRL_SGNLS[3]
INR_PC,     // CTRL_SGNLS[4]
CLR_PC,     // CTRL_SGNLS[5]
LD_DR,      // CTRL_SGNLS[6]
INR_DR,     // CTRL_SGNLS[7]
CLR_DR,     // CTRL_SGNLS[8]
LD_AC,      // CTRL_SGNLS[9]
INR_AC,     // CTRL_SGNLS[10]
CLR_AC,     // CTRL_SGNLS[11]
LD_IR,      // CTRL_SGNLS[12]
LD_TR,      // CTRL_SGNLS[13]
INR_TR,     // CTRL_SGNLS[14]
CLR_TR,     // CTRL_SGNLS[15]
MEM_WE,     // CTRL_SGNLS[16]
LD_E,       // CTRL_SGNLS[17]
CMP_E,      // CTRL_SGNLS[18]
CLR_E;      // CTRL_SGNLS[19]
wire [2:0] OPSEL_ALU;  // CTRL_SGNLS[20]

assign LD_AR      = CTRL_SGNLS[0];
assign INR_AR     = CTRL_SGNLS[1];
assign CLR_AR     = CTRL_SGNLS[2];
assign LD_PC      = CTRL_SGNLS[3];
assign INR_PC     = CTRL_SGNLS[4];
assign CLR_PC     = CTRL_SGNLS[5];
assign LD_DR      = CTRL_SGNLS[6];
assign INR_DR     = CTRL_SGNLS[7];
assign CLR_DR     = CTRL_SGNLS[8];
assign LD_AC      = CTRL_SGNLS[9];
assign INR_AC     = CTRL_SGNLS[10];
assign CLR_AC     = CTRL_SGNLS[11];
assign LD_IR      = CTRL_SGNLS[12];
assign LD_TR      = CTRL_SGNLS[13];
assign INR_TR     = CTRL_SGNLS[14];
assign CLR_TR     = CTRL_SGNLS[15];
assign MEM_WE     = CTRL_SGNLS[16];
assign LD_E       = CTRL_SGNLS[17];
assign CMP_E      = CTRL_SGNLS[18];
assign CLR_E      = CTRL_SGNLS[19];
assign OPSEL_ALU  = CTRL_SGNLS[20];   


// Instantiate registers
RwLRI #(.WIDTH(12)) AR (.clk(clk), .WE(LD_AR), .INC(INR_AR), .RST(CLR_AR), .DATA(BUS[11:0]), .A(w_AR));
RwLRI #(.WIDTH(12)) PC (.clk(clk), .WE(LD_PC), .INC(INR_PC), .RST(CLR_PC), .DATA(BUS[11:0]), .A(w_PC));
RwLRI #(.WIDTH(16)) DR (.clk(clk), .WE(LD_DR), .INC(INR_DR), .RST(CLR_DR), .DATA(BUS[WIDTH-1:0]), .A(w_DR));
RwLRI #(.WIDTH(16)) AC (.clk(clk), .WE(LD_AC), .INC(INR_AC), .RST(CLR_AC), .DATA(w_ALU), .A(w_AC));
RwLRI #(.WIDTH(16)) IR (.clk(clk), .WE(LD_IR), .INC(), .RST(), .DATA(BUS[WIDTH-1:0]), .A(w_IR));
RwLRI #(.WIDTH(16)) TR (.clk(clk), .WE(LD_TR), .INC(INR_TR), .RST(CLR_TR), .DATA(BUS[WIDTH-1:0]), .A(w_TR));

// Assign values to the array
assign MUX_ARRAY[0] = {4'b0, w_AR};  // Input 0: AR (extended 12-bit to 16-bit)
assign MUX_ARRAY[1] = {4'b0, w_PC};  // Input 1: PC (extended 12-bit to 16-bit)
assign MUX_ARRAY[2] = w_DR;          // Input 2: DR
assign MUX_ARRAY[3] = w_AC;          // Input 3: AC
assign MUX_ARRAY[4] = w_IR;          // Input 4: IR
assign MUX_ARRAY[5] = w_TR;          // Input 5: TR
assign MUX_ARRAY[6] = w_MEM;         // Input 6: Memory Output
assign MUX_ARRAY[7] = WRD;         // Input 7: Reserved (default 0)

// Instantiate memory
mux8to1 bus_mux(
.MUX_INPUT(MUX_ARRAY),
.SELECT(BUS_SEL), 
.MUX_OUT(BUS)
);

M memory(
.clk(clk),
.WE(WE_MEM),
.IN_ADF(w_AR),
.W_DATA(BUS[WIDTH-1:0]),
.R_DATA(w_MEM)
);

ALU alu(
.AC(w_AC),
.DR(w_DR),
.RESULT(w_ALU),
.CNTRL_E(w_CNTRL_E),
.E(w_E),
.OPSEL(OPSEL_ALU),
.CO(),
.Z(),
.N(),
.OVF()
); 

E_FF e_ff(
.clk(clk),
.CNTRL_E(w_CNTRL_E),
.LOAD(LD_E),           
.CMP(CMP_E),       
.RST(CLR_E),   
.E(w_E)  
);

endmodule
