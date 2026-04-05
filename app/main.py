from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.endpoints import analyze
import os

def create_app() -> FastAPI:
    app = FastAPI(
        title="Sentiment Analysis API",
        description="MLOps 파이프라인 구축을 위한 FastAPI 기반 감정 분석 웹 서버",
        version="1.0.0"
    )

    # API 라우터 등록
    app.include_router(analyze.router, prefix="/api/v1/analyze", tags=["Sentiment Analysis"])

    # 정적 파일 서빙 (정적 파일이 담길 static 폴더 마운트)
    os.makedirs("app/static", exist_ok=True)
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    @app.get("/", summary="Serve beautiful UI")
    def serve_frontend():
        # 루트에 접근하면 브라우저에 index.html을 내보냅니다.
        return FileResponse("app/static/index.html")
        
    return app

app = create_app()
