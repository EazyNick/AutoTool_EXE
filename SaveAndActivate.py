# 사용자의 입력값, 시간을 계산 및 저장해서 불러오는 모듈

import time
import keyboard
from pynput.mouse import Listener
import pyautogui

# 사용자로부터 입력할 키 목록 저장
keys = []
# 키 입력 간격을 저장할 리스트
key_intervals = []
# 첫 번째 키 입력 시간 초기화
start_time = None
# 사용자로부터 입력할 마우스 클릭 좌표 저장
mouse = []
mouse_x = []
mouse_y = []

#key, moust 입력 및 클릭 시 순서를 넣을 변수, 이 모듈 내 각 함수에서 값 변경 가능. 전역변수 선언 해주었기 떄문이다.
# 원래는 함수내에서도 global Arr을 써줘야 하지만, 리스트, 딕셔너리같은 가변적인 변수들의 경우에는 안써줘도 사용이 가능하다.
Arr = []

# 저장한 내역들 실행
def perform_actions(Arr, key_intervals):

    #mouse_listener.stop()

    for i, action in enumerate(Arr):
        if isinstance(action, str):
            print("키가 동작: ", action)
            pyautogui.press(action)
        else:
            x, y = action
            print("마우스가 동작", action)
            pyautogui.moveTo(x, y)
            pyautogui.click()

        if i == len(Arr) - 1:
            pass
        else:
            time.sleep(float(key_intervals[i]))

def reset(Arr, key_intervals):

    Arr = []
    key_intervals = []
    
    return Arr, key_intervals


# 사용자 마우스 클릭 저장
def on_click(x, y, button, pressed):

    global start_time

    if pressed:
        mouse_x.append(x)
        mouse_y.append(y)
        mouse.append(button)
        if len(mouse) < 2:
        # 첫 번째 마우스 입력 시간 기록
            start_zero = 0
            start_time = time.time()
            interval = start_zero
            key_intervals.append(interval)
            print("key_intervals : ", key_intervals)
        else:
            end_time = time.time()  # 다음 키 입력 시간 기록
            interval = end_time - start_time
            key_intervals.append(interval)
            print("key_intervals : ", key_intervals)
            start_time = end_time 

        print(f"마우스 클릭: ({x}, {y}) - {button} 버튼이 눌림")
        
        # print("사용자가 누른 마우스 x좌표 : ", mouse_x)
        # print("사용자가 누른 마우스 y좌표 : ", mouse_y)
        # print("사용자가 누른 마우스 : ", mouse)

        Arr.append((x, y))
        print("순서도 : ", Arr)

# def perform_actions():
#     # 키 입력
#     for i, key in enumerate(Arr):
#         if isinstance(key, str): # key값이 문자열이라면
#             print("key가 동작 : ", key)
#             keyboard.press_and_release(key)
#             time.sleep(key_intervals[i])
#         else: 
#              # 마우스 이동 및 클릭
#             print("마우스가 동작")
#             mouse = Controller()
#             mouse.position = (key[0], key[1])
#             mouse.click(Button.left)
#             time.sleep(key_intervals[i])

# 사용자의 키 입력 감지
def key_listener(event):

    global start_time # 계속 동작시켜야 함. 지역변수로 하면 한번 동작 후 사라짐!!

    # target_key = 'a'

    # if target_key == event.name:
    #         perform_actions()
            
    if event.event_type == keyboard.KEY_DOWN:
        if len(keys) < 1:
            # 첫 번째 키 입력 시간 기록
            start_zero = 0
            start_time = time.time()
            interval = start_zero
            key_intervals.append(interval)
            print("key_intervals : ", key_intervals)
        else:
            end_time = time.time()  # 다음 키 입력 시간 기록
            interval = end_time - start_time
            key_intervals.append(interval)
            print("key_intervals : ", key_intervals)
            start_time = end_time 

        print(f"사용자가 누른 키: {event.name}")
        keys.append(event.name)

        Arr.append(event.name)
        print("순서도 : ", Arr)

def start_key_listener():
        keyboard.on_press(key_listener)
        # 프로그램이 실행 중인 동안 대기
        keyboard.wait()

# 해당 스크립트를 직접 실행할 떄만 동작        
if __name__ == "__main__":
    # 마우스 클릭 이벤트 리스너 등록
    mouse_listener = Listener(on_click=on_click) # on_click 파라미터는 마우스 클릭 이벤트가 발생했을 때 호출할 콜백 함수를 지정합니다.
    mouse_listener.start()


    # 키 입력 이벤트 리스너 등록, 키보드 동작 시 () 안의 함수를 실행
    keyboard.on_press(key_listener)
    # 프로그램이 실행 중인 동안 대기
    keyboard.wait()



