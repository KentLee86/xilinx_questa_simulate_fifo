// D Flip-Flop Module
module ff (
    input wire clk,    // Clock signal
    input wire rst,    // Reset signal (asynchronous)
    input wire d,      // Data input
    output reg q       // Data output
);

    // D flip-flop with asynchronous reset
    always @(posedge clk or posedge rst) begin
        if (rst) begin
            q <= 1'b0;  // Initialize output to 0 on reset
        end else begin
            q <= d;     // Transfer input to output on clock rising edge
        end
    end

endmodule
