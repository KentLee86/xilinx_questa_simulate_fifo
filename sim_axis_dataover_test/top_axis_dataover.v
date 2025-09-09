`timescale 1ns/1ps

module top_axis_dataover #(
    parameter string FILE_PATH = "test_data.csv",
    parameter string FILE_TYPE = "csv_dec",
    parameter bit LITTLE_ENDIAN = 1'b1,
    parameter int DATA_BYTES = 4,
    parameter signed [31:0] THRESHOLD = 32'd1000000
)(
    input  logic        aclk,
    input  logic        aresetn,

    // Control inputs for axis_master_file_v2
    input  logic        i_start,
    input  logic        i_loop,
    input  logic        i_restart,
    input  logic        i_pause,
    input  logic [31:0] i_gap_cycles,
    input  logic        i_reload,

    // Status outputs from axis_master_file_v2
    output logic        o_busy,
    output logic        o_done_pulse,
    output logic [31:0] o_sent_count,

    // Dataover output
    output logic        data_over
);

// Internal signals for AXI4-Stream connection
logic [31:0] m_axis_tdata;
logic        m_axis_tvalid;
logic        m_axis_tready;
logic [3:0]  m_axis_tkeep;
logic        m_axis_tlast;

// Connect AXI4-Stream master to dataover input
logic signed [31:0] data_in;
logic signed [31:0] threshold;

// Convert unsigned to signed for dataover module
assign data_in = $signed(m_axis_tdata);
assign threshold = THRESHOLD;

// AXI4-Stream master instance
axis_master_file_v2 #(
    .FILE_PATH     (FILE_PATH),
    .FILE_TYPE     (FILE_TYPE),
    .LITTLE_ENDIAN (LITTLE_ENDIAN),
    .DATA_BYTES    (DATA_BYTES)
) axis_master_inst (
    .aclk         (aclk),
    .aresetn      (aresetn),

    .i_start      (i_start),
    .i_loop       (i_loop),
    .i_restart    (i_restart),
    .i_pause      (i_pause),
    .i_gap_cycles (i_gap_cycles),
    .i_reload     (i_reload),

    .o_busy       (o_busy),
    .o_done_pulse (o_done_pulse),
    .o_sent_count (o_sent_count),

    .m_axis_tdata  (m_axis_tdata),
    .m_axis_tvalid (m_axis_tvalid),
    .m_axis_tready (m_axis_tready),
    .m_axis_tkeep  (m_axis_tkeep),
    .m_axis_tlast  (m_axis_tlast)
);

// Dataover instance
dataover dataover_inst (
    .data_in   (data_in),
    .threshold (threshold),
    .data_over (data_over)
);

// Always ready to receive data
assign m_axis_tready = 1'b1;

endmodule
