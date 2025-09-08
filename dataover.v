`timescale 1ns/1ps

module dataover (
    input  wire signed [31:0] data_in,     // 32-bit signed input data
    input  wire signed [31:0] threshold,   // 32-bit signed threshold value
    output wire               data_over    // output: 1 if data_in > threshold, 0 otherwise
);

    // Signed comparison: data_in > threshold
    assign data_over = (data_in > threshold);

endmodule
