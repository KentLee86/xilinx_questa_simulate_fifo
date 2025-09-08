`timescale 1ns/1ps

module axis_fifo_example_top #(
    parameter integer DATA_W  = 32,
    parameter integer KEEP_W  = (DATA_W/8),
    parameter integer USER_W  = 1,
    parameter integer FRAME_BEATS = 8  // 한 프레임 당 비트(beat) 수
)(
    input  wire                   aclk,
    input  wire                   aresetn
);
    // AXIS 소스 → FIFO 입력
    wire                   s_tvalid, s_tready, s_tlast;
    wire [DATA_W-1:0]      s_tdata;
    wire [KEEP_W-1:0]      s_tkeep;
    wire [USER_W-1:0]      s_tuser;

    // FIFO 출력 → AXIS 싱크
    wire                   m_tvalid, m_tready, m_tlast;
    wire [DATA_W-1:0]      m_tdata;
    wire [KEEP_W-1:0]      m_tkeep;
    wire [USER_W-1:0]      m_tuser;

    // Wait done signal from counter source
    wire                   wait_done;

    // Internal tready from sink checker
    wire                   sink_tready;

    // Delayed wait_done for 2 clock cycles
    reg [1:0]              wait_done_delay;

    // 1) 프레임 생성기(소스)
    axis_counter_src #(
        .DATA_W(DATA_W),
        .KEEP_W(KEEP_W),
        .USER_W(USER_W),
        .FRAME_BEATS(FRAME_BEATS)
    ) u_src (
        .aclk(aclk),
        .aresetn(aresetn),
        .m_axis_tvalid(s_tvalid),
        .m_axis_tready(s_tready),
        .m_axis_tdata (s_tdata ),
        .m_axis_tkeep (s_tkeep ),
        .m_axis_tlast (s_tlast ),
        .m_axis_tuser (s_tuser ),
        .wait_done(wait_done)
    );

    // 2) Xilinx XPM FIFO (AXIS)
    axis_fifo_xpm #(
        .DATA_W(DATA_W),
        .KEEP_W(KEEP_W),
        .USER_W(USER_W),
        .DEPTH(1024)
    ) u_fifo (
        .aclk           (aclk),
        .aresetn        (aresetn),

        .s_axis_tvalid  (s_tvalid),
        .s_axis_tready  (s_tready),
        .s_axis_tdata   (s_tdata),
        .s_axis_tkeep   (s_tkeep),
        .s_axis_tlast   (s_tlast),
        .s_axis_tuser   (s_tuser),

        .m_axis_tvalid  (m_tvalid),
        .m_axis_tready  (m_tready),
        .m_axis_tdata   (m_tdata),
        .m_axis_tkeep   (m_tkeep),
        .m_axis_tlast   (m_tlast),
        .m_axis_tuser   (m_tuser),

        .prog_full      (),
        .prog_empty     ()
    );

    // 3) 소비자(싱크) — TREADY로 백프레셔 생성(토글)
    axis_sink_checker #(
        .DATA_W(DATA_W),
        .KEEP_W(KEEP_W),
        .USER_W(USER_W)
    ) u_sink (
        .aclk(aclk),
        .aresetn(aresetn),
        .s_axis_tvalid(m_tvalid),
        .s_axis_tready(sink_tready),
        .s_axis_tdata (m_tdata ),
        .s_axis_tkeep (m_tkeep ),
        .s_axis_tlast (m_tlast ),
        .s_axis_tuser (m_tuser )
    );

    // 2-clock delay logic for wait_done
    always @(posedge aclk) begin
        if (!aresetn) begin
            wait_done_delay <= 2'b00;
        end else begin
            wait_done_delay <= {wait_done_delay[0], ~wait_done};
        end
    end

    // Conditional tready logic: m_tready = sink_tready when wait_done goes low after 2 clocks
    // assign m_tready = wait_done_delay[1] ? sink_tready : 1'b0;
    assign m_tready = sink_tready;

endmodule
