// 동기 가산기 테스트벤치 (대안 버전 - 더 확실한 종료)
`timescale 1ns / 1ps

module tb_sync_adder_alt;

    // 파라미터
    parameter WIDTH = 8;
    parameter CLK_PERIOD = 10; // 10ns 클럭 주기 (100MHz)
    parameter SIM_TIME = 1000; // 시뮬레이션 시간 (ns)

    // 신호 선언
    reg                 clk;
    reg                 rst_n;
    reg                 enable;
    reg  [WIDTH-1:0]    a;
    reg  [WIDTH-1:0]    b;
    wire [WIDTH:0]      sum;
    wire                valid;

    // 시뮬레이션 제어
    reg sim_done = 0;

    // DUT (Device Under Test) 인스턴스
    sync_adder #(
        .WIDTH(WIDTH)
    ) dut (
        .clk(clk),
        .rst_n(rst_n),
        .enable(enable),
        .a(a),
        .b(b),
        .sum(sum),
        .valid(valid)
    );

    // 클럭 생성 (시뮬레이션 완료 시 자동 중지)
    initial begin
        clk = 0;
        while (!sim_done) begin
            #(CLK_PERIOD/2) clk = ~clk;
        end
    end

    // 시뮬레이션 타임아웃 (안전장치)
    initial begin
        #SIM_TIME;
        if (!sim_done) begin
            $display("WARNING: 시뮬레이션 타임아웃 - 강제 종료");
            sim_done = 1;
            #10;
            $finish;
        end
    end

    // 테스트 시나리오
    initial begin
        // 초기화
        rst_n = 0;
        enable = 0;
        a = 0;
        b = 0;

        // VCD 파일 생성 (파형 덤프)
        $dumpfile("sync_adder.vcd");
        $dumpvars(0, tb_sync_adder_alt);

        $display("=== 동기 가산기 시뮬레이션 시작 ===");

        // 리셋 해제
        #(CLK_PERIOD * 2);
        rst_n = 1;
        
        // 테스트 케이스 1: 기본 덧셈
        #(CLK_PERIOD);
        enable = 1;
        a = 8'd15;
        b = 8'd25;
        #(CLK_PERIOD);
        $display("Test 1: %d + %d = %d, valid = %b", a, b, sum, valid);

        // 테스트 케이스 2: 오버플로우 테스트
        #(CLK_PERIOD);
        a = 8'd200;
        b = 8'd100;
        #(CLK_PERIOD);
        $display("Test 2: %d + %d = %d, valid = %b", a, b, sum, valid);

        // 테스트 케이스 3: enable 비활성화
        #(CLK_PERIOD);
        enable = 0;
        a = 8'd50;
        b = 8'd50;
        #(CLK_PERIOD);
        $display("Test 3 (disabled): %d + %d = %d, valid = %b", a, b, sum, valid);

        // 테스트 케이스 4: enable 재활성화
        #(CLK_PERIOD);
        enable = 1;
        #(CLK_PERIOD);
        $display("Test 4 (re-enabled): %d + %d = %d, valid = %b", a, b, sum, valid);

        // 테스트 케이스 5: 0 + 0
        #(CLK_PERIOD);
        a = 8'd0;
        b = 8'd0;
        #(CLK_PERIOD);
        $display("Test 5: %d + %d = %d, valid = %b", a, b, sum, valid);

        // 테스트 케이스 6: 최대값 테스트
        #(CLK_PERIOD);
        a = 8'd255;
        b = 8'd255;
        #(CLK_PERIOD);
        $display("Test 6: %d + %d = %d, valid = %b", a, b, sum, valid);

        // 리셋 테스트
        #(CLK_PERIOD);
        rst_n = 0;
        #(CLK_PERIOD);
        $display("Reset test: sum = %d, valid = %b", sum, valid);

        // 시뮬레이션 완료
        #(CLK_PERIOD * 2);
        $display("=== 시뮬레이션 완료 ===");
        
        // 시뮬레이션 종료
        sim_done = 1;
        #10; // 클럭이 완전히 멈출 때까지 대기
        $finish;
    end

    // 클럭 에지에서 출력 모니터링
    always @(posedge clk) begin
        if (rst_n && valid && !sim_done) begin
            $display("시간 %0t: %d + %d = %d", $time, a, b, sum);
        end
    end

endmodule
