class SentimentModel:
    def __init__(self):
        print("Loading Ultimate Context-Aware Sentiment Model...")
        # 1. 자연어 문맥 매핑 사전 대폭 확장 (명사 위주)
        self.context_emojis = {
            # 자연/날씨
            '꽃': '🌸', '자연': '🌿', '바다': '🌊', '눈': '❄️', '비': '🌧️', '맑음': '☀️', '구름': '☁️', '불': '🔥', '무지개': '🌈', '별': '⭐', '태양': '🌞', '달': '🌙', '산': '⛰️',
            # 동물
            '강아지': '🐶', '개': '🐕', '고양이': '🐱', '동물': '🐾', '토끼': '🐰', '새': '🐦', '물고기': '🐟', '곰': '🐻', '호랑이': '🐯',
            # 감정/관계
            '사랑': '❤️', '이별': '💔', '눈물': '😢', '웃음': '😆', '분노': '😠', '우정': '🤝', '축하': '🎉', '행복': '🥰', '놀람': '😲', '짜증': '😒', '키스': '💋',
            # 음식/음료
            '커피': '☕', '맥주': '🍺', '소주': '🍶', '와인': '🍷', '음식': '🍔', '피자': '🍕', '치킨': '🍗', '과일': '🍎', '아이스크림': '🍦', '케이크': '🍰', '초콜릿': '🍫',
            # 생활/오피스/기타
            '돈': '💸', '재물': '💰', '선물': '🎁', '회사': '🏢', '학교': '🏫', '공부': '📚', '퇴근': '🏃‍♂️', '음악': '🎵', '노래': '🎤', '영화': '🎬', '게임': '🎮', '운동': '🏋️‍♂️', '여행': '✈️', '차': '🚗', '컴퓨터': '💻', '코딩': '👨‍💻', '잠': '💤', '약': '💊', '병원': '🏥', '생일': '🎂'
        }

    def predict(self, text: str) -> dict:
        # 단어장을 훨씬 촘촘하게 확장하여 긍/부정 식별률 향상
        positive_words = [
            '좋아', '훌륭', '최고', '기뻐', '행복', '사랑', '재밌', '예쁘', '멋지', '추천', '아름다', '성공', '합격', '대박', '완벽', '환상', '기대', '고마', '감사', '편안', '시원', '달콤', '맛있', '신나', '짜릿', '최애', '강추', '짱',
            'good', 'great', 'awesome', 'excellent', 'amazing', 'perfect', 'beautiful', 'love', 'happy'
        ]
        
        negative_words = [
            '싫어', '최악', '슬퍼', '나빠', '짜증', '노잼', '실망', '별로', '망했', '아퍼', '우울', '화나', '분노', '절망', '실패', '끔찍', '구려', '귀찮', '피곤', '힘들', '답답', '아쉬', '비추', '별로', '노맛', '개판', '지루', '쓰레기',
            'bad', 'terrible', 'awful', 'worst', 'hate', 'sad', 'angry'
        ]
        
        text_lower = text.lower()
        
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        # 2. 감정 기준선(Boundary)을 더욱 명확하게 분리 (Positive / Negative / Neutral)
        # Neutral의 범위를 줄이고, 긍/부정의 점수(Threshold)를 확실하게 갈라줌.
        weight = 0.1 # 매칭 단어 1개당 감정 가중치
        
        if pos_count > 0 and neg_count == 0:
            sentiment = "Positive"
            score = 0.75 + (pos_count * weight)
        elif neg_count > 0 and pos_count == 0:
            sentiment = "Negative"
            score = 0.25 - (neg_count * weight)
        elif pos_count > neg_count:
            sentiment = "Positive"
            score = 0.60 + ((pos_count - neg_count) * weight)
        elif neg_count > pos_count:
            sentiment = "Negative"
            score = 0.40 - ((neg_count - pos_count) * weight)
        else:
            # 긍정 단어와 부정 단어의 개수가 정확히 같거나 둘 다 0일 때만 중립 시그널을 제공합니다.
            sentiment = "Neutral"
            score = 0.50
            
        # 스코어 클리핑 (Confidence Score가 비정상적으로 치솟거나 음수가 되지 않도록 방어)
        score = max(0.01, min(0.99, score))
        
        # 3. 강화된 컨텍스트 기반 이모지 탐색 로직 적용
        # 텍스트에 포함된 가장 긴 키워드를 우선 매칭하거나, 먼저 발견되는 키워드를 이모지로 세팅
        found_emoji = ""
        for keyword, emoji in self.context_emojis.items():
            if keyword in text_lower:
                found_emoji = emoji
                break
                
        # 매칭되는 문맥(키워드)이 없을 경우, 감정에 적절한 '기본 이모지'로 할당
        if not found_emoji:
            if sentiment == "Positive":
                found_emoji = "✨"
            elif sentiment == "Negative":
                found_emoji = "⛈️"
            else:
                found_emoji = "😶"
        
        return {"sentiment": sentiment, "score": float(round(score, 3)), "context_emoji": found_emoji}

# 싱글톤 인스턴스
model = SentimentModel()
