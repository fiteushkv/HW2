document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('analyze-form');
    const textInput = document.getElementById('text-input');
    const submitBtn = document.getElementById('submit-btn');
    const btnText = document.querySelector('.btn-text');
    const loader = document.querySelector('.loader');
    
    const resultBox = document.getElementById('result-box');
    const sentimentIcon = document.getElementById('sentiment-icon');
    const sentimentText = document.getElementById('sentiment-text');
    const scoreValue = document.getElementById('score-value');
    const progressFill = document.getElementById('progress-fill');

    // 기분에 따른 이모티콘 및 CSS 클래스 매핑
    const emotionsMap = {
        'Positive': { icon: '😍', class: 'status-positive' },
        'Negative': { icon: '🤬', class: 'status-negative' },
        'Neutral':  { icon: '🤔', class: 'status-neutral' }
    };

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const text = textInput.value.trim();
        if (!text) return;

        // 1. 시각적 로딩 상태 처리
        btnText.style.display = 'none';
        loader.style.display = 'block';
        submitBtn.disabled = true;
        form.style.opacity = '0.7';
        
        // 결과창 초기화 작업
        progressFill.style.width = '0%';
        resultBox.classList.remove('status-positive', 'status-negative', 'status-neutral');
        
        try {
            // 2. FastAPI 서버로 분석 요청 보내기
            const response = await fetch('/api/v1/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: text })
            });

            if (!response.ok) throw new Error('Network error from API');

            const data = await response.json();
            const sentiment = data.sentiment;
            const score = data.score;
            const contextEmoji = data.context_emoji; // 백엔드에서 생성해준 문맥 이모지를 받아옴!
            
            // 3. UI 업데이트 및 애니메이션 동작 설정 시작
            const emotionConfig = emotionsMap[sentiment] || emotionsMap['Neutral'];
            
            // 박스 애니메이션 재실행 트릭 (reflow)
            resultBox.classList.remove('hidden');
            resultBox.style.animation = 'none';
            void resultBox.offsetWidth; 
            resultBox.style.animation = 'slideUp 0.6s ease-out forwards';
            
            // 텍스트 및 클래스 삽입 (여기서 하드코딩된 이모지 대신 서버가 준 이모지를 사용!)
            sentimentIcon.textContent = contextEmoji;
            sentimentIcon.style.animation = 'none';
            void sentimentIcon.offsetWidth;
            sentimentIcon.style.animation = 'pop 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.3) forwards';

            sentimentText.textContent = sentiment;
            resultBox.classList.add(emotionConfig.class);

            
            // 점수를 기반으로 게이지 바 부드럽게 채우기
            const percentage = (score * 100).toFixed(1);
            scoreValue.textContent = `${percentage}%`;
            
            setTimeout(() => {
                progressFill.style.width = `${percentage}%`;
            }, 100); // UI 렌더링 후 약간의 딜레이를 주어 애니메이션 극대화

        } catch (error) {
            console.error('Analysis failed:', error);
            alert('서버 응답 오류! 서버(FastAPI)가 제대로 실행 중인지 확인해주세요.');
        } finally {
            // 4. 로딩 상태 해제 처리
            btnText.style.display = 'block';
            loader.style.display = 'none';
            submitBtn.disabled = false;
            form.style.opacity = '1';
        }
    });
});
