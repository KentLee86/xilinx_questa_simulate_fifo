# Vivado 시뮬레이션 TCL 스크립트
# 동기 가산기 시뮬레이션 자동화

# 프로젝트 설정
set project_name "sync_adder_sim"
set project_dir "./vivado_project"

# 기존 프로젝트가 있으면 삭제
if {[file exists $project_dir]} {
    file delete -force $project_dir
}

# 새 프로젝트 생성
create_project $project_name $project_dir -part xc7a35tcpg236-1 -force

# 소스 파일 추가
add_files -norecurse {sync_adder.v}
add_files -fileset sim_1 -norecurse {tb_sync_adder.v}

# 시뮬레이션 설정
set_property top tb_sync_adder [get_filesets sim_1]
set_property top_lib xil_defaultlib [get_filesets sim_1]

# 시뮬레이션 실행 시간 설정 (1000ns)
set_property -name {xsim.simulate.runtime} -value {1000ns} -objects [get_filesets sim_1]

# 시뮬레이션 실행
launch_simulation

# 파형 창에 모든 신호 추가
add_wave {{/tb_sync_adder/dut/clk}}
add_wave {{/tb_sync_adder/dut/rst_n}}
add_wave {{/tb_sync_adder/dut/enable}}
add_wave {{/tb_sync_adder/dut/a}}
add_wave {{/tb_sync_adder/dut/b}}
add_wave {{/tb_sync_adder/dut/sum}}
add_wave {{/tb_sync_adder/dut/valid}}

# 파형 확대/축소 자동 조정
run all
zoom fit

puts "시뮬레이션 완료!"
puts "파형을 확인하려면 Vivado GUI에서 확인하세요."
puts "또는 생성된 sync_adder.vcd 파일을 GTKWave로 열어보세요."
