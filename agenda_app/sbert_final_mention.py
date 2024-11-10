import json
from sentence_transformers import SentenceTransformer, util
import torch
import re

# M1 GPU 가속을 위한 Metal 설정
device = torch.device("mps") if torch.backends.mps.is_available() else "cpu"

# Sentence-BERT 모델 로드
model_sbert = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2').to(device)

# 문장 분할 함수
def split_sentences(text):
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    return [sentence.strip() for sentence in sentences if sentence.strip()]

# JSON 입력 데이터를 처리하는 함수 (중복되지 않은 안건 추출)
def process_non_overlapping_input(json_data, threshold=0.6):
    agenda_dict = json_data["agenda"]
    transcript = json_data["transcript"]

    # Agenda 문장 리스트로 변환
    agenda_sentences = list(agenda_dict.values())
    transcript_sentences = split_sentences(transcript)

    # Sentence-BERT로 문장 임베딩 계산
    embeddings_agenda = model_sbert.encode(agenda_sentences, convert_to_tensor=True).to(device)
    embeddings_transcript = model_sbert.encode(transcript_sentences, convert_to_tensor=True).to(device)

    # 중복되지 않은 안건 도출
    non_overlapping_agenda = {}
    for i, (index, sentence) in enumerate(agenda_dict.items()):
        # 각 agenda 문장과 transcript 문장 간의 최대 유사도 계산
        similarities = util.pytorch_cos_sim(embeddings_agenda[i], embeddings_transcript)
        max_similarity = torch.max(similarities).item()

        # 유사도가 임계값 이하인 경우 중복되지 않은 안건으로 간주
        if max_similarity < threshold:
            non_overlapping_agenda[index] = sentence

    return non_overlapping_agenda

# 테스트용 JSON 입력 예시
input_json = """
{
  "agenda": {
    "1": "전면 UI 디자인 진행 상황",
    "2": "figma 를 사용한 디자인 초안 완성 여부",
    "3": "최종 디자인을 확정",
    "4": "React 구현 현재 상황",
    "5": "STT API와 MongoDB 연결하기",
    "6": "프로젝트 완료 목표일 통합",
    "7": "RAG 사용하기",
    "8": "적용된 프롬프트 엔지니어링 기법",
    "9": "프로토타입 데드라인 정하기"
  },
  "transcript": "전면 UI 디자인은 어떻게 진행되고 있나요? figma 로 초안을 완성했던데, 다음 단계는 어떻게 되죠? 네, figma로 디자인 초안 은 모두 완성했고, 현재는 React로 구현 중입니다. 다음 주까지는 프론트엔드 프로토타입을 완성할 예정이에요. 그럼 다음주에 최종 디자인을 확정해야겠네요? 네 맞습니다. STT API와 MongoDB의 데이터베이스 연결은 어떻게 진행되고 있나요? 아, 그 부분이 생각보다 복잡하네요. 특히 데이터 스키마와 API 응답 형식을 맞추는 작업이 쉽지 않습니다. 이틀 안에 마무리 지을 수 있도록 최선을 다하겠습니다. 적용된 프롬프트 엔지니어링 기법은 뭔가요? 현재 3가지 방법으로 진행 중입니다. 알겠습니다, 복잡한 부분이 있으면 언제든지 도움 요청하세요. 우리 모두 같이 해결해 나가 봅시다. 저희 프로토타입 데드라인 정하는 건 언제인가요? 프로토타입 데드라인 은 11월 9일까지로 정했습니다."
}
"""

# JSON 입력 파싱
input_data = json.loads(input_json)

# 중복되지 않은 회의 안건 도출
non_overlapping_agenda = process_non_overlapping_input(input_data)

# 결과 출력
print(non_overlapping_agenda)
