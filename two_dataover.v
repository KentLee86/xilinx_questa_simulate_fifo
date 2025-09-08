`timescale 1ns/1ps

module two_dataover (
    input  wire signed [31:0] data_in,        // 32-bit signed input data
    output wire               data_over_100,  // output: 1 if data_in > 100, 0 otherwise
    output wire               data_over_200   // output: 1 if data_in > 200, 0 otherwise
);

    // Fixed signed thresholds
    localparam signed [31:0] THRESHOLD_100 = 32'sd100;
    localparam signed [31:0] THRESHOLD_200 = 32'sd200;

    // Instantiate first dataover module for comparison with 100
    dataover dataover_inst_100 (
        .data_in(data_in),
        .threshold(THRESHOLD_100),
        .data_over(data_over_100)
    );

    // Instantiate second dataover module for comparison with 200
    dataover dataover_inst_200 (
        .data_in(data_in),
        .threshold(THRESHOLD_200),
        .data_over(data_over_200)
    );

endmodule
