# ./Dockerfile

FROM python:3.10-slim

# 1. 작업 디렉토리 설정
WORKDIR /app

# 2. requirements 설치
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# 3. 전체 코드 및 .env 복사
COPY . .    
# .env 포함

# 4. FastAPI 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
