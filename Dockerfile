# 베이스 이미지: 가볍고 최적화된 python slim 버전 사용
FROM python:3.11-slim

# 환경 변수 설정
# PYTHONDONTWRITEBYTECODE: 파이썬이 .pyc 파일을 쓰지 않도록 설정 (용량 최적화)
# PYTHONUNBUFFERED: 파이썬 출력이 버퍼링 없이 즉시 출력되도록 설정 (로그 확인 용이)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 작업 디렉토리 설정
WORKDIR /app

# 운영체제 레벨의 패키지 업데이트 및 필요한 시스템 패키지 설치 (컨테이너 경량화를 위해 설치 후 캐시 삭제)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 패키지 설치 최적화: requirements.txt만 먼저 복사하여 종속성 설치 (Docker 빌드 캐시 활용)
COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 전체 복사 (app 폴더 및 파일들)
COPY . .

# FastAPI 서버가 사용할 8000번 포트 노출
EXPOSE 8000

# 컨테이너 실행 시 uvicorn을 이용해 실행되도록 설정
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
