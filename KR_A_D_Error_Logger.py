from pynput import keyboard
import time

# 상태 추적 변수
a_pressed = False
d_pressed = False
start_time = None  # 동시입력
inactive_start_time = None  # 미입력

# 색상 정의
GREEN = '\033[38;2;0;255;0m'    # 녹색 (RGB: 0, 255, 0)
YELLOW = '\033[38;2;255;255;0m' # 노란색 (RGB: 255, 255, 0)
RED = '\033[38;2;255;0;0m'      # 적색 (RGB: 255, 0, 0)
RESET = '\033[0m'               # 색상 리셋

def print_duration():
    """동시입력 시간 출력 (ms 단위)"""
    global start_time
    if start_time is not None:
        duration = (time.time() - start_time) * 1000  # 초를 밀리초로 변환
        print(f"동시입력 시간: {RED}{duration:.2f}ms{RESET}")
        start_time = None  # 시간 출력 후 초기화

def print_inactive_duration():
    """미입력 시간 출력 (ms 단위)"""
    global inactive_start_time
    if inactive_start_time is not None:
        duration = (time.time() - inactive_start_time) * 1000  # 초를 밀리초로 변환
        if duration <= 120:
            print(f"미입력 시간: {GREEN}{duration:.2f}ms{RESET}")  # 녹색
        elif 120 < duration <= 600:
            print(f"미입력 시간: {YELLOW}{duration:.2f}ms{RESET}")  # 노란색
        inactive_start_time = None  # 시간 출력 후 초기화

def on_press(key):
    global a_pressed, d_pressed, start_time, inactive_start_time

    try:
        if key.char == 'a':
            a_pressed = True
            # A와 D가 동시에 눌린 경우 시간 측정 시작
            if d_pressed and start_time is None:
                start_time = time.time()
            # A 또는 D가 눌려 있을 때 시간이 측정되면 출력
            if inactive_start_time is not None:
                print_inactive_duration()

        elif key.char == 'd':
            d_pressed = True
            # A와 D가 동시에 눌린 경우 시간 측정 시작
            if a_pressed and start_time is None:
                start_time = time.time()
            # A 또는 D가 눌려 있을 때 시간이 측정되면 출력
            if inactive_start_time is not None:
                print_inactive_duration()

    except AttributeError:
        pass

def on_release(key):
    global a_pressed, d_pressed, start_time, inactive_start_time

    try:
        if key.char == 'a':
            a_pressed = False
            # 두 키가 모두 떼어진 상태에서 시간을 측정 시작
            if not d_pressed and not a_pressed and inactive_start_time is None:
                inactive_start_time = time.time()
            # A와 D가 모두 눌린 상태에서 A가 떼어졌을 때 시간을 출력
            if d_pressed and start_time is not None:
                print_duration()

        elif key.char == 'd':
            d_pressed = False
            # 두 키가 모두 떼어진 상태에서 시간을 측정 시작
            if not a_pressed and not d_pressed and inactive_start_time is None:
                inactive_start_time = time.time()
            # A와 D가 모두 눌린 상태에서 D가 떼어졌을 때 시간을 출력
            if a_pressed and start_time is not None:
                print_duration()

        # 두 키가 모두 떼어진 상태에서 시간을 출력
        if not a_pressed and not d_pressed and start_time is not None:
            print_duration()  # A와 D가 모두 떼어진 상태에서 시간을 출력

    except AttributeError:
        pass

# 키보드 리스너 설정
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
