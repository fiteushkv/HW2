from fastapi import APIRouter
from app.schemas.sentiment import SentimentRequest, SentimentResponse
from app.services.model import model

router = APIRouter()

@router.post("/", response_model=SentimentResponse)
async def analyze_sentiment(request: SentimentRequest):
    """
    사용자가 입력한 텍스트에 대한 감정 분석 결과를 반환합니다.
    """
    result = model.predict(request.text)
    return SentimentResponse(
        text=request.text,
        sentiment=result["sentiment"],
        score=result["score"],
        context_emoji=result["context_emoji"]
    )
