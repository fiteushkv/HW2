class SentimentModel:
    def __init__(self):
        # MLOps 파이프라인에서는 이 부분에서 사전 학습된 모델(예: HuggingFace, PyTorch 모델)을 로드합니다.
        # 현재는 인프라 구축 단계이므로 Rule-based Mock 모델로 대체합니다.
        print("Loading Sentiment Model...")

    def predict(self, text: str) -> dict:
        positive_words = ['좋아', '훌륭', '최고', '기뻐', '행복', '사랑', '재밌', 'good', 'great', 'awesome']
        negative_words = ['싫어', '최악', '슬퍼', '나빠', '짜증', '노잼', '실망', 'bad', 'terrible', 'awful']
        
        text_lower = text.lower()
        
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        if pos_count > neg_count:
            return {"sentiment": "Positive", "score": 0.85 + (pos_count * 0.01)}
        elif neg_count > pos_count:
            return {"sentiment": "Negative", "score": 0.15 - (neg_count * 0.01)}
        else:
            return {"sentiment": "Neutral", "score": 0.5}

# 싱글톤으로 모델 인스턴스 생성 (API 호출 시마다 모델을 로드하는 것을 방지)
model = SentimentModel()
