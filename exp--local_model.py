# https://github.com/stanfordnlp/dspy/pull/1347/commits/ac94c15cc8b45a72fc4f86c482816bef5969f8ac

import dspy
from llama_cpp import Llama


llm = Llama(
    model_path="./_ignore/model/gemma-2-9b-it-Q4_K_M.gguf",
    n_gpu_layers=-1,
    n_ctx=0,
    verbose=False       
)


llamalm = dspy.LlamaCpp(
    model="llama",
    llama_model=llm,
    model_type="chat",
    temperature=0.4
)

dspy.settings.configure(lm=llamalm)

#Define a simple signature for basic question answering
class BasicQA(dspy.Signature):
    """Answer questions with short factoid answers."""
    question = dspy.InputField()
    # answer = dspy.OutputField(desc="often between 1 and 5 words")
    answer = dspy.OutputField(desc="최소 5 문장 이상")

#Pass signature to Predict module
generate_answer = dspy.Predict(BasicQA)

# Call the predictor on a particular input.
question='안녕? 너는 누구고 무엇을 할 수 있는지 소개해줄래?'
pred = generate_answer(question=question)

print(f"Question: {question}")
print(f"Predicted Answer: {pred.answer}")
