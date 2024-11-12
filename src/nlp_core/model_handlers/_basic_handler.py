import dspy

#Define a simple signature for basic question answering
class BasicQA(dspy.Signature):
    """Answer questions with short factoid answers."""
    question = dspy.InputField()
    answer = dspy.OutputField(desc="3 문장 이하") # eg.) "often between 1 and 5 words"


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
        
        print(f"Question: {question}")
        print(f"Answer: {out.answer}")
        return out
