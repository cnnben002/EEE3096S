//CNNBEN002 & ANTNOA001
//17/10/2021

module alu_tb();

reg clk;       //Clock 
reg[7:0] A,B;  //Inputs A and B
reg[3:0] Sel;  //Input selector
wire[7:0] Out; //ALU out

integer i;     //Declaring an integer for 'for' loop 
  
alu test(
  	clk,       // Clock 
    A,B,       // ALU 8-bit Inputs
  	Sel,       // ALU Selection
  	Out        // ALU 8-bit Output
);
  
initial 
  	begin
        A = 8'b00000101;  //Setting A value
  		B = 8'b00000010;  //Setting B value
  		Sel = 4'b0000;    //Setting selector value
      	clk = 1'b1;       //Setting clock value
      
        $display("A = ", A, " = b%b", A);          //Displaying A
        $display("B = ", B, " = b%b", B);          //Displaying B
        $display("\n");
        $monitor("Selector = b%b", Sel,
               "\tOutput = ", Out, " = b%b", Out);  //Monitoring the output
      
        for (i=0;i<15;i=i+1) begin  //for loop to cycle through selector
            #5;
          	clk=!clk;           //Invert clock
   			#5;
          	clk=!clk;           //Invert clock 
            Sel = Sel + 8'h01;  //Increase selector value
  		end
        //$dumpfile("dump.vcd"); 
        //$dumpvars(1);
 	end
endmodule
