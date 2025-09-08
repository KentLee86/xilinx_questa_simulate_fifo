`timescale 1ns / 1ps

// ���� ����� �׽�Ʈ��ġ

module tb_sync_adder;

    // �Ķ����
    parameter WIDTH = 8;
    parameter CLK_PERIOD = 10; // 10ns Ŭ�� �ֱ� (100MHz)

    // ��ȣ ����
    reg                 clk;
    reg                 rst_n;
    reg                 enable;
    reg  [WIDTH-1:0]    a;
    reg  [WIDTH-1:0]    b;
    wire [WIDTH:0]      sum;
    wire                valid;

    // DUT (Device Under Test) �ν��Ͻ�
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

    // Ŭ�� ���� (���� ������ ���)
    reg clk_enable = 1;

    initial begin
        clk = 0;
        while (clk_enable) begin
            #(CLK_PERIOD/2) clk = ~clk;
        end
    end

    // �׽�Ʈ �ó�����
    initial begin
        // �ʱ�ȭ
        rst_n = 0;
        enable = 0;
        a = 0;
        b = 0;

        // VCD ���� ���� (���� ����)
        $dumpfile("sync_adder.vcd");
        $dumpvars(0);

        // ���� ����
        #(CLK_PERIOD * 2);
        rst_n = 1;

        // �׽�Ʈ ���̽� 1: �⺻ ����
        #(CLK_PERIOD);
        enable = 1;
        a = 8'd65;
        b = 8'd55;
        #(CLK_PERIOD);
        $display("Test 1: %d + %d = %d, valid = %b", a, b, sum, valid);

        // �׽�Ʈ ���̽� 2: �����÷ο� �׽�Ʈ
        #(CLK_PERIOD);
        a = 8'd200;
        b = 8'd100;
        #(CLK_PERIOD);
        $display("Test 2: %d + %d = %d, valid = %b", a, b, sum, valid);

        // �׽�Ʈ ���̽� 3: enable ��Ȱ��ȭ
        #(CLK_PERIOD);
        enable = 0;
        a = 8'd50;
        b = 8'd50;
        #(CLK_PERIOD);
        $display("Test 3 (disabled): %d + %d = %d, valid = %b", a, b, sum, valid);

        // �׽�Ʈ ���̽� 4: enable ��Ȱ��ȭ
        #(CLK_PERIOD);
        enable = 1;
        #(CLK_PERIOD);
        $display("Test 4 (re-enabled): %d + %d = %d, valid = %b", a, b, sum, valid);

        // �׽�Ʈ ���̽� 5: 0 + 0
        #(CLK_PERIOD);
        a = 8'd0;
        b = 8'd0;
        #(CLK_PERIOD);
        $display("Test 5: %d + %d = %d, valid = %b", a, b, sum, valid);

        // �׽�Ʈ ���̽� 6: �ִ밪 �׽�Ʈ
        #(CLK_PERIOD);
        a = 8'd255;
        b = 8'd255;
        #(CLK_PERIOD);
        $display("Test 6: %d + %d = %d, valid = %b", a, b, sum, valid);

        // ���� �׽�Ʈ
        #(CLK_PERIOD);
        rst_n = 0;
        #(CLK_PERIOD);
        $display("Reset test: sum = %d, valid = %b", sum, valid);

        // �ùķ��̼� ����
        #(CLK_PERIOD * 2);
        $display("�ùķ��̼� �Ϸ�");

        // Ŭ�� ���� ����
        clk_enable = 0;
        #1; // Ŭ���� ������ ���� ������ ��� ���

        $finish;
    end

    // Ŭ�� �������� ��� ����͸�
    always @(posedge clk) begin
        if (rst_n && valid) begin
            $display("�ð� %0t: %d + %d = %d", $time, a, b, sum);
        end
    end

endmodule
