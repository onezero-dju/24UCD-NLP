from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util
import torch

# M1 GPU 가속을 위한 Metal 설정
device = torch.device("mps") if torch.backends.mps.is_available() else "cpu"

# Sentence-BERT 모델 로드
model_sbert = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2').to(device)

# FastAPI 애플리케이션 초기화
app = FastAPI()

# Pydantic 모델 정의 (입력 데이터 형식)
class AgendaInput(BaseModel):
    agenda: dict
    transcript: str

# JSON 입력 데이터를 처리하는 함수
def compare_sentences(agenda_dict, transcript, threshold=0.6):
    # Agenda 문장 리스트로 변환
    agenda_sentences = list(agenda_dict.values())
    stt_sentence = transcript

    # Sentence-BERT로 문장 임베딩 계산
    embeddings_agenda = model_sbert.encode(agenda_sentences, convert_to_tensor=True).to(device)
    embedding_stt = model_sbert.encode(stt_sentence, convert_to_tensor=True).to(device)

    # 코사인 유사도 계산
    cosine_scores = util.pytorch_cos_sim(embeddings_agenda, embedding_stt.unsqueeze(0))

    # 중복되지 않은 안건 인덱스 도출
    non_overlapping_indices = []
    for i, (index, sentence) in enumerate(agenda_dict.items()):
        max_similarity = cosine_scores[i][0].item()

        # 유사도가 임계값 이하인 경우에만 인덱스를 추가
        if max_similarity < threshold:
            non_overlapping_indices.append(index)

    return non_overlapping_indices

# POST 요청을 처리하는 엔드포인트
@app.post("/extract_agenda")
async def extract_agenda(data: AgendaInput):
    try:
        agenda_dict = data.agenda
        transcript = data.transcript

        # 중복되지 않은 회의 안건 인덱스 도출
        non_overlapping_indices = compare_sentences(agenda_dict, transcript)

        # 결과 반환
        return {"non_overlapping_indices": non_overlapping_indices}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))