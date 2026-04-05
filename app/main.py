from fastapi import FastAPI
from app.api.endpoints import analyze

def create_app() -> FastAPI:
    app = FastAPI(
        title="Sentiment Analysis API",
        description="MLOps 파이프라인 구축을 위한 FastAPI 기반 감정 분석 웹 서버",
        version="1.0.0"
    )

    # API 라우터 등록
    app.include_router(analyze.router, prefix="/api/v1/analyze", tags=["Sentiment Analysis"])

    @app.get("/")
    def health_check():
        return {
            "status": "healthy",
            "message": "Sentiment Analysis API is running. Visit /docs for Swagger UI."
        }
        
    return app

app = create_app()
