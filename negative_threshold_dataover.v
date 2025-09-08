`timescale 1ns/1ps

module negative_threshold_dataover (
    input  wire signed [31:0] data_in,           // 32-bit signed input data
    output wire               data_over_neg100,  // output: 1 if data_in > -100, 0 otherwise
    output wire               data_over_neg50    // output: 1 if data_in > -50, 0 otherwise
);

    // Fixed negative thresholds
    localparam signed [31:0] THRESHOLD_NEG100 = -32'sd100;
    localparam signed [31:0] THRESHOLD_NEG50  = -32'sd50;

    // Instantiate first dataover module for comparison with -100
    dataover dataover_inst_neg100 (
        .data_in(data_in),
        .threshold(THRESHOLD_NEG100),
        .data_over(data_over_neg100)
    );

    // Instantiate second dataover module for comparison with -50
    dataover dataover_inst_neg50 (
        .data_in(data_in),
        .threshold(THRESHOLD_NEG50),
        .data_over(data_over_neg50)
    );

endmodule
