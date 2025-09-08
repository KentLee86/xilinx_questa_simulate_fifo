`timescale 1ns/1ps

module axis_counter_src #(
    parameter integer DATA_W = 32,
    parameter integer KEEP_W = (DATA_W/8),
    parameter integer USER_W = 1,
    parameter integer FRAME_BEATS = 8
)(
    input  wire                 aclk,
    input  wire                 aresetn,

    output reg                  m_axis_tvalid,
    input  wire                 m_axis_tready,
    output reg  [DATA_W-1:0]    m_axis_tdata,
    output reg  [KEEP_W-1:0]    m_axis_tkeep,
    output reg                  m_axis_tlast,
    output reg  [USER_W-1:0]    m_axis_tuser
);
    reg [31:0] beat_cnt;
    reg [31:0] frame_id;

    always @(posedge aclk) begin
        if (!aresetn) begin
            m_axis_tvalid <= 1'b0;
            m_axis_tdata  <= {DATA_W{1'b0}};
            m_axis_tkeep  <= {KEEP_W{1'b1}}; // 항상 유효(byte enable)
            m_axis_tlast  <= 1'b0;
            m_axis_tuser  <= {USER_W{1'b0}};
            beat_cnt      <= 32'd0;
            frame_id      <= 32'd0;
        end else begin
            // 기본적으로 전송 시도
            m_axis_tvalid <= 1'b1;

            // 데이터 패턴: {frame_id, beat_cnt}의 하위에 매핑(폭이 다르면 자동 절단)
            m_axis_tdata  <= {frame_id[15:0], beat_cnt[15:0]};
            m_axis_tuser  <= {USER_W{1'b0}}; // 필요 시 마킹

            // 프레임 끝(TLAST) 지정
            m_axis_tlast  <= (beat_cnt == (FRAME_BEATS-1));

            if (m_axis_tvalid && m_axis_tready) begin
                if (m_axis_tlast) begin
                    beat_cnt <= 32'd0;
                    frame_id <= frame_id + 1;
                end else begin
                    beat_cnt <= beat_cnt + 1;
                end
            end
        end
    end
endmodule
