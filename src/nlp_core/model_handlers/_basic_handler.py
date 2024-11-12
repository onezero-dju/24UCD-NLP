import dspy
# from llama_cpp import Llama
# from pathlib import Path

# model_name = "gemma-2-9b-it-Q4_K_M.gguf"
# current_file_path = Path(__file__).resolve().parent.parent.parent
# path_to_model = str(current_file_path / "models" / model_name)

# lm_gemma2 = Llama(
#     model_path=path_to_model,
#     n_gpu_layers=-1,
#     n_ctx=0,
#     verbose=False       
# )

# summarize_lm = dspy.LlamaCpp(
#     model="gemma_2",
#     llama_model=lm_gemma2,
#     model_type="text",
#     temperature=0.4,
#     max_tokens=500
# )

# dspy.settings.configure(lm=summarize_lm)

#Define a simple signature for basic question answering
class BasicQA(dspy.Signature):
    """Answer questions with short factoid answers."""
    question = dspy.InputField()
    answer = dspy.OutputField(desc="3 문장 이하") # eg.) "often between 1 and 5 words"


# class SummarizeTranscript(dspy.Signature):
#     """Verify that the text is based on the provided context."""

#     transcript: str = dspy.InputField(desc="transcript")
#     summary: str = dspy.OutputField(desc="요약. '-한다.'체로 작성.")


# # DSPy program for summarization and comparison
# class ConferenceSummarizer(dspy.Module):
#     def __init__(self):
#         super().__init__()
#         # self.summarize_transcript = dspy.ChainOfThought("transcript -> summary") # if needed, add `, agenda_comparison`
#         self.summarize_transcript = dspy.ChainOfThought(SummarizeTranscript)

#     def forward(self, transcript: str):
#         return self.summarize_transcript(transcript=transcript)


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
        # print(f"Answer: {out.answer}")
        return out
