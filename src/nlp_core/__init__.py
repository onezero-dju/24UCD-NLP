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
    temperature=0.2,
    max_tokens=500
)

dspy.settings.configure(lm=summarize_lm)
