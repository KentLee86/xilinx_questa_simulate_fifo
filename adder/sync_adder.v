`timescale 1ns / 1ps
// 동기 가산기 (Synchronous Adder)
// 클럭에 동기화되어 두 입력을 더하는 모듈

module sync_adder #(
    parameter WIDTH = 8  // 데이터 폭
)(
    input  wire                clk,      // 클럭 신호
    input  wire                rst_n,    // 리셋 신호 (active low)
    input  wire                enable,   // 인에이블 신호
    input  wire [WIDTH-1:0]    a,        // 첫 번째 입력
    input  wire [WIDTH-1:0]    b,        // 두 번째 입력
    output reg  [WIDTH:0]      sum,      // 출력 (캐리 포함)
    output reg                 valid     // 출력 유효 신호
);

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            sum   <= {(WIDTH+1){1'b0}};
            valid <= 1'b0;
        end else if (enable) begin
            sum   <= a + b;
            valid <= 1'b1;
        end else begin
            valid <= 1'b0;
        end
    end

endmodule
