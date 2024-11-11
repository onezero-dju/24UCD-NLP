import dspy
from llama_cpp import Llama
from pathlib import Path

model_name = "gemma-2-9b-it-Q4_K_M.gguf"
current_file_path = Path(__file__).resolve().parent.parent.parent
path_to_model = str(current_file_path / "models" / model_name)

lm_gemma2 = Llama(
    model_path=path_to_model,
    n_gpu_layers=-1,
    n_ctx=0,
    verbose=False       
)

summarize_lm = dspy.LlamaCpp(
    model="gemma_2",
    llama_model=lm_gemma2,
    model_type="text",
    temperature=0.4,
    max_tokens=500
)

dspy.settings.configure(lm=summarize_lm)

#Define a simple signature for basic question answering
class BasicQA(dspy.Signature):
    """Answer questions with short factoid answers."""
    question = dspy.InputField()
    answer = dspy.OutputField(desc="3 문장 이하") # eg.) "often between 1 and 5 words"


class SummarizeTranscript(dspy.Signature):
    """Verify that the text is based on the provided context."""

    transcript: str = dspy.InputField(desc="transcript")
    summary: str = dspy.OutputField(desc="요약. '-한다.'체로 작성.")


# DSPy program for summarization and comparison
class ConferenceSummarizer(dspy.Module):
    def __init__(self):
        super().__init__()
        # self.summarize_transcript = dspy.ChainOfThought("transcript -> summary") # if needed, add `, agenda_comparison`
        self.summarize_transcript = dspy.ChainOfThought(SummarizeTranscript)

    def forward(self, transcript: str):
        return self.summarize_transcript(transcript=transcript)


class BasicHandler(dspy.Module):
    def __init__(self):
        super().__init__()
        # Pass signature to 'ChainOfThought' module
        self.generate_answer = dspy.ChainOfThought(BasicQA)
    
    def lm_greet(self):
        question='안녕? 너는 누구고 무엇을 할 수 있는지 간단하게 소개해줘.'
        return dspy.Predict(BasicQA)(question=question)
    
    def custom_question_answer(self, question: dict):
        out = self.generate_answer(question=question['question'])
        
        # print(f"Question: {question}")
        print(f"Answer: {out.answer}")
        return out


if __name__ == "__main__":
    conference_summarizer = ConferenceSummarizer()
    
    test_string = "\
        다음 글을 3 문장으로 요약해줘. \
        집중과 몰입을 강조할 때, 초보적인 독자가 가지기 쉬운 오류는 그것이 빠른 속도에서 얻어지는 것이라고 착각한다는 사실입니다. \
        결론적으로 말해 집중이나 몰입은 속도와는 무관한 ‘정신의 고조상태’를 말할 뿐입니다. \
        오히려 여러분이 분명히 아셔야 될 것은 좋은 독서 전체에서 ‘느림과 여유의 미학’이 차지하는 비중이 무려 70~80%에 이른다는 점입니다. \
        스피노자는 이성(理性)이 절대 위치에 있는 철학 전통에서 인간을 이해하는 데 무엇보다 감성(感性)이 중요한 키워드임을 주지시켰던 혁명적인 철학자입니다. \
        그는 공포와 예속이 익숙한 시대에 항상 긍정과 자유의 철학을 이야기함으로써 살해 위협도 받고, 동료들로부터 따돌림당하기도 했습니다. \
        유대교 교리에 어긋나는 언행으로 유대 교회에 의해 파문당했던 그는 렌즈 가공일을 하다 생긴 폐질환으로 숨지고 맙니다. \
        스피노자는 언제 어떤 상황에 처해서도 항상 느리고 여유 있는 자세로 삶을 영위한 걸로 유명합니다. \
        그 저명한 대가가 평생 소장한 책은 100권이 채 되지 않았던 것입니다. \
        그런데 스피노자보다도 몇 배나 더 ‘느림의 미학’을 추구한 이가 있으니, ‘슬로 리딩(Slow reading)’의 창시자로 유명한 하시모토 다케시입니다. \
        나다고등학교 교장으로 재직하던 시절, 그는 학생들에게 놀이를 통해 배움에 대한 흥미와 즐거움을 주고자 슬로 리딩법을 고안해 냅니다. \
        고교 3년 동안 학생들은 선정된 오직 한 권의 책만 가지고서 다양하게 읽고 생각하고 쓰며 토론해 나갑니다. \
        그 황당하리라 여겨졌던 수업의 결과는 의외로 도쿄대와 교토대의 합격률 1위라는 찬란한 결과로 나타나 세상을 경악시키지요. \
        졸업생의 무려 58%가 도쿄대에 합격하고, 특히 낙타가 바늘구멍 들어가기보다 어렵다는 100명 정원의 도쿄대 의대 합격생을 한 해에만 16명을 배출하는 기염을 토합니다.\
    "
    
    print(conference_summarizer.forward(test_string))
# end main