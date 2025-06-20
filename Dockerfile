# ./Dockerfile

FROM python:3.10-slim

# 작업 디렉토리 설정
WORKDIR /app

# requirements.txt와 프로젝트 파일 복사
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

# FastAPI 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

