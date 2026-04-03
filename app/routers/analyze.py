from fastapi import APIRouter, HTTPException, Request
from app.schemas.analyze import AnalyzeRequest, AnalyzeResponse
from app.services.claude_service import ClaudeService

router = APIRouter(prefix="/analyze", tags=["analysis"])


@router.post("/transcript", response_model=AnalyzeResponse)
async def analyze_transcript(payload: AnalyzeRequest, request: Request):
    if not payload.transcript.strip():
        raise HTTPException(status_code=400, detail="Transcript cannot be empty")

    try:
        settings = request.app.state.settings
        service = ClaudeService(api_key=settings.anthropic_api_key)

        result = await service.analyze(payload.transcript)
        return result

    except Exception:
        raise HTTPException(status_code=500, detail="Analysis failed")