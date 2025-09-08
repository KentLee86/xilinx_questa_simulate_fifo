`timescale 1ns/1ns

module tb_axis_fifo_example;

    localparam DATA_W = 32;
    localparam KEEP_W = DATA_W/8;
    localparam USER_W = 1;

    reg aclk;
    reg aresetn;

    // DUT
    axis_fifo_example_top #(
        .DATA_W(DATA_W),
        .KEEP_W(KEEP_W),
        .USER_W(USER_W),
        .FRAME_BEATS(8)
    ) dut (
        .aclk   (aclk),
        .aresetn(aresetn)
    );

    // 100 MHz
    initial begin
        aclk = 0;
        forever #5 aclk = ~aclk;
    end

    initial begin
        aresetn = 0;
        repeat(10) @(posedge aclk);
        aresetn = 1;

        // 2000ns 정도 돌려봄
        #(2000);
        $display("TB done.");
        $finish;
    end
endmodule
