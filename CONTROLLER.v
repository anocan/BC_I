module CONTROLLER #(
    parameter WIDTH=16,
    parameter CTRL_LNGTH = 21)
(  
    input clk,
    input [15:0] IR,
    input CO, Z, N, OVF, E_IN,
    input FGI,
    output reg [2:0] BUS_SEL, 
    output reg [2:0] CTRL_SGNLS [0:CTRL_LNGTH-1]
);

reg INR_SC, CLR_SC, CLR_R, LD_IEN, CLR_IEN;

reg [7:0] D;
wire [15:0] T;
wire [2:0] OPCODE = IR[14:12];
reg I, S, IEN, R;

initial begin
    INR_SC = 1'b0;
    CLR_R = 1'b0;
    LD_IEN = 1'b0;
    CLR_IEN = 1'b0;
    IEN = 1'b1;
    S = 1'b1;
    R = 1'b0;
    D = 8'b0;
end

// SEQUENCE COUNTER
SC sc(
.clk(clk),          
.CLR(CLR_SC),       
.INR(INR_SC),
.S(S), 
.T(T) 
);

// R Register
always @(posedge clk) begin
    if (CLR_R) R <= 0; else if((~T[0]) && (~T[1]) && (~T[2]) && IEN && FGI)    R <= 1;
end

// IEN Register
always @(posedge clk) begin
    if (CLR_IEN)
        IEN <= 1'b0;  
    else if (LD_IEN)
        IEN <= IEN + 1'b1;
end

