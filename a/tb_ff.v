// D Flip-Flop Testbench
`timescale 1ns / 1ps

module tb_ff;

    // Testbench signal declarations
    reg clk;
    reg rst;
    reg d;
    wire q;
    
    // Clock period (10ns = 100MHz)
    parameter CLK_PERIOD = 10;
    
    // DUT (Device Under Test) instance
    ff dut (
        .clk(clk),
        .rst(rst),
        .d(d),
        .q(q)
    );
    
    // Clock generation
    initial begin
        clk = 0;
        forever #(CLK_PERIOD/2) clk = ~clk;
    end
    
    // VCD waveform dump setup
    initial begin
        $dumpfile("ff_sim.vcd");
        $dumpvars(0, tb_ff);
    end
    
    // Test scenario
    initial begin
        // Initialization
        $display("=== D Flip-Flop Simulation Start ===");
        $display("Time\tCLK\tRST\tD\tQ");
        $monitor("%0t\t%b\t%b\t%b\t%b", $time, clk, rst, d, q);
        
        // Initial value setup
        rst = 1;
        d = 0;
        
        // Reset test (asynchronous reset)
        #15;
        $display("\n--- Asynchronous Reset Test ---");
        rst = 1;
        d = 1;  // Reset takes priority even when data is 1
        #20;
        
        // Normal operation test after reset release
        $display("\n--- Normal Operation Test ---");
        rst = 0;
        
        // Test case 1: d = 0 -> q = 0
        #5;
        d = 0;
        #20;
        
        // Test case 2: d = 1 -> q = 1
        d = 1;
        #20;
        
        // Test case 3: d = 0 -> q = 0
        d = 0;
        #20;
        
        // Test case 4: Continuous data changes
        $display("\n--- Continuous Data Change Test ---");
        repeat(8) begin
            d = $random;
            #10;
        end
        
        // Reset during operation test
        $display("\n--- Reset During Operation Test ---");
        d = 1;
        #10;
        rst = 1;  // Reset during operation
        #10;
        rst = 0;
        #10;
        
        // End simulation
        #50;
        $display("\n=== Simulation Complete ===");
        $finish;
    end
    
    // Variables for functional verification
    reg prev_d;
    reg verification_active;
    
    // Functional verification through assertions
    initial begin
        verification_active = 0;
        
        // Reset operation verification
        wait(rst == 1);
        #1;
        if (q !== 1'b0) begin
            $error("Reset Error: q is not 0. q = %b", q);
        end else begin
            $display("Reset operation verified");
        end
        
        // Preparation for normal operation verification
        wait(rst == 0);
        #1;
        verification_active = 1;
        $display("Starting flip-flop operation verification");
    end
    
    // Perform verification at every clock edge
    always @(posedge clk) begin
        if (verification_active && !rst) begin
            #1;  // Wait briefly after clock edge for output stabilization
            if (q !== prev_d) begin
                $display("Warning: Expected q=%b, got q=%b at time %0t", prev_d, q, $time);
            end
        end
        
        if (!rst) begin
            prev_d = d;  // Store current d value for next clock
        end
    end
    
    // Verification completion message
    initial begin
        #200;  // After sufficient time
        if (verification_active) begin
            $display("D Flip-flop operation verification completed");
        end
    end

endmodule
