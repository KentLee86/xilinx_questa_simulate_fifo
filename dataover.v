`timescale 1ns/1ps

module dataover (
    input  wire [31:0] data_in,     // 32-bit input data
    input  wire [31:0] threshold,   // 32-bit threshold value
    output wire        data_over    // output: 1 if data_in > threshold, 0 otherwise
);

    // Simple comparison: data_in > threshold
    assign data_over = (data_in > threshold);

endmodule
