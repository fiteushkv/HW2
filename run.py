import uvicorn

if __name__ == "__main__":
    # uvicorn을 사용하여 FastAPI 앱 실행
    # reload=True 옵션은 개발 모드에서 코드가 변경될 때 자동으로 서버를 재시작합니다.
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
