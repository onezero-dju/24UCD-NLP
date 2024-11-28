# [ 2024 UCD ] -- NLP

> [!NOTE]  
> '2024 UCD' 프로젝트와 관련된 레포지토리이다.

> [!IMPORTANT]  
> Python 기본 가상 환경인 venv를 사용 중이며, 이 환경은 현재 레포 내 `.venv/` 디렉토리에 보관 중이다. 일반적으로 가상환경 자체는 `.gitignore`를 통해 변화 추적을 무시한다. 마찬가지로 이 레포에서도 `.venv/`를 무시하도록 하고 있으나, 현 시점에서는 몇몇 파일을 강제로 추적하도록 하고 있다.  
> 이는 이 글을 작성하는 시점(24.8.7)을 기준으로, 원하는 기능을 구현하기 위해 필요한 코드가 DSPy의 pip 패키지인 `dspy-ai`에 업데이트되지 않았기 떄문이다(정확히는 아직 DSPy의 릴리즈가 새로 나오지 않았다). 이에 따라 수동으로 패키지를 수정했으며, 다른 수정 사항과 더불어 이 또한 GitHub에 업로드한다.  
> 이후 DSPy의 버전 릴리즈가 이뤄진 뒤에는 더 이상 추적하지 않을 예정이다.
>
> → *24.9.29 기준, DSPy의 버전 릴리즈에 llama.cpp가 사용 가능함에 따라 더 이상 `.venv/`를 추적하지 않는다. 다만, DSPy 버전 2.6부터는 `dspy.LM`을 제외한 LM 클라이언트를 지원하지 않을 예정이라고 한다(현재 v.2.5). 이에 따라 장기적인 유지보수를 위한 코드 변경이 필요하다.*

```text
.
├── Dockerfile_custom_api               # 도커 이미지 빌드용 파일 (커스텀 API)
├── Dockerfile_runpod_api               # 도커 이미지 빌드용 파일 (RunPod SDK 기반)
├── README.md
├── _exp/                               # 실험 파일 디렉토리
├── data/
├── lib/
├── models/
├── notebooks/
│   └── README.md
├── requirements.txt                    # 의존성 패키지 목록
├── scripts/
│   ├── build_docker_image.sh
│   ├── download_model.sh
│   └── initialize_virtual_env.py
└── src/
    ├── api_custom
    │   ├── __init__.py
    │   ├── main.py
    │   ├── nlp_link -> ../nlp_core
    │   ├── routers                     # API 라우트 (엔드포인트) 디렉토리
    │   │   ├── _test_lm_comm.py
    │   │   └── transcript_nlp.py
    │   └── services
    │       ├── __init__.py
    │       └── vdb_client.py
    ├── api_runpod
    │   ├── __init__.py
    │   └── main.py
    └── nlp_core
        ├── README.md
        ├── __init__.py
        ├── dspy_signatures.py
        ├── metric
        │   └── evaluate_model.py
        └── model_handlers
            ├── _basic_handler.py
            ├── agenda_handler.py
            └── summarize_handler.py
```

아래 버튼을 클릭하여 서비스를 실행할 수 있다. 다만, 이 레포에 모델은 실려있지 않으므로, 클라우드 환경에서 모델을 다운로드 하고 적절한 디렉토리에 넣을 필요가 있다. 빠른 방법으로는 버튼 아래의 스크립트를 Cloud Shell 상에서 실행하면 된다.

[![Run on Google Cloud](https://deploy.cloud.run/button.svg)](https://deploy.cloud.run/?git_repo=https://github.com/onezero-dju/24UCD-NLP.git&dir=.)

```bash
wget https://huggingface.co/lmstudio-community/gemma-2-9b-it-GGUF/resolve/main/gemma-2-9b-it-Q4_K_M.gguf -P ./24UCD-NLP/app/ml_models/language_model/
```