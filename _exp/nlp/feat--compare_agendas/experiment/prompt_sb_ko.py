from sentence_transformers import SentenceTransformer, util
import torch

# M1 GPU 가속을 위한 Metal 설정
device = torch.device("mps") if torch.backends.mps.is_available() else "cpu"

# Sentence-BERT 모델 로드 (한국어 지원하는 모델 선택 가능)
model_sbert = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2').to(device)

# kr_prompts 파일에서 프롬프트 가져오기
from prompt import kr_prompts

# 프롬프트를 결합한 입력 데이터 생성
def create_prompt_input(agenda_phrases, stt_phrases):
    # kr_prompts에서 프롬프트 생성
    prompt = kr_prompts["context"].format(context=' '.join(stt_phrases))

    # 회의 안건과 회의 내용 사이의 비교를 위한 프롬프트 결합
    return [f"{agenda}: {prompt}" for agenda in agenda_phrases]

# 문장 단위로 비교하여 중복되지 않은 항목 도출
def compare_sentences(agenda_sentences, stt_sentences, threshold=0.6):  # 문장 단위로 비교, threshold 조정
    # Sentence-BERT로 문장 임베딩 계산
    embeddings_agenda = model_sbert.encode(agenda_sentences, convert_to_tensor=True).to(device)
    embeddings_stt = model_sbert.encode(stt_sentences, convert_to_tensor=True).to(device)

    # 코사인 유사도 계산
    cosine_scores = util.pytorch_cos_sim(embeddings_agenda, embeddings_stt)

    # 중복되지 않은 항목 도출
    non_overlapping_sentences = []
    for i in range(len(agenda_sentences)):
        max_similarity = max(cosine_scores[i]).item()
        
        # 임계값보다 낮은 경우에만 중복되지 않은 문장으로 처리
        if max_similarity < threshold:
            non_overlapping_sentences.append(agenda_sentences[i])

    return non_overlapping_sentences

# 텍스트 파일에서 읽기
def load_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().splitlines()

# 텍스트 파일 로드
agenda_sentences = load_text("agenda.txt")  # 문장 단위로 저장된 안건
stt_sentences = load_text("stt.txt")  # 문장 단위로 저장된 회의 내용

# 중복되지 않은 회의 안건 도출 (문장 단위)
non_overlapping_sentences = compare_sentences(agenda_sentences, stt_sentences)

# 결과 출력: 중복되지 않은 회의 안건만 출력
print("\n중복되지 않은 회의 안건:")
for idx, sentence in enumerate(non_overlapping_sentences, 1):
    print(f"{idx}. {sentence}하기")

print(non_overlapping_sentences)