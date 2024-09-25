import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

from transformers import AutoModelForCausalLM, AutoTokenizer


# CPU 기반 실행
device = "cpu"

# 양자화된 모델 로드
model_name = "google/gemma-2-9b-it"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, low_cpu_mem_usage=True).to(device)


# 모델 실행


# 텍스트 생성 파이프라인 설정
generator = pipeline("text-generation", model=model, tokenizer=tokenizer, device=0 if torch.backends.mps.is_available() else -1)

# Gemma-2 9B 모델을 사용해 중복되지 않은 단어 도출
def compare_tokens_gemma2(agenda_phrases, stt_phrases):
    # 안건과 회의 내용을 단어 단위로 분할
    agenda_tokens = ' '.join(agenda_phrases).split()  # 전체 안건을 단어 단위로 분할
    stt_tokens = ' '.join(stt_phrases).split()  # 전체 회의 내용을 단어 단위로 분할

    # Gemma-2 9B 모델에 제공할 프롬프트 생성
    prompt = f"다음 단어들 중에서 회의 내용에서 논의되지 않은 단어들을 추출하세요.\n\n회의 안건: {', '.join(agenda_tokens)}\n회의 내용: {', '.join(stt_tokens)}\n\n논의되지 않은 단어는:"

    # Gemma-2 9B 모델로 생성
    with torch.no_grad():  # 그래디언트 계산 방지
        result = generator(prompt, max_new_tokens=50, num_return_sequences=1)
    
    # 생성된 텍스트에서 중복되지 않은 단어들만 추출
    generated_text = result[0]['generated_text']
    
    # "논의되지 않은 단어는:" 이후의 내용을 추출
    if "논의되지 않은 단어는:" in generated_text:
        non_overlapping_tokens = generated_text.split("논의되지 않은 단어는:")[-1].strip()
    else:
        non_overlapping_tokens = generated_text.strip()
    
    return non_overlapping_tokens

# 텍스트 파일에서 읽기 함수
def load_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().splitlines()

# 텍스트 파일 로드
agenda_phrases = load_text("agenda.txt")
stt_phrases = load_text("stt.txt")

# Gemma-2 9B 모델을 사용하여 중복되지 않은 단어 도출
non_overlapping_tokens = compare_tokens_gemma2(agenda_phrases, stt_phrases)

# 결과 출력
print("중복되지 않은 단어:")
print(non_overlapping_tokens)
