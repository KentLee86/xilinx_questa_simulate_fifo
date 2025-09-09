import pandas as pd
import numpy as np


# sin 256개 데이터 생성(Q32 Fixed)
# sampling 5khz
# 500hz 1초 데이터
sample_rate = 5000
sample_time_sec = 1
sample_data = sample_time_sec * sample_rate + 1

# 500hz 1초 데이터
freq_1 = 50  # 이 값을 변경하면 다른 주파수의 1주기를 볼 수 있습니다

x = np.arange(0, sample_data)
sin_data = np.sin(x * 2 * np.pi * freq_1 / sample_rate)
sin_data = (sin_data * (2**31 - 1)).astype(int)


# sin_data = x * 10


data = pd.DataFrame({
    'data': sin_data
})


data.to_csv('data.csv', index=False, header=False)

# Hex format CSV 생성
data_hex = data.copy()
data_hex['data'] = data_hex['data'].apply(lambda x: f"0x{x:08X}")
data_hex.to_csv('data_hex.csv', index=False, header=False)


t = x / sample_rate
import matplotlib.pyplot as plt
plt.plot(t, sin_data)
plt.grid(True)
plt.savefig('sin_data.png')

# freq_1 1 사이클 데이터 확인 (1주기 = sample_rate / freq_1)
# 정확한 1주기를 위해 +1을 추가 (시작점과 끝점 모두 포함)
length = int(sample_rate / freq_1) + 1

plt.figure(figsize=(10, 5))
plt.plot(t[:length], sin_data[:length])
plt.title(f'One Cycle of {freq_1}Hz Signal (Period: {1/freq_1:.3f}s)')
plt.xlabel('Time (seconds)')
plt.ylabel('Amplitude (Q32 Fixed)')
plt.grid(True)
plt.savefig('sin_data_length.png')