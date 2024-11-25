from sentence_transformers import SentenceTransformer, util
import torch

# Sentence-BERT 모델 로드
model_sbert = SentenceTransformer("sentence-transformers/paraphrase-multilingual-mpnet-base-v2")

# 문장 임베딩 함수
def get_sbert_embeddings(sentences):
    return model_sbert.encode(
        sentences, convert_to_tensor=True, show_progress_bar=False
    )

# 중복되지 않은 문장 비교 함수 (평균 유사도 사용)
def compare_sentences_sbert(agenda_sentences, stt_sentences, threshold=0.3):
    embeddings_agenda = get_sbert_embeddings(agenda_sentences)
    embeddings_stt = get_sbert_embeddings(stt_sentences)

    non_overlapping_sentences = []
    for i, emb_agenda in enumerate(embeddings_agenda):
        # 모든 STT 문장과의 유사도 계산 후 평균값 사용
        similarities = util.cos_sim(emb_agenda, embeddings_stt)
        mean_similarity = torch.mean(similarities).item()
        print(f"Mean Similarity for '{agenda_sentences[i]}': {mean_similarity:.2f}")

        # 평균 유사도가 threshold 이하인 경우만 추가
        if mean_similarity < threshold:
            non_overlapping_sentences.append(agenda_sentences[i])

    return non_overlapping_sentences

# 회의 안건 추천 형식으로 출력
def generate_natural_summary(non_overlapping_sentences):
    if not non_overlapping_sentences:
        return "모든 안건이 논의되었습니다. 추가 추천 사항이 없습니다."
    
    output = "회의 안건 추천:"
    for idx, sentence in enumerate(non_overlapping_sentences, 1):
        output += f"\n{idx}. {sentence}"
    return output

# 텍스트 파일에서 읽기 함수
def load_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().splitlines()

# 텍스트 파일 로드
agenda_sentences = load_text("/Users/minhyeok/Desktop/PROJECT/UCD_PROJECT/Prompt_Playground/text_file/agenda2.txt")
stt_sentences = load_text("/Users/minhyeok/Desktop/PROJECT/UCD_PROJECT/Prompt_Playground/text_file/stt2.txt")

# 중복되지 않은 회의 안건 도출
non_overlapping_sentences = compare_sentences_sbert(agenda_sentences, stt_sentences)

# 회의 안건 추천 목록 출력
final_output = generate_natural_summary(non_overlapping_sentences)

# 결과 출력
print(final_output)