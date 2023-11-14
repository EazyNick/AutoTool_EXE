# 9/ 21 백업본

# tkinter는 쓰기 안좋다.
# 현재 동작 방법 : 저장 > 저장 > 실행 , 한번만 저장된다. 다른 사용자 입력 받을려면 다시 켜야함. 저장 버튼 추가, 
# 저장 시 마지막 동작 작동 안함 - 9/20

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
import SaveAndActivate
import keyboard
from pynput.mouse import Listener
import sys
import threading
import Json

# QMainWindow 클래스는 PyQt5에서 제공하는 메인 창(윈도우) 위젯
class MyWindow(QMainWindow):
    #self를 통해 클래스의 자식이 됨, 즉 QMainWindow 메인 창에 연결됨 = 자식클래스가 됨
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt 애플리케이션")
        self.setGeometry(100, 100, 600, 800)
        # self자리에는 연결하고 싶은 위젯 창을 적으면 됨. 우리는 QMainWindow에 연결할 것이니 self 적음
        button = QPushButton("내 동작 저장", self)
        button.setGeometry(200, 100, 200, 100)
        button.clicked.connect(self.button_click)

        button2 = QPushButton("저장 한 동작 실행", self)
        button2.setGeometry(200, 200, 200, 100)
        button2.clicked.connect(self.button_click2)

        button3 = QPushButton("저장 한 동작 불러오고 실행", self)
        button3.setGeometry(300,300, 100, 100)
        button3.clicked.connect(self.button_click3)

        #self로 써야 클래스 내에 같은 함수들끼리 변수 공유 가능. self없으면 같은 클래스내에 다른 함수에서
        #해당 변수들 사용 불가.
        self.toggle = False
        self.key_listener_thread = None  # 키 이벤트 리스너를 실행할 스레드
        self.mouse_listener = None


    def button_click(self):

        if self.toggle == False:
            self.mouse_listener = Listener(on_click=SaveAndActivate.on_click) # on_click 파라미터는 마우스 클릭 이벤트가 발생했을 때 호출할 콜백 함수를 지정합니다.
            self.mouse_listener.start()

    # 키 입력 이벤트 리스너 등록, 키보드 동작 시 () 안의 함수를 실행
            self.key_listener_thread = threading.Thread(target=SaveAndActivate.start_key_listener)
            self.key_listener_thread.start()
        else:
            if self.mouse_listener is not None:
                self.mouse_listener.stop()
            keyboard.unhook_all()
            # 맨 뒤 원소는 없앰.
            self.Arr = SaveAndActivate.Arr[:-1]
            self.key_intervals = SaveAndActivate.key_intervals[1:-1]

            # Arr과 key_intervals의 인덱스 개수 차이로 인해 저장 시, 1개 덜 저장해서 임의의 숫자 딜레이 0 추가
            self.key_intervals.append(0)
            self.intervals, self.Arrange = Json.Json(self.key_intervals, self.Arr)
            print("self.Arr : ", self.Arr)
            print("self.key_intervals : ", self.key_intervals)
        # 스위치 1번 누를 때 마다 toggle 값 변경
        self.toggle = not self.toggle
        
    def button_click2(self):
        
        if self.toggle == False:
            SaveAndActivate.perform_actions(self.Arr, self.key_intervals)
        else:
            if self.mouse_listener is not None:
                self.mouse_listener.stop()
            keyboard.unhook_all()
        self.toggle = not self.toggle

    def button_click3(self):

        if self.toggle == True:
            print(self.intervals)
            SaveAndActivate.perform_actions(self.Arrange, self.intervals)
        else:
            if self.mouse_listener is not None:
                self.mouse_listener.stop()
            keyboard.unhook_all()
        self.toggle = not self.toggle


if __name__ == "__main__":
    app = QApplication(sys.argv) # PyQt5 애플리케이션을 초기화, QApplication은 PyQt5 애플리케이션을 관리하는 데 사용
    # sys.argv는 명령행 인자를 의미하며, 이를 사용하여 PyQt5 애플리케이션에 전달해서 실행할, 명령행 인자를 전달

    #애플리케이션의 메인 창인 MyWindow 클래스의 인스턴스를 생성합니다. 이 때, MyWindow 클래스의 생성자(__init__ 메서드)가 호출됩니다.
    window = MyWindow()

    #window.show(): 메인 창을 화면에 표시합니다. 이 메서드를 호출하지 않으면 창이 숨겨진 상태로 시작합니다.
    window.show()

    #(app.exec_()): PyQt5 애플리케이션의 이벤트 루프를 실행합니다. 이 루프는 사용자의 상호 작용(버튼 클릭, 메뉴 선택 등)을 처리하고 애플리케이션을 실행합니다. 
    #app.exec_()는 애플리케이션의 실행을 시작하고, 이벤트 루프가 종료되면 sys.exit()를 사용하여 애플리케이션을 종료합니다.
    sys.exit(app.exec_())
