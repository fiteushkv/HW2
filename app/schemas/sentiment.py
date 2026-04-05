from pydantic import BaseModel, Field

class SentimentRequest(BaseModel):
    text: str = Field(..., example="이 영화 정말 최고였어요!")

class SentimentResponse(BaseModel):
    text: str
    sentiment: str = Field(..., description="Positive, Negative, or Neutral")
    score: float = Field(..., description="Sentiment score between 0.0 and 1.0")
    context_emoji: str = Field(..., description="Emoji matching the context of the text")