// COMBINATONAL CONTROL LOGICS
integer i;
always @(*) begin
    BUS_SEL = 3'b000;
    INR_SC = 1'b0;
    CLR_SC = 1'b0;
    LD_IEN = 1'b0;
    CLR_IEN = 1'b0;
    CLR_R = 1'b0;

    // Clear the CTRL_SGNLS with 0s in each cycle
    for (i = 0; i < CTRL_LNGTH-1; i = i + 1) begin
        CTRL_SGNLS[i] = 3'b000;
    end
    CTRL_SGNLS[CTRL_LNGTH-1] = 3'b111;

    // INSTRUCTION CYCLE
    if (~R) begin
        // FETCH 
        case (1'b1)
            T[0]: begin // AR <- PC
                BUS_SEL = 3'b001;
                CTRL_SGNLS[0] = 1'b1;
                INR_SC = 1'b1;
            end 
            T[1]: begin // IR <- M[AR], PC <- PC + 1
                BUS_SEL = 3'b110;
                CTRL_SGNLS[4] = 1'b1;
                CTRL_SGNLS[12] = 1'b1;
                INR_SC = 1'b1;
            end
            T[2]: begin //  D0, . . . , D7 <- Decode IR(14-12), AR <- IR(11-0), I <- IR(15)
                BUS_SEL = 3'b100;
                CTRL_SGNLS[0] = 1'b1;
                I = IR[15];
                INR_SC = 1'b1;
                // DECODE 
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
        endcase
    end else begin // INTERRUPT CYCLE 
        case (1'b1)
            T[0]: begin // AR <- 0, TR <- PC
                CTRL_SGNLS[2] = 1'b1;
                BUS_SEL = 3'b001;
                CTRL_SGNLS[13] = 1'b1;
                INR_SC = 1'b1;
            end
            T[1]: begin // M[AR] <- TR, PC <- 0
                CTRL_SGNLS[5] = 1'b1;
                BUS_SEL = 3'b101;
                CTRL_SGNLS[16] = 1'b1;
                INR_SC = 1'b1;
            end
            T[2]: begin // PC <- PC + 1, IEN <- 0, R <- 0, SC <- 0
                CTRL_SGNLS[4] = 1'b1;
                CLR_IEN = 1'b1;
                CLR_R = 1'b1;
                CLR_SC = 1'b1;
            end 
            //default: 
        endcase
    end // END INTERRUPT CYCLE

    // EXECUTE
    case (1'b1)
            T[3]: begin
                // REGISTER REFERENCE (NO I/O OPERATION ASSUMED)
                if (D[7] && S && ~I) begin // SC <- 0, 
                    CLR_SC = 1'b1;
                    case (1'b1)
                        IR[11]: CTRL_SGNLS[11] = 1'b1; // AC <- 0
                        IR[10]: CTRL_SGNLS[19] = 1'b1; // E <- 0
                        IR[9]: begin // AC <- AC'
                            CTRL_SGNLS[9]  = 1'b1;
                            CTRL_SGNLS[20] = 3'b011;
                        end
                        IR[8]: CTRL_SGNLS[18] = 1'b1; // E <- E'
                        IR[7]: begin // AC <- {shl[AC], E}  
                            CTRL_SGNLS[9] = 1'b1;
                            CTRL_SGNLS[20] = 3'b100; 
                        end
                        IR[6]: begin // AC <- {E, shl[AC]}  
                            CTRL_SGNLS[9] = 1'b1;
                            CTRL_SGNLS[20] = 3'b101; 
                        end
                        IR[5]: CTRL_SGNLS[10] = 1'b1; // AC <- AC + 1
                        IR[4]: begin // if (AC(15) === 0) then PC <- PC + 1
                            CTRL_SGNLS[20] = 3'b011;
                            if (N) CTRL_SGNLS[4] = 1'b1;
                        end
                        IR[3]: begin // if (AC(15) === 1) then PC <- PC + 1
                            CTRL_SGNLS[20] = 3'b011;
                            if (~N) CTRL_SGNLS[4] = 1'b1;
                        end
                        IR[2]: begin // if (AC === 0) then PC <- PC + 1
                            CTRL_SGNLS[20] = 3'b011;
                            if (~Z) CTRL_SGNLS[4] = 1'b1;
                        end
                        IR[1]: if (~E_IN) begin // if (E === 0) then PC <- PC + 1
                            CTRL_SGNLS[4] = 1'b1;
                        end
                        IR[0]: S = 0; // S <- 0
                        //default: 
                    endcase
                end
                // INTERRUPT ENABLE/DISABLE 
                else if (D[7] && S && I) begin
                    CLR_SC = 1'b1;
                    case (1'b1)
                        IR[7]: LD_IEN = 1'b1; // IEN <- 1
                        IR[6]: CLR_IEN = 1'b1; // IEN <- 0
                    endcase
                end
                // MEMORY REFERENCE
                else if (~D[7] && S) begin
                    INR_SC = 1'b1;
                    if (I) begin // INDIRECT AR <- M[AR]
                        BUS_SEL = 3'b110;
                        CTRL_SGNLS[0] = 1'b1;
                    end 
                end
            end
            T[4]: begin
                case (1'b1)
                    D[0]: begin // AND: DR <- M[AR]
                        INR_SC = 1'b1;
                        BUS_SEL = 3'b110;
                        CTRL_SGNLS[6] = 1'b1;
                    end
                    D[1]: begin // ADD: DR <- M[AR]
                        INR_SC = 1'b1;
                        BUS_SEL = 3'b110;
                        CTRL_SGNLS[6] = 1'b1;                  
                    end
                    D[2]: begin // LDA: DR <- M[AR]
                        INR_SC = 1'b1;
                        BUS_SEL = 3'b110;
                        CTRL_SGNLS[6] = 1'b1;                  
                    end
                    D[3]: begin // STA: M[AR] <- AC, SC <- 0
                        CLR_SC = 1'b1;
                        BUS_SEL = 3'b011;
                        CTRL_SGNLS[16] = 1'b1; 
                    end
                    D[4]: begin // BUN: PC <- AR, SC <- 0
                        CLR_SC = 1'b1;
                        BUS_SEL = 3'b000;
                        CTRL_SGNLS[3] = 1'b1; 
                    end
                    D[5]: begin // BSA: M[AR] <- PC, AR <- AR + 1
                        INR_SC = 1'b1;
                        BUS_SEL = 3'b001;
                        CTRL_SGNLS[1] = 1'b1;
                        CTRL_SGNLS[16] = 1'b1;
                    end
                    D[6]: begin // ISZ: DR <- M[AR]
                        INR_SC = 1'b1;
                        BUS_SEL = 3'b110;
                        CTRL_SGNLS[6] = 1'b1;                 
                    end 
                    //default: 
                endcase
            end
            T[5]: begin
                case (1'b1)
                    D[0]: begin // AND: AC <- AC ∧ DR, SC <- 0
                        CLR_SC = 1'b1;
                        CTRL_SGNLS[9] = 1'b1;
                        CTRL_SGNLS[20] = 3'b001;
                    end
                    D[1]: begin // ADD: AC <- AC + DR, E <- CO, SC <- 0
                        CLR_SC = 1'b1;
                        CTRL_SGNLS[9] = 1'b1;
                        CTRL_SGNLS[20] = 3'b000;
                    end 
                    D[2]: begin // LDA: AC <- DR, SC <- 0
                        CLR_SC = 1'b1;
                        CTRL_SGNLS[9] = 1'b1;
                        CTRL_SGNLS[20] = 3'b010;
                    end
                    D[5]: begin // BSA: PC <- AR, SC <- 0
                        CLR_SC = 1'b1;
                        BUS_SEL = 3'b000;
                        CTRL_SGNLS[3] = 1'b1;
                    end
                    D[6]: begin // ISZ: DR <- DR + 1
                        INR_SC = 1'b1;
                        CTRL_SGNLS[7] = 1'b1;
                    end
                    //default: 
                endcase            
            end
            T[6]: begin
                case (1'b1)
                    D[6]: begin // ISZ: M[AR] <- DR, if (DR==0): PC <- PC + 1, SC <- 0
                        CLR_SC = 1'b1;
                        BUS_SEL = 3'b010;
                        CTRL_SGNLS[16] = 1'b1;
                        CTRL_SGNLS[20] = 3'b010;
                        if (Z) CTRL_SGNLS[4] = 1'b1;
                    end 
                    //default: 
                endcase
            end
            //default: 
    endcase
end

endmodule
