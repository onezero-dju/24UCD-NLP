from qdrant_client import QdrantClient
client = QdrantClient("localhost", port=6333)


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


from dspy.retrieve.qdrant_rm import QdrantRM
qdrant_retriever_model = QdrantRM("general_finance_service", client, k=10)
dspy.settings.configure(lm=llamalm, rm=qdrant_retriever_model)

class RAG(dspy.Module):
    def __init__(self, num_passages=3):
        super().__init__()

        self.retrieve = dspy.Retrieve(k=num_passages)
        self.generate_answer = dspy.ChainOfThought("context, question -> answer")
    
    def forward(self, question):
        context = self.retrieve(question).passages
        prediction = self.generate_answer(context=context, question=question)
        return dspy.Prediction(context=context, answer=prediction.answer)
    
    
uncompiled_rag = RAG()

query = "2010년 미국에서 50세 미만에서 발생한 직장암과 결장암의 퍼센트는 어떻게 되며, 이 비율이 2030년에는 어떻게 변할 것으로 예상되는가?"

response = uncompiled_rag(query)

print(response.answer)