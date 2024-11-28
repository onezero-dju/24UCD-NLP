from fastapi import APIRouter
from api_custom.nlp_link.model_handlers\
    .agenda_handler import get_mentioned_agendas
from api_custom.nlp_link.model_handlers\
    .summarize_handler import BlockSummarizer, FinalSummarizer

router = APIRouter()

block_summarizer = BlockSummarizer()

@router.post("/nlp/in-mtg")
async def summarize_block(
    request: dict[str, str | dict[str, str]]
) -> dict[str, dict[str, str | dict[str, str]]]:
    
    mentioned_agendas = get_mentioned_agendas(request)
    block_summary = block_summarizer.forward(request["block_transcript"])
    return {
        "output": {
            "mentioned_agendas": mentioned_agendas,
            "block_summary": block_summary
        }
    }

# for final summarizing
@router.post("/nlp/end-mtg")
async def conclude(
    request: dict[str,
                  str | dict[str, str]]
) -> dict[str, dict[str, str]]:

    unmentioned_agendas = request["unmentioned_agendas"]
    block_summary_chain = request["block_summary_chain"]
    
    final_summarizer = FinalSummarizer(
                            unmentioned_agendas=unmentioned_agendas,
                            block_summary_chain=block_summary_chain)
    total_summary = final_summarizer.get_total_summary()
    suggested_agenda = final_summarizer.get_agenda_suggest()
    
    return {
        "output": {
            "total_summary": total_summary,
            "suggested_agenda": suggested_agenda
        }
    }
