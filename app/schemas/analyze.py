from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    transcript: str = Field(..., min_length=10)


class AnalyzeResponse(BaseModel):
    qa_score: int
    justification: str
    summary: str
    sentiment: str