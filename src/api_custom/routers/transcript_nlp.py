from fastapi import APIRouter
from api_custom.nlp_link.model_handlers\
    .agenda_handler import get_mentioned_agendas
from api_custom.nlp_link.model_handlers\
    .summarize_handler import BlockSummarizer, FinalSummarizer

router = APIRouter()

block_summarizer = BlockSummarizer()

@router.post("/nlp/in-mtg")
async def summarize_block(request: dict):
    mentioned_agendas = get_mentioned_agendas(request)
    block_summary = block_summarizer.forward(request["transcript"])
    return {
        "mentioned_agendas": mentioned_agendas,
        "block_summary": block_summary
    }

# @router.post("/nlp/end-mtg")
# async def conclude():
#     """
#     for final summarizing
#     """
#     final_summary = FinalSummarizer.forward()
#     return {
#         "final_summary": final_summary
#     }
