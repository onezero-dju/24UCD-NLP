
import dspy
from dotenv import load_dotenv
from os import environ

load_dotenv()  # load the `.env` file

# Config LM -- Gemini 1.0 pro
gemini_pro = dspy.Google(
    model = "models/gemini-1.0-pro",
    api_key=environ.get('GEMINI_API_KEY')  # Gemini API Key
)

# # Config LM -- GPT-4-turbo
# gpt4T = dspy.OpenAI(
#     model='gpt-4-1106-preview',
#     max_tokens=1000, model_type='chat'
# )

language_model = gemini_pro  # shadowing

# Define the signature for automatic assessments.
class Assess(dspy.Signature):
    """Assess the quality of a summary along the specified dimension."""

    assessed_text = dspy.InputField()
    assessment_question = dspy.InputField()
    assessment_answer = dspy.OutputField(desc="Yes or No")


# def metric(gold, pred, trace=None):
#     question, answer, tweet = gold.question, gold.answer, pred.output

#     engaging = "Does the assessed text make for a self-contained, engaging tweet?"
#     correct = f"The text should answer `{question}` with `{answer}`. Does the assessed text contain this answer?"
    
#     with dspy.context(lm=language_model):
#         correct =  dspy.Predict(Assess)(assessed_text=tweet, assessment_question=correct)
#         engaging = dspy.Predict(Assess)(assessed_text=tweet, assessment_question=engaging)

#     correct, engaging = [m.assessment_answer.lower() == 'yes' for m in [correct, engaging]]
#     score = (correct + engaging) if correct and (len(tweet) <= 280) else 0

#     if trace is not None: return score >= 2
#     return score / 2.0


# Define the metric function with Korean assessment questions.
def summarization_metric(gold, pred, trace=None):
    summary = pred.output
    engaging = "요약이 흥미롭고 잘 작성되었습니까?"
    informative = "요약이 원본 텍스트의 주요 내용을 정확하게 포착하고 있습니까?"

    with dspy.context(lm=language_model):
        engaging_assessment = dspy.Predict(Assess)(assessed_text=summary, assessment_question=engaging)
        informative_assessment = dspy.Predict(Assess)(assessed_text=summary, assessment_question=informative)

    engaging_score = engaging_assessment.assessment_answer.lower() == 'yes'
    informative_score = informative_assessment.assessment_answer.lower() == 'yes'

    score = (engaging_score + informative_score) / 2.0
    return score >= 1.0 if trace is not None else score

# Example usage with an optimizer.
from dspy.teleprompt import BootstrapFewShot
trainset = [...]  # Your training data here
fewshot_optimizer = BootstrapFewShot(metric=summarization_metric, max_bootstrapped_demos=4, max_labeled_demos=16)
compiled_program = fewshot_optimizer.compile(student=your_dspy_program, trainset=trainset)

# -------

class Assess(dspy. Signature):
    """Assess the quality of a summary along the specified dimension."""
    assessed_text = dspy. InputField
    assessment_question = dspy. InputField ( )
    assessment_answer = dspy.OutputField(desc="Yes or No")
    


# Define the metric function with Korean assessment questions.
def summarization_metric(gold, pred, trace=None):
    summary = pred.output
    engaging= "요약이 흥미롭고 잘 작성되었습니까?" # Is the summary engaging and well-written?
    informative="요악이 원본 텍스트의 주요 내용을 정확하게 포착하고 있습니까?"# Does the summary accurately capture the key points of the source text?

    with dspy. context (lm=language_model):
        # Create a Predict instance with the Assess signature and call it with the summary and engaging question.
        engaging_assessment = dspy.Predict(Assess)(assessed_text=summary, assessment_question=engaging)

        # Create another Predict instance with the Assess signature and call it with the summary and informative question.
        informative_assessment = dspy.Predict(Assess)(assessed_text=summary, assessment_question=informative)

    # Evaluate the responses from the language model.
    engaging_score = engaging_assessment.assessment_answer.lower() == 'yes'
    informative_score = informative_assessment.assessment_answer. lower () == 'yes'
    score = (engaging_score + informative_score) / 2.0

    return score >= 1.0 if trace is not None else score


# -----

from dspy.datasets import DataLoader
from dspy.teleprompt import BootstrapFewShotWithRandomSearch
from dspy import Module

# Load JSON data
dl = DataLoader()
json_dataset = dl.from_json("conference_data.json", fields=("transcript", "agenda"), input_keys=("transcript",))

# Define a DSPy program for summarization and comparison
class ConferenceSummarizer(Module):
    def __init__(self):
        super().__init__()
        self.prog = dspy.ChainOfThought("transcript -> summary, agenda_comparison")

    def forward(self, transcript):
        return self.prog(transcript=transcript)

# Define a metric for evaluation
def agenda_metric(example, pred, trace=None):
    # Implement logic to compare pred.summary with example.agenda
    # and extract additional topics
    return score

# Choose an optimizer
optimizer = BootstrapFewShotWithRandomSearch(metric=agenda_metric)

# Compile the program
optimized_program = optimizer.compile(ConferenceSummarizer(), trainset=json_dataset)
