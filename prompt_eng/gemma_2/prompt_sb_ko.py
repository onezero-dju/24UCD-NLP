from sentence_transformers import SentenceTransformer, util
import torch

# M1 GPU 가속을 위한 Metal 설정
device = torch.device("mps") if torch.backends.mps.is_available() else "cpu"

# Sentence-BERT 모델 로드 (한국어 지원하는 모델 선택 가능)
model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2').to(device)

# 두 텍스트 비교 후 중복되지 않은 단어들 도출
def compare_tokens(agenda_phrases, stt_phrases, threshold=0.75):
    # 안건과 회의 내용을 단어 단위로 분할
    agenda_tokens = ' '.join(agenda_phrases).split()  # 전체 안건을 단어 단위로 분할
    stt_tokens = ' '.join(stt_phrases).split()  # 전체 회의 내용을 단어 단위로 분할

    # 단어를 임베딩으로 변환
    embeddings_agenda = model.encode(agenda_tokens, convert_to_tensor=True).to(device)
    embeddings_stt = model.encode(stt_tokens, convert_to_tensor=True).to(device)
    
    # 유사도 계산 (cosine similarity)
    cosine_scores = util.pytorch_cos_sim(embeddings_agenda, embeddings_stt)

    # 유사도가 낮은 단어들만 추출 (유사도 threshold 이하일 경우 중복되지 않은 단어로 간주)
    non_overlapping_tokens = []
    for i in range(len(agenda_tokens)):
        # 각 안건 단어에 대해 STT 단어 중 최대 유사도 값을 확인
        max_similarity = max(cosine_scores[i]).item()
        if max_similarity < threshold:
            non_overlapping_tokens.append(agenda_tokens[i])

    return non_overlapping_tokens

# 텍스트 파일에서 읽기
def load_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().splitlines()

# 텍스트 파일 로드
agenda_phrases = load_text("agenda.txt")
stt_phrases = load_text("stt.txt")

# 중복되지 않은 회의 단어 도출
non_overlapping_tokens = compare_tokens(agenda_phrases, stt_phrases)

# 결과 출력
print("중복되지 않은 회의 안건 단어:")
for token in non_overlapping_tokens:
    print(token)
