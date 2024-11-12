from fastapi import APIRouter
from api_custom.nlp_link.model_handlers\
    .agenda_handler import *
from api_custom.nlp_link.model_handlers\
    .summarize_handler import BlockSummarizer, FinalSummarizer

router = APIRouter()

block_summarizer = BlockSummarizer()

@router.post("/nlp/in-mtg")
async def summarize_block(request):
    mentioned_agendas = None
    block_summary = block_summarizer.forward()
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