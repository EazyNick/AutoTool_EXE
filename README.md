# 사용자 동작 자동화 프로그램

이 프로젝트는 사용자의 키보드 입력 및 마우스 클릭 동작을 기록하고 저장한 후, 재생할 수 있는 자동화 프로그램입니다. PyQt5를 활용한 GUI 인터페이스를 제공하여 사용자가 손쉽게 동작을 저장하고 실행할 수 있도록 지원합니다.

## 목차

- [프로젝트 개요](#프로젝트-개요)
- [주요 기능](#주요-기능)
- [프로젝트 구조](#프로젝트-구조)
- [설치 및 실행](#설치-및-실행)
- [사용 방법](#사용-방법)
- [코드 상세 설명](#코드-상세-설명)
- [향후 개선 사항](#향후-개선-사항)
- [라이선스](#라이선스)
- [감사의 말](#감사의-말)

## 프로젝트 개요

이 프로그램은 키보드와 마우스의 동작을 기록하여 저장하고, 이를 JSON 파일로 저장하여 재실행할 수 있도록 구현되었습니다. 기록된 동작은 프로그램의 GUI를 통해 실행할 수 있습니다.

## 주요 기능

- **동작 기록**: 키보드와 마우스 클릭의 좌표 및 입력 간격을 저장
- **동작 재생**: 기록된 동작을 PyAutoGUI를 사용하여 재생
- **JSON 파일 저장**: 동작을 JSON 형식으로 저장하고 불러오기 가능
- **GUI 인터페이스**: PyQt5 기반의 직관적인 GUI 제공

## 프로젝트 구조

```plaintext
├── main.py                 # 메인 파일 (프로그램 실행 진입점)
├── GUI.py                  # GUI를 담당하는 PyQt5 기반의 인터페이스
├── chatgpt.py              # ChatGPT API와 관련된 기능 파일
├── data.json               # 저장된 동작과 시간을 담은 JSON 파일
├── Json.py                 # JSON 파일을 다루는 기능 모듈
├── SaveAndActivate.py      # 사용자의 동작을 기록하고 재생하는 핵심 기능 모듈
└── README.md               # 프로젝트 문서
```

## 설치 및 실행

### 사전 요구 사항

- **Python 3.6** 이상

- 필요한 라이브러리 설치:
  ```bash
  pip install pyqt5 pynput pyautogui
  ```

### 실행 방법

1. 저장소를 클론한 후 해당 디렉토리로 이동합니다.
   ```bash
   git clone https://github.com/yourusername/automation-app.git
   cd automation-app
   ```
2. main.py 파일을 실행하여 GUI 프로그램을 시작합니다
  ```bash
   python main.py
   ```

## 사용 방법

- **동작 기록**: GUI에서 "내 동작 저장" 버튼을 눌러 키보드와 마우스의 입력을 기록합니다.
- **동작 실행**: "저장한 동작 실행" 버튼을 눌러 기록된 동작을 재생합니다.
- **JSON 저장/불러오기**: JSON 파일에 저장된 동작을 불러오거나, 현재 기록된 동작을 JSON 파일로 저장하여 언제든 불러올 수 있습니다.

---

## 코드 상세 설명

### 주요 모듈 및 클래스

- **`main.py`**: 프로그램의 진입점으로 `MyWindow` 클래스를 초기화하여 GUI를 실행합니다.
- **`GUI.py`**: PyQt5 기반으로 GUI를 구현합니다.
  - **`MyWindow` 클래스**:
    - GUI의 기본 창을 구성하며, 버튼 클릭과 사용자 입력을 처리합니다.
    - `button_click`: 동작 기록 및 JSON 저장 기능 실행
    - `button_click2`: JSON에 저장된 동작을 재생
- **`SaveAndActivate.py`**: 사용자 입력을 기록하고 저장된 데이터를 재생하는 기능을 구현한 모듈입니다.
  - **주요 함수**:
    - `perform_actions`: 저장된 `Arr`와 `key_intervals`을 사용하여 동작을 재생
    - `on_click`: 마우스 클릭 좌표 및 버튼 정보를 저장
    - `key_listener`: 키보드 입력 및 간격 정보를 저장
- **`Json.py`**: `data.json` 파일에 동작 데이터를 저장하고 불러오는 모듈입니다.
  - **주요 함수**:
    - `Json`: 현재 동작과 시간을 JSON 형식으로 저장
    - `Json_Get`: JSON 파일에서 데이터를 불러와서 인터벌과 동작 내용 리스트로 반환
- **`chatgpt.py`**: 사용자의 입력 값을 ChatGPT와 연동하기 위해 작성된 파일입니다.

### 데이터 파일

- **`data.json`**: JSON 형식으로 저장된 동작 및 시간 간격 데이터를 저장합니다.

---

## 향후 개선 사항

- **동작 편집 기능 추가**: 저장된 동작을 GUI에서 편집하여 미세 조정할 수 있는 기능
- **데이터베이스 연동**: JSON 파일 대신 데이터베이스를 이용한 동작 데이터의 지속적 저장 및 관리
- **다양한 동작 지원**: 마우스 드래그 및 특정 조건에 따른 동작 추가
- **보안 기능 강화**: 민감한 데이터를 다룰 경우 보안 프로토콜 추가

---

## 라이선스

MIT License에 따라 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

---

## 감사의 말

이 프로젝트는 Python 커뮤니티와 PyQt5 및 PyAutoGUI 커뮤니티의 도움을 받아 개발되었습니다.  
자동화 및 GUI 개발에 도움을 준 오픈소스 프로젝트에 감사드립니다.
