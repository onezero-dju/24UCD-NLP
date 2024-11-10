# [ 2024 UCD ] -- RAG

> [!NOTE]  
> '2024 UCD' 프로젝트와 관련된 레포지토리이다.

> [!IMPORTANT]  
> Python 기본 가상 환경인 venv를 사용 중이며, 이 환경은 현재 레포 내 `.venv/` 디렉토리에 보관 중이다. 일반적으로 가상환경 자체는 `.gitignore`를 통해 변화 추적을 무시한다. 마찬가지로 이 레포에서도 `.venv/`를 무시하도록 하고 있으나, 현 시점에서는 몇몇 파일을 강제로 추적하도록 하고 있다.  
> 이는 이 글을 작성하는 시점(24.8.7)을 기준으로, 원하는 기능을 구현하기 위해 필요한 코드가 DSPy의 pip 패키지인 `dspy-ai`에 업데이트되지 않았기 떄문이다(정확히는 아직 DSPy의 릴리즈가 새로 나오지 않았다). 이에 따라 수동으로 패키지를 수정했으며, 다른 수정 사항과 더불어 이 또한 GitHub에 업로드한다.  
> 이후 DSPy의 버전 릴리즈가 이뤄진 뒤에는 더 이상 추적하지 않을 예정이다.
>
> → *24.9.29 기준, DSPy의 버전 릴리즈에 llama.cpp가 사용 가능함에 따라 더 이상 `.venv/`를 추적하지 않는다. 다만, DSPy 버전 2.6부터는 `dspy.LM`을 제외한 LM 클라이언트를 지원하지 않을 예정이라고 한다(현재 v.2.5). 이에 따라 장기적인 유지보수를 위한 코드 변경이 필요하다.*

```
.
│
├── app/
│   ├── __init__.py               # 패키지 초기화 파일
│   ├── main.py                   # API 서버를 실행하는 메인 파일
│   ├── routes/                   # API 라우트 (엔드포인트) 디렉토리
│   │   ├── __init__.py
│   │   ├── users.py              # 예: 사용자 관련 엔드포인트
│   │   └── items.py              # 예: 아이템 관련 엔드포인트
│   ├── models/                   # 데이터베이스 모델 디렉토리
│   │   ├── __init__.py
│   │   └── user.py               # 예: 사용자 모델
│   ├── services/                 # 비즈니스 로직 및 서비스 계층
│   │   ├── __init__.py
│   │   └── user_service.py       # 예: 사용자 관련 비즈니스 로직
│   ├── schemas/                  # 데이터 검증 및 직렬화 스키마
│   │   ├── __init__.py
│   │   └── user_schema.py        # 예: 사용자 관련 데이터 스키마
│   └── config.py                 # 설정 파일
│
├── tests/                        # 테스트 코드 디렉토리
│   ├── __init__.py
│   ├── test_main.py              # 예: 메인 엔드포인트 테스트
│   └── test_user.py              # 예: 사용자 관련 테스트
│
├── Dockerfile                    # Docker 이미지 생성을 위한 파일
├── docker-compose.yml            # Docker Compose 파일 (여러 컨테이너를 관리할 때 사용)
├── requirements.txt              # 프로젝트 의존성 목록
├── .env                          # 환경 변수 파일 (개발/운영 설정)
├── .gitignore                    # Git에서 무시할 파일/디렉토리 목록
└── README.md                     # 프로젝트 설명 파일
```

아래 버튼을 클릭하여 서비스를 실행할 수 있다. 다만, 이 레포에 모델은 실려있지 않으므로, 클라우드 환경에서 모델을 다운로드 하고 적절한 디렉토리에 넣을 필요가 있다. 빠른 방법으로는 버튼 아래의 스크립트를 Cloud Shell 상에서 실행하면 된다.

[![Run on Google Cloud](https://deploy.cloud.run/button.svg)](https://deploy.cloud.run/?git_repo=https://github.com/onezero-dju/24UCD-NLP.git&dir=.)

```bash
wget https://huggingface.co/lmstudio-community/gemma-2-9b-it-GGUF/resolve/main/gemma-2-9b-it-Q4_K_M.gguf -P ./24UCD-NLP/app/ml_models/language_model/
```