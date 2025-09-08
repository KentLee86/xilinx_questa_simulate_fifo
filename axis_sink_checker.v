`timescale 1ns/1ps

module axis_sink_checker #(
    parameter integer DATA_W = 32,
    parameter integer KEEP_W = (DATA_W/8),
    parameter integer USER_W = 1
)(
    input  wire                 aclk,
    input  wire                 aresetn,

    input  wire                 s_axis_tvalid,
    output reg                  s_axis_tready,
    input  wire [DATA_W-1:0]    s_axis_tdata,
    input  wire [KEEP_W-1:0]    s_axis_tkeep,
    input  wire                 s_axis_tlast,
    input  wire [USER_W-1:0]    s_axis_tuser
);
    // 간단한 백프레셔: 몇 사이클마다 ready 토글
    reg [3:0] rdy_div;

    // 수신 카운터/프레임 카운터
    reg [31:0] beat_rcv;
    reg [31:0] frame_rcv;

    always @(posedge aclk) begin
        if (!aresetn) begin
            rdy_div      <= 4'd0;
            s_axis_tready<= 1'b0;
            beat_rcv     <= 32'd0;
            frame_rcv    <= 32'd0;
        end else begin
            rdy_div <= rdy_div + 1;
            // 1/2 duty로 backpressure (테스트 목적)
            s_axis_tready <= rdy_div[0];

            if (s_axis_tvalid && s_axis_tready) begin
                beat_rcv <= beat_rcv + 1;
                if (s_axis_tlast) begin
                    frame_rcv <= frame_rcv + 1;
                    // 시뮬에서 확인용: 프레임 종료 표시
                    // synthesis translate_off
                    $display("[%0t] Frame %0d received, total beats=%0d, data(last)=0x%08x keep=0x%0x user=0x%0x",
                        $time, frame_rcv, beat_rcv+1, s_axis_tdata, s_axis_tkeep, s_axis_tuser);
                    // synthesis translate_on
                    beat_rcv <= 32'd0;
                end
            end
        end
    end
endmodule
