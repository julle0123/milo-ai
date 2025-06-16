from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "테스트 성공"}