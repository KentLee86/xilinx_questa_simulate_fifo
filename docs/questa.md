
## Questa 설치 작업

![alt text](enter_setting.png)

![alt text](path_setting.png)

## 시뮬레이션 라이브러리 컴파일 방법

- 시간 오래 걸림

![alt text](compile_sim_menu.png)

![alt text](compile_sim_library.png)


## SIM 설정
- 디버그 추가(브레이크 포인트)
- 웨이브 폼 추가
- 시뮬레이션 종료시 꺼짐 방지


```
# Compile vlog More option
+define+DEBUG

# Elaboration vopt More option
+acc=blnr -debugdb +cover=sbfec

# Simulation vsim More option
-onfinish stop
```

![alt text](sim_compile_option.png)
![alt text](sim_option_elabortion.png)
![alt text](sim_option_sim.png)