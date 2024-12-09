from pynput import keyboard
import time

# 키 상태를 저장할 변수
key_status = {"A": False, "D": False}
key_times = {"A": None, "D": None}
simultaneous_time = 0  # A와 D가 동시에 눌린 시간
inactive_time = 0  # A와 D가 동시에 눌리지 않은 시간
last_event_time = time.perf_counter()  # 마지막 이벤트 시간 (초 단위)
braking_started = False  # 브레이킹 시작 여부

# ANSI escape codes for colors
RED = '\033[91m'  # 빨간색
GREEN = '\033[92m'  # 녹색
RESET = '\033[0m'  # 기본 색상

# 로그 기록 함수 (색상 추가)
def log_event(event, color=RESET, blank_line=False):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"{color}[{timestamp}] {event}{RESET}")
    if blank_line:  # 줄 간격을 두고 출력하려면 빈 줄 추가
        print()

# A와 D 키가 동시에 눌린 시간 계산 및 출력 함수
def analyze_times():
    global simultaneous_time, inactive_time, last_event_time, braking_started

    # A와 D가 동시에 눌린 상태일 때 (브레이킹 상태)
    if key_status["A"] and key_status["D"]:
        if not braking_started:
            braking_started = True  # 브레이킹 시작
        simultaneous_time += time.perf_counter() - last_event_time  # 경과 시간 추가
        last_event_time = time.perf_counter()  # 현재 시간을 마지막 이벤트 시간으로 갱신
        log_event(f"Both 'A' and 'D' keys are pressed.", RED, blank_line=True)  # 빨간색 출력 후 간격 추가

    # A와 D가 모두 입력되지 않았을 때 (브레이킹 후 멈춤 상태)
    elif not key_status["A"] and not key_status["D"]:
        if braking_started:  # 브레이킹 상태에서 둘 다 입력되지 않았을 때
            inactive_time = time.perf_counter() - last_event_time  # 경과 시간 추가 (누적하지 않음)
            last_event_time = time.perf_counter()  # 현재 시간을 마지막 이벤트 시간으로 갱신
            log_event(f"Both 'A' and 'D' are not pressed. Inactive time: {inactive_time:.2f} seconds.", GREEN, blank_line=True)  # 초 단위 출력 후 간격 추가
        braking_started = False  # 브레이킹 상태 종료

# 키 눌림 처리
def on_press(key):
    try:
        if key.char.upper() in key_status:
            if not key_status[key.char.upper()]:  # 키가 처음 눌린 경우
                key_status[key.char.upper()] = True
                key_times[key.char.upper()] = time.perf_counter()

            # 타이밍 분석
            analyze_times()

    except AttributeError:
        pass

# 키 해제 처리
def on_release(key):
    try:
        if key.char.upper() in key_status:
            if key_status[key.char.upper()]:  # 키가 눌린 상태에서 해제된 경우
                key_status[key.char.upper()] = False
                duration = time.perf_counter() - key_times[key.char.upper()]
                log_event(f"'{key.char.upper()}' key released. Duration: {duration:.2f} seconds.", RESET)  # 초 단위 출력

                key_times[key.char.upper()] = None

            # A와 D 키가 동시에 해제되었을 때
            if not key_status["A"] and not key_status["D"]:
                log_event("Both 'A' and 'D' keys are released.", RESET, blank_line=False)  # 간격 없이 기본 색상 출력
                # 타이밍 분석
                analyze_times()

    except AttributeError:
        pass

# 키보드 리스너 설정
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    print("Key listener started. Press ESC to exit.")
    listener.join()
