# tkinter는 쓰기 안좋다.
# 현재 동작 방법 : 저장 > 저장 > 실행 , 한번만 저장된다. 다른 사용자 입력 받을려면 다시 켜야함. 초기화 기능 만들어야 함
# 사용자 입력버튼 추가- 9/21

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QInputDialog, QLineEdit, QLabel, QMessageBox
from PyQt5.QtCore import Qt
import SaveAndActivate
import keyboard
from pynput.mouse import Listener
import threading
import Json
import sys
import os,subprocess #모듈 호출

app = QApplication(sys.argv) # PyQt5 애플리케이션을 초기화, QApplication은 PyQt5 애플리케이션을 관리하는 데 사용
# sys.argv는 명령행 인자를 의미하며, 이를 사용하여 PyQt5 애플리케이션에 전달해서 실행할, 명령행 인자를 전달

# QMainWindow 클래스는 PyQt5에서 제공하는 메인 창(윈도우) 위젯
class MyWindow(QMainWindow):
    #self를 통해 클래스의 자식이 됨, 즉 QMainWindow 메인 창에 연결됨 = 자식클래스가 됨
    def __init__(self):
        super().__init__()

        #self로 써야 클래스 내에 같은 함수들끼리 변수 공유 가능. self없으면 같은 클래스내에 다른 함수에서 해당 변수들 사용 불가.
        #1개의 버튼만 눌리도록 체크하는 변수
        self.toggle = False
        # 키 이벤트 리스너를 실행할 스레드
        self.key_listener_thread = None
        #마우스 리스너 초기화
        self.mouse_listener = None
        # 버튼 클릭 상태를 나타내는 변수
        self.button_clicked = False
        #입력값 저장하는 1번 클릭버튼 초기화 조건 변수
        self.cnt = 0
        
        # 사용자 입력 받는 입력란 생성
        self.input_field = QLineEdit(self)
        self.input_field.setGeometry(50, 50, 200, 40)
        self.input_field.setPlaceholderText("사용자의 입력 = 함수")

        # QLineEdit에서 엔터 키 눌렀을 때 처리할 슬롯(함수) 연결
        self.input_field.returnPressed.connect(self.on_input_enter)

        #창 타이틀 이름, 크기 설정
        self.setWindowTitle("PyQt 애플리케이션")
        self.setGeometry(100, 100, 600, 800)

        # self자리에는 연결하고 싶은 위젯 창을 적으면 됨. 우리는 QMainWindow에 연결할 것이니 self 적음
        # 동작 저장 버튼
        self.button = QPushButton("내 동작 저장", self)
        self.button.setGeometry(200, 100, 200, 100)
        self.button.clicked.connect(self.button_click)

        # 저장 한 동작 실행 버튼
        self.button2 = QPushButton("저장 한 동작 실행", self)
        self.button2.setGeometry(200, 200, 200, 100)
        self.button2.clicked.connect(self.button_click2)

        # json에 저장 한 동작 불러오고 실행 버튼
        self.button3 = QPushButton("저장 한 동작 불러오고 실행", self)
        self.button3.setGeometry(200,300, 200, 100)
        self.button3.clicked.connect(self.button_click3)

        # 사용자 입력 받는 버튼
        self.button4 = QPushButton("사용자 입력 받기", self)
        self.button4.setGeometry(100, 550, 200, 100)
        self.button4.clicked.connect(self.button_click4)

        #화면을 항상 상단에 고정
        self.initUI()

    #화면을 항상 상단에 고정
    def initUI(self):
            label = QLabel('이 창은 항상 화면 최상단에 고정됩니다.', self)
            label.setAlignment(Qt.AlignCenter)
            label.setGeometry(100, 0, 400, 50)

            # 창의 WindowFlags를 조절하여 항상 최상단에 고정합니다.
            self.setWindowFlag(Qt.WindowStaysOnTopHint)

    def closeEvent(self, event):
        # 창을 닫을 때 호출되는 메서드
        reply = QMessageBox.question(self, '확인', '프로그램을 종료하시겠습니까?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()  # 프로그램 종료
            app.quit()
            print(os.system('tasklist')) #프로세스 목록 출력
            #os.system('taskkill /f /pid 11172') #pid를 사용한 프로세스 종료
            os.system('taskkill /f /im main.exe') #프로세스명을 사용한 프로세스 종료
        else:
            event.ignore()  # 창을 닫지 않음

    # 사용자 입력 받았을 때 사용할 함수
    def on_input_enter(self):
        # 사용자가 입력 후 엔터를 눌렀을 때 동작하는 코드
        user_input = self.input_field.text()
        print("사용자 입력 (Enter로 제출):", user_input)
        # 여기에서 추가적인 처리를 할 수 있습니다.

        # 사용자 입력란 비우기
        self.input_field.clear()

    # 동작 저장 버튼
    def button_click(self):

        if not self.button_clicked:
            self.button.setStyleSheet('''
                background-color: red;
                color: white;
            ''')
        else:
            self.button.setStyleSheet('')  # 원래 스타일로 돌아갑니다.

        self.button_clicked = not self.button_clicked   

        if self.toggle == False:
            self.mouse_listener = Listener(on_click=SaveAndActivate.on_click) # on_click 파라미터는 마우스 클릭 이벤트가 발생했을 때 호출할 콜백 함수를 지정합니다.
            self.mouse_listener.start()

            # 키 입력 이벤트 리스너 등록, 키보드 동작 시 () 안의 함수를 실행
            self.key_listener_thread = threading.Thread(target=SaveAndActivate.start_key_listener)
            self.key_listener_thread.start()

            #한번 실행 후 두번째 클릭 시 초기화
            if self.cnt == 1:
                SaveAndActivate.Arr, SaveAndActivate.key_intervals = SaveAndActivate.reset(SaveAndActivate.Arr, SaveAndActivate.key_intervals)
                if SaveAndActivate.Arr == [] and SaveAndActivate.key_intervals == []:
                    print("초기화 완료", SaveAndActivate.Arr, SaveAndActivate.key_intervals)

        else:
            if self.mouse_listener is not None:
                self.mouse_listener.stop()
            keyboard.unhook_all()

            # 맨 뒤 원소는 없앰.
            self.Arr = SaveAndActivate.Arr[:-1]
            self.key_intervals = SaveAndActivate.key_intervals[1:-1]

            # Arr과 key_intervals의 인덱스 개수 차이로 인해 저장 시, 1개 덜 저장해서 임의의 숫자 딜레이 0 추가
            self.key_intervals.append(0)

            #처음 눌렀을 때는 저장
            if self.cnt == 0:
                self.intervals, self.Arrange = Json.Json(self.key_intervals, self.Arr)
                print("저장 값 : ", self.Arrange, self.intervals)
                self.cnt = 1
            # 두번째 눌렀을 때 동작
            elif self.cnt == 1:
                self.intervals, self.Arrange = Json.Json(self.key_intervals, self.Arr)
                print("저장 값 : ", self.Arrange, self.intervals)
                self.cnt = 0

            # print("self.Arr : ", self.Arr)
            # print("self.key_intervals : ", self.key_intervals)

        # 스위치 1번 누를 때 마다 toggle 값 변경
        self.toggle = not self.toggle
        
    # 저장한 동작 실행 버튼
    def button_click2(self):

        SaveAndActivate.perform_actions(self.Arrange, self.intervals)

    # json에 저장 한 동작 불러오고 실행 버튼
    def button_click3(self):

        loaded_keys, loaded_values = Json.Json_Get()
        SaveAndActivate.perform_actions(loaded_values, loaded_keys)

    # 사용자 입력 받는 버튼
    def button_click4(self):

        # 사용자 입력 받는 버튼 클릭 시 동작하는 코드
        text, ok = QInputDialog.getText(self, '사용자 입력', '입력하세요:')
        if ok:
            print("사용자 입력:", text)  

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWindow()
    ex.show()
    sys.exit(app.exec_())
