import dspy
from llama_cpp import Llama

lm_gemma2 = Llama(  # TODO: make the path to the model more robust
    model_path="app/ml_models/language_model/gemma-2-9b-it-Q4_K_M.gguf",
    n_gpu_layers=-1,
    n_ctx=0,
    verbose=False       
)

summarize_lm = dspy.LlamaCpp(
    model="llama",
    llama_model=lm_gemma2,
    model_type="chat",
    temperature=0.4
)

dspy.settings.configure(lm=summarize_lm)

#Define a simple signature for basic question answering
class BasicQA(dspy.Signature):
    """Answer questions with short factoid answers."""
    question = dspy.InputField()
    # answer = dspy.OutputField(desc="often between 1 and 5 words")
    answer = dspy.OutputField(desc="3 문장 이하")


class ModelHandler():
    def __init__(self):
        # Pass signature to 'ChainOfThought' module
        self.generate_answer = dspy.ChainOfThought(BasicQA)
    
    def test_question(self):
        question='안녕? 너는 누구고 무엇을 할 수 있는지 소개해줄래?'
        pred = self.generate_answer(question=question)
        
        print(f"Question: {question}")
        print(f"Answer: {pred.answer}")
        
        return pred
    
    def predict(self, *args):
        return self.test_question()
    
    def answer(self, question: dict):
        out = self.generate_answer(question=question['question'])
        
        # print(f"Question: {question}")
        print(f"Answer: {out.answer}")
        
        return out

print(ModelHandler().test_question())