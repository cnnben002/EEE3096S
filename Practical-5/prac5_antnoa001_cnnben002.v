//CNNBEN002 & ANTNOA001
//17/10/2021

module alu (
  	input clk,            //Creating a clock 
    input [7:0] A,B,      //Create two 8-bit inputs                 
    input [3:0] Sel,      //Create 4-bit selection
  	output reg [7:0] Out  //Create 8-bit output
);
  
  
reg [7:0] Acc;       //Defining accumulator register
  
  always @(posedge clk)   //On positive clock edge
	begin
		case(Sel)
   			4'b0000: Acc = A+B;                  //ADD
   			4'b0001: Acc = A-B;                  //SUB
   			4'b0010: Acc = A*B;                  //MUL
   			4'b0011: Acc = A/B;                  //DIV
   			4'b0100: Acc = Acc+A;                //ADDA
   			4'b0101: Acc = Acc*A;                //MULA
            4'b0110: Acc = Acc+(A*B);            //MAC
            4'b0111: Acc = {A[6:0], A[7]};       //ROL
            4'b1000: Acc = {A[0], A[7:1]};       //ROR
   			4'B1001: Acc = A&B;                    //AND
   			4'b1010: Acc = A|B;                    //OR
   			4'b1011: Acc = A^B;                    //XOR
            4'b1100: Acc = ~(A&B);                 //NAND
            4'b1101: Acc = (A==B)?8'b11111111:8'b0;   //ETH
            4'b1110: Acc = (A>B)?8'b11111111:8'b0;    //GTH
            4'b1111: Acc = (A<B)?8'b11111111:8'b0;    //LTH
    
   			default: Acc = 8'b0;      // Setting default case
  		endcase   
    	Out <= Acc;  //Setting the accumulator value to output
 	end
endmodule
