from dspy import Signature, InputField, OutputField


class SummarizeBlockTranscript(Signature):
    """
    〈 DSPy `Signature` 〉  
    Summarize the block transcript
    """

    transcript: str = InputField(desc="transcript")
    summary: str = OutputField(
        desc="""
        Generate summary of the context in Korean less than 3 sentences.
        Only output the result, not the process.
        The end of each sentences should be as '한다'.
        """)


class SummarizeTotal(Signature):
    """
    〈 DSPy `Signature` 〉  
    Generate summary of the total summaries concatenated
    """
    
    block_summary_chain: str = InputField(desc="concatenated summaries")
    
    total_summary: str = OutputField(
        desc="""
        Generate a comprehensive summary in Korean.
        Only output the result, not the process.
        The end of each sentences should be as '한다'.
        """)


class SuggestAgenda(Signature):
    """
    〈 DSPy `Signature` 〉  
    Suggest future agendas for
    """
    
    block_summary_chain: str = InputField(desc="concatenated summaries")
    unmentioned_agendas: dict[str, str] = InputField(desc="")
    
    suggested_agenda: str = OutputField(
        desc="""
        'block_summary_chain'에 따라 앞으로 얘기해볼만한 안건을 추천.
        한국어로 작성.
        """)
