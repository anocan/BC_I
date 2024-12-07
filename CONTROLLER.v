module CONTROLLER #(
    parameter WIDTH=16,
    parameter CTRL_LNGTH = 20)
(  
    input clk,
    input [15:0] IR,
    output reg [2:0] BUS_SEL, 
    output reg [CTRL_LNGTH-1:0] CTRL_SGNLS
);

reg INR_SC, CLR_SC;

reg [7:0] D;
wire [15:0] T;
wire [2:0] OPCODE = IR[14:12];
reg I;

initial begin
    INR_SC = 1'b0;
end

// DECODER
always @(*) begin
    D = 8'b0;
    case (OPCODE)
       3'b000:  D[0] = 1'b1;
       3'b001:  D[1] = 1'b1;
       3'b010:  D[2] = 1'b1;
       3'b011:  D[3] = 1'b1;
       3'b100:  D[4] = 1'b1;
       3'b101:  D[5] = 1'b1;
       3'b110:  D[6] = 1'b1;
       3'b111:  D[7] = 1'b1;
        default: D = 8'b0;
    endcase
end

// SEQUENCE COUNTER
SC sc(
.clk(clk),          
.CLR(CLR_SC),       
.INR(INR_SC),    
.T(T) 
);

// COMBINATONAL CONTROL LOGICS

always @(*) begin
    BUS_SEL = 3'b000;
    CTRL_SGNLS = 16'b0;
    INR_SC = 1'b0;

    // FETCH
    case (1'b1)
        T[0]: begin // AR <- PC
            BUS_SEL = 3'b001;
            CTRL_SGNLS[0] = 1'b1;
            INR_SC = 1'b1;
        end 
        T[1]: begin // IR <- M[AR], PC <- PC + 1
            BUS_SEL = 3'b110;
            CTRL_SGNLS[12] = 1'b1;
            CTRL_SGNLS[4] = 1'b1;
            INR_SC = 1'b1;
        end
        T[2]: begin //  D0, . . . , D7 <- Decode IR(14-12), AR <- IR(11-0), I <- IR(15)
            BUS_SEL = 3'b100;
            CTRL_SGNLS[0] = 1'b1;
            I = IR[15];
            INR_SC = 1'b1;
        end
        
    // EXECUTE
        T[3]: begin
            // REGISTER REFERENCE (NO I/O OPERATION ASSUMED)
            if (D[7]) begin // SC <- 0, 
                CLR_SC = 0;
                case (1'b1)
                    IR[11]: begin
                        CTRL_SGNLS[11] = 1'b1;
                    end

                    //default: 
                endcase
            end
        end

        //default: 
    endcase
end

endmodule
