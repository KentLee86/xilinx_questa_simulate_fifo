// axis_master_file_v2.sv
`timescale 1ns/1ps

module axis_master_file_v2 #(
  parameter string  FILE_PATH     = "data.csv",  // 초기 로드 파일
  parameter string  FILE_TYPE     = "csv",       // "csv" | "bin"
  parameter bit     LITTLE_ENDIAN = 1'b1,
  parameter int     DATA_BYTES    = 4            // 32b 고정
)(
  input  logic        aclk,
  input  logic        aresetn,

  // ---- 런타임 제어 입력 ----
  input  logic        i_start,        // 원샷 발사(즉시 0번부터 전송)
  input  logic        i_loop,         // 1=루프 모드, 0=원샷 모드 (언제든 변경 가능)
  input  logic        i_restart,      // 전송 중/대기 중 관계없이 인덱스 0으로 리와인드
  input  logic        i_pause,        // 1=일시정지(핸드셰이크 중단), 0=재개
  input  logic [31:0] i_gap_cycles,   // 워드 간 삽입 갭 사이클(런타임 반영)
  input  logic        i_reload,       // 파일 재로드(현재 FILE_PATH에서 다시 읽기)

  // ---- 상태 모니터링 출력 ----
  output logic        o_busy,         // 전송 중(핸드셰이크 진행 포함)
  output logic        o_done_pulse,   // 원샷 완료 시 1클럭 펄스
  output logic [31:0] o_sent_count,   // 누적 전송 워드 수(프레임 기준으로는 완료 후 리셋됨)

  // ---- AXI4-Stream master ----
  output logic [31:0] m_axis_tdata,
  output logic        m_axis_tvalid,
  input  logic        m_axis_tready,
  output logic [3:0]  m_axis_tkeep,
  output logic        m_axis_tlast
);
  typedef bit [31:0] word_t;
  word_t q[$];            // 파일에서 읽은 워드 큐
  int unsigned idx;       // 현재 전송 인덱스
  int unsigned gap_cnt;   // 갭 카운터

  // -------- 파일 로더 --------
  function void load_csv(string path);
    int fd; string line; word_t w;
    q.delete();
    fd = $fopen(path, "r");
    if (!fd) $fatal(1, "[axis_v2] CSV open fail: %s", path);
    while (!$feof(fd)) begin
      line = "";
      void'($fgets(line, fd));
      if ($sscanf(line, "%h", w) == 1)      q.push_back(w);
      else if ($sscanf(line, "%d", w) == 1) q.push_back(w);
    end
    $fclose(fd);
    $display("[axis_v2] CSV loaded: %0d words", q.size());
  endfunction

  function void load_bin(string path, bit little_endian);
    int fd; int r; byte buf[$]; byte tmp[4096];
    q.delete();
    fd = $fopen(path, "rb");
    if (!fd) $fatal(1, "[axis_v2] BIN open fail: %s", path);
    do begin
      r = $fread(tmp, fd);
      for (int i=0;i<r;i++) buf.push_back(tmp[i]);
    end while (r == tmp.size());
    $fclose(fd);
    if (DATA_BYTES != 4)  $fatal(1, "DATA_BYTES must be 4 for 32b.");
    int words = buf.size()/DATA_BYTES;
    for (int i=0;i<words;i++) begin
      int base = i*4; word_t w;
      if (little_endian) w = {buf[base+3],buf[base+2],buf[base+1],buf[base+0]};
      else               w = {buf[base+0],buf[base+1],buf[base+2],buf[base+3]};
      q.push_back(w);
    end
    if ((buf.size()%4)!=0)
      $display("[axis_v2] WARN trailing %0d byte(s) ignored", buf.size()%4);
    $display("[axis_v2] BIN loaded: %0d words", q.size());
  endfunction

  task automatic reload_file();
    if (FILE_TYPE == "csv")      load_csv(FILE_PATH);
    else if (FILE_TYPE == "bin") load_bin(FILE_PATH, LITTLE_ENDIAN);
    else $fatal(1, "Unknown FILE_TYPE: %s", FILE_TYPE);
  endtask

  // -------- 초기화/리로드 트리거 --------
  // i_reload는 언제든 펄스 주면 즉시 재적재(전송 중이면 다음 전송부터 새 데이터 사용)
  // 안전하게 쓰려면 i_pause=1로 멈춘 뒤 i_reload→i_restart→i_pause=0 순서를 추천
  always @(posedge aclk) if (aresetn && i_reload) begin
    reload_file();
    idx <= 0;
  end

  // -------- 메인 시퀀서(FSM-less, 명시적 가드) --------
  typedef enum logic [1:0] {IDLE, SEND, GAP} state_t;
  state_t state;

  // 기본 출력
  always_comb begin
    m_axis_tkeep = 4'hF;
  end

  // 동작
  always_ff @(posedge aclk or negedge aresetn) begin
    if (!aresetn) begin
      state         <= IDLE;
      m_axis_tdata  <= '0;
      m_axis_tvalid <= 1'b0;
      m_axis_tlast  <= 1'b0;
      o_busy        <= 1'b0;
      o_done_pulse  <= 1'b0;
      o_sent_count  <= 32'd0;
      idx           <= 0;
      gap_cnt       <= 0;
      // 첫 로드
      // 주: 시뮬레이터마다 reset 시 파일 접근 타이밍 차이가 있을 수 있어요.
      // 필요하면 testbench에서 reset 해제 후 i_reload=1 펄스로 동작하세요.
    end else begin
      o_done_pulse <= 1'b0;

      // 즉시 리와인드(언제든)
      if (i_restart) begin
        idx          <= 0;
        state        <= IDLE;
        m_axis_tvalid<= 1'b0;
        m_axis_tlast <= 1'b0;
        gap_cnt      <= 0;
        o_busy       <= 1'b0;
      end

      case (state)
        IDLE: begin
          m_axis_tvalid <= 1'b0;
          m_axis_tlast  <= 1'b0;
          o_busy        <= 1'b0;
          gap_cnt       <= 0;

          // 원샷 트리거
          if (i_start && q.size()>0) begin
            idx   <= 0;
            state <= SEND;
            o_busy<= 1'b1;
          end
          // 루프 모드 즉시 송신(시작 신호 없이도 계속 돌리고 싶다면 아래 주석 해제)
          else if (i_loop && q.size()>0) begin
            // idx 유지: 루프 재개 지점에서 이어감. 완전 처음부터 원하면 i_restart와 함께 사용
            state <= SEND;
            o_busy<= 1'b1;
          end
        end

        SEND: begin
          o_busy <= 1'b1;

          // 일시정지
          if (i_pause) begin
            m_axis_tvalid <= 1'b0;
            m_axis_tlast  <= 1'b0;
          end
          else begin
            // 현재 워드 준비
            m_axis_tdata  <= q[idx];
            m_axis_tvalid <= 1'b1;
            m_axis_tlast  <= (idx == q.size()-1);

            // 핸드셰이크 완료?
            if (m_axis_tvalid && m_axis_tready) begin
              o_sent_count <= o_sent_count + 1;
              // 마지막 워드였나?
              if (idx == q.size()-1) begin
                // 모드에 따라 분기
                if (i_loop) begin
                  idx           <= 0;
                  m_axis_tvalid <= 1'b0;
                  m_axis_tlast  <= 1'b0;
                  // 갭 적용
                  gap_cnt       <= (i_gap_cycles==0)?0:i_gap_cycles-1;
                  state         <= (i_gap_cycles==0) ? SEND : GAP;
                end else begin
                  // 원샷 완료
                  m_axis_tvalid <= 1'b0;
                  m_axis_tlast  <= 1'b0;
                  o_done_pulse  <= 1'b1;
                  state         <= IDLE;
                end
              end
              else begin
                // 다음 워드로 진행
                idx           <= idx + 1;
                m_axis_tvalid <= 1'b0;    // 다음 사이클에 재어설트
                m_axis_tlast  <= 1'b0;
                // 갭 적용
                gap_cnt       <= (i_gap_cycles==0)?0:i_gap_cycles-1;
                state         <= (i_gap_cycles==0) ? SEND : GAP;
              end
            end
          end
        end

        GAP: begin
          // 갭 카운트 소모 (i_pause가 걸리면 그냥 정지된 상태 유지)
          if (!i_pause) begin
            if (gap_cnt == 0) begin
              state <= SEND;
            end else begin
              gap_cnt <= gap_cnt - 1;
            end
          end
          m_axis_tvalid <= 1'b0;
          m_axis_tlast  <= 1'b0;
          o_busy        <= 1'b1;
        end
      endcase
    end
  end

  // 초기 파일 자동 로드(옵션)
  initial begin
    // 시뮬레이터에 따라 reset 이전 파일 접근이 싫다면 주석 처리하세요.
    reload_file();
  end

endmodule
