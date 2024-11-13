import os, sys
import platform
from subprocess import run

def create_and_activate_venv():
    # 운영체제 인식
    os_type = platform.system()

    # 가상환경 디렉토리 이름
    venv_dir = "venv"

    # 가상환경 생성 명령어
    create_venv_cmd = [sys.executable, "-m", "venv", venv_dir]

    # 가상환경 생성
    run(create_venv_cmd, check=True)

    # 운영체제에 따른 가상환경 활성화 명령어 설정
    if os_type == "Windows":
        activate_cmd = os.path.join(venv_dir, "Scripts", "activate.bat")
    elif os_type in ["Darwin", "Linux"]:  # macOS
        activate_cmd = os.path.join(venv_dir, "bin", "activate")
    else:
        print(f"지원하지 않는 운영체제입니다: {os_type}")
        sys.exit(1)

    print(f"가상환경이 생성되었습니다. 활성화하려면 다음 명령어를 실행하세요:\nsource {activate_cmd}" if os_type != "Windows" else f"{activate_cmd}")

if __name__ == "__main__":
    create_and_activate_venv()