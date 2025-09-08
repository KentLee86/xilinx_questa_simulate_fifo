// xpm_fifo_axis 기반, Vivado/Questa 모두 동작
module axis_fifo_xpm #(
    parameter integer DATA_W = 32,
    parameter integer KEEP_W = (DATA_W/8),
    parameter integer USER_W = 1,
    parameter integer DEPTH  = 1024
)(
    input  wire                 aclk,
    input  wire                 aresetn,

    // s_axis
    input  wire                 s_axis_tvalid,
    output wire                 s_axis_tready,
    input  wire [DATA_W-1:0]    s_axis_tdata,
    input  wire [KEEP_W-1:0]    s_axis_tkeep,
    input  wire                 s_axis_tlast,
    input  wire [USER_W-1:0]    s_axis_tuser,

    // m_axis
    output wire                 m_axis_tvalid,
    input  wire                 m_axis_tready,
    output wire [DATA_W-1:0]    m_axis_tdata,
    output wire [KEEP_W-1:0]    m_axis_tkeep,
    output wire                 m_axis_tlast,
    output wire [USER_W-1:0]    m_axis_tuser,

    // 선택: 상태/임계치
    output wire                 prog_full,
    output wire                 prog_empty
);

  xpm_fifo_axis #(
    // ========== 기본 설정 ==========   .CASCADE_HEIGHT(0),             // DECIMAL
   .CDC_SYNC_STAGES(2),            // DECIMAL
   .CLOCKING_MODE("common_clock"), // String
   .ECC_MODE("no_ecc"),            // String
   .EN_SIM_ASSERT_ERR("warning"),  // String
   .FIFO_DEPTH(2048),              // DECIMAL
   .FIFO_MEMORY_TYPE("auto"),      // String
   .PACKET_FIFO("false"),          // String
   .PROG_EMPTY_THRESH(10),         // DECIMAL
   .PROG_FULL_THRESH(10),          // DECIMAL
   .RD_DATA_COUNT_WIDTH(1),        // DECIMAL
   .RELATED_CLOCKS(0),             // DECIMAL
   .SIM_ASSERT_CHK(0),             // DECIMAL; 0=disable simulation messages, 1=enable simulation messages
   .TDATA_WIDTH(32),               // DECIMAL
   .TDEST_WIDTH(1),                // DECIMAL
   .TID_WIDTH(1),                  // DECIMAL
   .TUSER_WIDTH(1),                // DECIMAL
   .USE_ADV_FEATURES("1000"),      // String
   .WR_DATA_COUNT_WIDTH(1)         // DECIMAL
  ) u_xpm_fifo_axis (
    .s_aresetn               (aresetn),
    .s_aclk                  (aclk),
    .s_axis_tvalid           (s_axis_tvalid),
    .s_axis_tready           (s_axis_tready),
    .s_axis_tdata            (s_axis_tdata),
    .s_axis_tkeep            (s_axis_tkeep),
    .s_axis_tlast            (s_axis_tlast),
    .s_axis_tuser            (s_axis_tuser),
    .s_axis_tstrb            (/*unused*/),
    .s_axis_tid              (/*unused*/),
    .s_axis_tdest            (/*unused*/),

    .m_axis_tvalid           (m_axis_tvalid),
    .m_axis_tready           (m_axis_tready),
    .m_axis_tdata            (m_axis_tdata),
    .m_axis_tkeep            (m_axis_tkeep),
    .m_axis_tlast            (m_axis_tlast),
    .m_axis_tuser            (m_axis_tuser),
    .m_axis_tstrb            (/*unused*/),
    // .m_axis_tid              (/*unused*/),
    // .m_axis_tdest            (/*unused*/),

    // 상태 핀(옵션)
    .prog_full_axis               (prog_full),
    .prog_empty_axis              (prog_empty),
    // .wr_data_count           (),        // 비AXIS 카운트(미사용)
    // .rd_data_count           (),        // 비AXIS 카운트(미사용)
    .wr_data_count_axis      (),        // AXIS 기준 write 카운트
    .rd_data_count_axis      (),        // AXIS 기준 read 카운트


    .injectsbiterr_axis(1'b0),
    .injectdbiterr_axis(1'b0),

    // 비동기 모드에서만 쓰는 포트 (common_clock에서는 미사용)
    .m_aclk                  (1'b0)
    // .s_axis_tready_early     ()
  );

endmodule
