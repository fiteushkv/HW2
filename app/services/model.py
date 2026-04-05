class SentimentModel:
    def __init__(self):
        print("Loading Improved Sentiment & Context Model...")
        # 텍스트 문맥과 연관된 이모지 사전 (사물/상황-이모지 매핑)
        self.context_emojis = {
            '꽃': '🌸', '자연': '🌿', '바다': '🌊', '눈': '❄️', '비': '🌧️',
            '강아지': '🐶', '고양이': '🐱', '동물': '🐾', '사랑': '❤️',
            '커피': '☕', '맥주': '🍺', '음식': '🍔', '돈': '💸', '선물': '🎁',
            '회사': '🏢', '학교': '🏫', '공부': '📚', '퇴근': '🏃‍♂️', '음악': '🎵'
        }

    def predict(self, text: str) -> dict:
        positive_words = ['좋아', '훌륭', '최고', '기뻐', '행복', '사랑', '재밌', '예쁘', '멋지', '추천', 'good', 'great', 'awesome']
        negative_words = ['싫어', '최악', '슬퍼', '나빠', '짜증', '노잼', '실망', '별로', '망했', 'bad', 'terrible', 'awful']
        
        text_lower = text.lower()
        
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        # 1. 감정 기준선(Boundary)을 좀 더 명확하게 분리 (Positive / Negative / Neutral)
        if pos_count > 0 and neg_count == 0:
            sentiment = "Positive"
            score = 0.8 + (pos_count * 0.05)
        elif neg_count > 0 and pos_count == 0:
            sentiment = "Negative"
            score = 0.2 - (neg_count * 0.05)
        elif pos_count > neg_count:
            sentiment = "Positive"
            score = 0.6 + ((pos_count - neg_count) * 0.05)
        elif neg_count > pos_count:
            sentiment = "Negative"
            score = 0.4 - ((neg_count - pos_count) * 0.05)
        else:
            sentiment = "Neutral"
            score = 0.5
            
        score = max(0.01, min(0.99, score)) # 스코어 클리핑
        
        # 2. 컨텍스트 기반 이모지 탐색 로직 적용
        found_emoji = ""
        for keyword, emoji in self.context_emojis.items():
            if keyword in text_lower:
                found_emoji = emoji
                break
                
        # 키워드가 없으면 감정에 따른 기본 이모지로 대체
        if not found_emoji:
            if sentiment == "Positive":
                found_emoji = "✨"
            elif sentiment == "Negative":
                found_emoji = "⛈️"
            else:
                found_emoji = "😶"
        
        return {"sentiment": sentiment, "score": score, "context_emoji": found_emoji}

# 싱글톤 인스턴스
model = SentimentModel()
