## 📚 목차

- [🧠 프로젝트 소개](#-마음을-기억하는-챗봇-milo)
- [👀 서비스 소개](#-서비스-소개)
- [📅 프로젝트 기간](#-프로젝트-기간)
- [📎 프론트 / 백엔드 / AI 주소](#-프론트--백엔드--ai-주소)
- [⭐ 주요 기능](#-주요-기능)
- [🔁 서비스 동작 구조](#-서비스-동작-구조)
- [⚙ 시스템 아키텍처](#-시스템-아키텍처)
- [📊 ERD 다이어그램](#-erd-다이어그램)
- [🖥 화면 구성 미리보기](#-화면-구성-미리보기)
- [📌 사용 예시](#-사용-예시)
- [🧼 데이터 전처리 과정](#-데이터-전처리-과정)
- [🛠 기술 스택](#-기술-스택)
- [🛠 설치 및 실행 (AI 서버 FastAPI)](#-설치-및-실행-ai-서버-fastapi)
- [📂 FastAPI 서버 디렉토리 구조](#-fastapi-서버-디렉토리-구조)
- [🤯 트러블슈팅 요약](#-트러블슈팅-요약)
- [👨‍👩‍👧‍👦 팀원 역할](#-팀원-역할)
- [📄 라이선스](#-라이선스)
---

# 🧠 마음을 기억하는 챗봇, Milo  
> (Agent Tool 기반 AI 정서 케어 챗봇 서비스)

<div align="center">
  <img src="https://github.com/user-attachments/assets/699397f4-0360-4981-9ad1-b683d0a29239" width="400px"/>
  <p><b>시작 화면</b><br/>당신의 감정을 들려주세요, Milo가 함께 할게요</p>
</div>

---

## 👀 서비스 소개
- **서비스명**: Milo  
- **서비스 설명**:  
  정서 표현이 어려운 사람들을 위한 **AI 기반 정서지원 챗봇 플랫폼**  
  사용자의 감정을 기억하고, 분석하고, 회복 문장과 위로 메시지를 제공합니다.  
  상담형/리허설형 챗봇, 감정 아카이브, 분석 리포트까지 포함된 **개인 맞춤형 감정 도우미**입니다.

---

## 📅 프로젝트 기간
2025.05.14 ~ 2025.07.10 (약 8주)

---

## 📎 프론트 / 백엔드 / AI 주소
백엔드 : https://github.com/suhwan87/milo-be <br>
프론트 : https://github.com/suhwan87/milo-fe <br>
AI : https://github.com/julle0123/milo-ai

---

## ⭐ 주요 기능
- 정서 지원 챗봇
- 감정 흐름 분석 및 자동 데일리 요약 리포트 생성
- 감정 회복 문장 저장 및 폴더 기반 관리 기능
- 역할 시뮬레이션 챗봇(이름/관계/말투/성격/상황 설정 기반 감정 리허설)
- 감정 이모지 캘린더 + 월간 감정 레이더 차트 시각화
- 사용자 감정에 맞는 콘텐츠 추천
- 사용자 정서 위험 탐지 → GPT 안정 응답 + 상담기관 안내

---

## 🔁 서비스 동작 구조

1. 프론트 → 백엔드(Spring)로 사용자 발화 전송
2. Spring → FastAPI로 사용자 질문/기록 전달
3. FastAPI(GPT Agent) → 감정 분석, 키워드 추출
4. Qdrant로 유사 감정 사례 검색 → GPT가 회복 피드백 생성
5. FastAPI → 감정 리포트 + 회복 문장 추천 응답
6. Spring → DB 저장 후 프론트로 최종 응답 전달
7. 리포트/감정 흐름/회복 문장 시각화에 반영됨

---

## ⚙ 시스템 아키텍처

![Image](https://github.com/user-attachments/assets/310b3b20-e602-4dcb-9ba0-0ca0d78588d5)

---

## 📊 ERD 다이어그램

![Image](https://github.com/user-attachments/assets/5bac60fe-1517-4ae1-b945-2fb4a214836b)

---

## 🖥 화면 구성 미리보기

<table>
<tr>
  <td align="center"><img src="https://github.com/user-attachments/assets/870979ed-ebfc-422d-a4d0-31590f179da4" width="200"/><br/>로그인</td>
  <td align="center"><img src="https://github.com/user-attachments/assets/1267be99-cc0c-490e-8cc8-350f0e0b997f" width="200"/><br/>메인 화면</td>
  <td align="center"><img src="https://github.com/user-attachments/assets/58ab9ae5-37a1-42c2-afec-01888b107022" width="200"/><br/>비밀번호 찾기</td>
  <td align="center"><img src="https://github.com/user-attachments/assets/2aaeef16-529b-4248-be7a-7423663cad39" width="200"/><br/>아이디 찾기</td>
  <td align="center"><img src="https://github.com/user-attachments/assets/8a03fe04-8796-4920-b3e0-38fd86bc38fa" width="200"/><br/>회원가입</td>
</tr>
<tr>
  <td align="center"><img src="https://github.com/user-attachments/assets/131eabc3-1203-475e-9ae5-4fc6e6644509" width="200"/><br/>상담 챗봇</td>
  <td align="center"><img src="https://github.com/user-attachments/assets/208a6a29-181b-48a7-bf38-5922b6440954" width="200"/><br/>하루 감정 리포트</td>
  <td align="center"><img src="https://github.com/user-attachments/assets/4ef059ef-d83c-4dab-8f8e-5139f9ae6921" width="200"/><br/>하루 감정 리포트 달력</td>
  <td align="center"><img src="https://github.com/user-attachments/assets/a181baf0-acf8-4908-b7b3-60290632c7fa" width="200"/><br/>감정 아카이브</td>
  <td align="center"><img src="https://github.com/user-attachments/assets/1865d352-ae86-4296-b340-153552db38aa" width="200"/><br/>상담 스타일 변경</td>
</tr>
<tr>
  <td align="center"><img src="https://github.com/user-attachments/assets/d56c2abf-5a9f-4a9e-9796-a80acfa8a48c" width="200"/><br/>역할 정하기1</td>
  <td align="center"><img src="https://github.com/user-attachments/assets/e7d40ee6-46be-4564-9636-3cfaf4b37a45" width="200"/><br/>역할 정하기2</td>
  <td align="center"><img src="https://github.com/user-attachments/assets/48c8a5b5-54ed-4991-862e-397cf8fc7831" width="200"/><br/>역할 정하기3</td>
  <td align="center"><img src="https://github.com/user-attachments/assets/bd9a1012-7935-43f2-bc81-efc397ccf289" width="200"/><br/>역할 정하기4</td>
  <td align="center"><img src="https://github.com/user-attachments/assets/f204d50c-4c3c-477d-839f-fc79d4e2d8bb" width="200"/><br/>역할 정하기5</td>
</tr>
<tr>
  <td align="center"><img src="https://github.com/user-attachments/assets/c987293d-7871-4d9f-a35e-3a538936464f" width="200"/><br/>역할 챗봇</td>
  <td align="center"><img src="https://github.com/user-attachments/assets/209a2433-00f8-4a27-a192-ab89ce9701d8" width="200"/><br/>회복문장</td>
  <td align="center"><img src="https://github.com/user-attachments/assets/e637d784-c728-4e60-a484-7719377532f4" width="200"/><br/>설정</td>
</tr>
</table>

---

## 📌 사용 예시

### 💬 사용자가 Milo에게 입력한 문장

> "요즘 너무 불안하고 잠이 안 와요… 혼자 있는 게 무서워요."

---

### 🧠 1. 감정 분석 결과 (GPT + 벡터 처리)

- 주요 감정: `불안(0.91), 슬픔(0.68)`
- 대표 감정: `불안`

---

### 🔍 2. 유사 감정 사례 검색 (Qdrant + RAG)

> 과거 사용자가 기록한 유사 대화 3건 추출 후 GPT 프롬프트에 포함

---

### 💡 3. GPT 응답 예시

> "당신이 지금 느끼는 불안은 결코 가벼운 것이 아니에요.  
> 누군가에게 기대고 싶다는 감정은 자연스러운 거예요.  
> 너무 혼자 버티려고 하지 마세요. 함께 있어줄게요."

---

### 🗂️ 4. 자동 저장

- 상담 내용 → `chat_log_TB`
- 감정 분석 결과 → `daily_emotion_report_TB`
- GPT 응답 → 회복 문장 추천 또는 저장 유도

---

## 🧼 데이터 전처리 과정

### 📁 데이터 출처
- AI Hub 감성 대화 말뭉치
- CounselGPT 한국어 심리상담 데이터셋
- 하이닥 심리상담 Q&A 크롤링
- 감정 분류용 라벨 데이터 (기쁨, 슬픔, 분노, 불안, 상처, 당황 등)

---

### 🔍 전처리 단계 요약

| 단계 | 설명 |
|------|------|
| 1. 중복 제거 | 동일 문장 또는 유사도 0.95 이상 문장 필터링 |
| 2. 비어 있는 행 제거 | 질문 또는 응답이 누락된 row 제거 |
| 3. 감정 라벨 정제 | 대분류 감정만 추출 (예: "불안_긴장" → "불안") |
| 4. 텍스트 통합 | 사람문장1~3을 하나의 입력으로 통합 |
| 5. 특수문자 제거 | `[^ㄱ-ㅎ가-힣a-zA-Z0-9\s]` 패턴으로 클렌징 |
| 6. 분류용 데이터셋 생성 | 감정 분석 학습용 `text`, `label` 컬럼 구성 |

---

### 🧠 최종 전처리 샘플

```csv
text,label
"요즘은 너무 지치고 잠도 잘 못 자요.","불안"
"기분이 좋고 뿌듯해요. 다 잘 될 것 같아요.","기쁨"
"그 사람이 또 나를 무시했어. 너무 화가 나.","분노"
```
---
### 전처리한 데이터를 토대로 만든 학습 모델(hugging-face)
https://huggingface.co/Seonghaa/emotion-koelectra

---
## 🛠 기술 스택

| 구분 | 사용 기술 |
|------|-----------|
| **Frontend** | ![](https://img.shields.io/badge/HTML-E34F26?style=for-the-badge&logo=html5&logoColor=white) ![](https://img.shields.io/badge/CSS-1572B6?style=for-the-badge&logo=css3&logoColor=white) ![](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black) ![](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black) ![](https://img.shields.io/badge/Chart.js-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white) ![](https://img.shields.io/badge/axios-5A29E4?style=for-the-badge&logo=axios&logoColor=white) |
| **Backend (API)** | ![](https://img.shields.io/badge/Java-ED8B00?style=for-the-badge&logo=openjdk&logoColor=white) ![](https://img.shields.io/badge/SpringBoot-6DB33F?style=for-the-badge&logo=springboot&logoColor=white) ![](https://img.shields.io/badge/JPA-007396?style=for-the-badge&logo=hibernate&logoColor=white) ![](https://img.shields.io/badge/SpringSecurity-6DB33F?style=for-the-badge&logo=springsecurity&logoColor=white) |
| **Backend (AI)** | ![](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white) ![](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![](https://img.shields.io/badge/Pydantic-007EC6?style=for-the-badge) ![](https://img.shields.io/badge/SQLAlchemy-FFCA28?style=for-the-badge) ![](https://img.shields.io/badge/Uvicorn-000000?style=for-the-badge) |
| **AI & LLM** | ![](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white) ![](https://img.shields.io/badge/LangChain-000000?style=for-the-badge) ![](https://img.shields.io/badge/AgentTool-0A0A0A?style=for-the-badge) ![](https://img.shields.io/badge/RAG-000000?style=for-the-badge) |
| **Database** | ![](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white) ![](https://img.shields.io/badge/Qdrant-1A1A1A?style=for-the-badge) |
| **Infra / Deploy** | ![](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white) ![](https://img.shields.io/badge/NaverCloud-03C75A?style=for-the-badge&logo=naver&logoColor=white) |
| **개발 도구** | ![](https://img.shields.io/badge/IntelliJ-000000?style=for-the-badge&logo=intellijidea&logoColor=white) ![](https://img.shields.io/badge/VSCode-007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white) |
| **기획 / 디자인 도구** | ![](https://img.shields.io/badge/Notion-000000?style=for-the-badge&logo=notion&logoColor=white) ![](https://img.shields.io/badge/Figma-F24E1E?style=for-the-badge&logo=figma&logoColor=white) |
| **협업 도구** | ![](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white) |

---

## 🛠 설치 및 실행 (AI 서버 FastAPI)

bash
# 1. 가상환경 생성 및 활성화 (선택)
python -m venv venv <br>
source venv/bin/activate

# 2. 라이브러리 설치
pip install -r requirements.txt

# 3. FastAPI 실행
uvicorn main:app --reload --port 8000

---
## 📂 FastAPI 서버 디렉토리 구조
--> 프론트와 백엔드는 다른곳에 기록됨.

```
milp-ai/
├──.github
│ └── workflows # git-action
├──app
│  ├── api/ # 라우터 정의
│  │ ├── chat.py # 상담 챗봇 API
│  │ ├── chat_end.py # 채팅 종료 API
│  │ ├── log.py # 로그 저장 API
│  │ ├── report.py # 리포트 기록 API
│  │ └── roleplay.py # 역할극 API
│  ├── core/ # 공통 설정 모듈
│  │ ├── client.py # openai 설정
│  │ ├── config.py # Settings(.env)
│  │ └── db.py # DB 연결 / 세션 관리
│  ├── models/ # SQLAlchemy 모델
│  │ ├── __init__.py 
│  │ ├── base.py # Base 선언
│  │ ├── chat_log.py
│  │ ├── daily_emotion_report.py
│  │ ├── monthly_emotion_summary.py
│  │ ├── rolecharacter.py
│  │ ├── role_play_log.py
│  │ ├── schema.py # 공통 Pydantic 스키마
│  │ └── user.py
│  ├── prompt/ # GPT 시스템 프롬프트 정의
│  │ ├── emotion_prompt_emotional.txt
│  │ ├── emotion_prompt_practical.txt
│  │ └── roleplay_prompt.txt
│  ├── services/ # 비즈니스 로직 처리
│  │ ├── agent.py # AgentTool 기반 응답 생성
│  │ ├── agent_roleplay.py # 역할극 응답 처리
│  │ ├── emotion_service.py # 감정 분석/백터화
│  │ ├── memory.py # 기억 공간
│  │ ├── rag_service.py # rag
│  │ └── report_service.py # 감정 리포트 저장 및 업데이트
│  ├── main.py # FastAPI 앱 진입점
├── .env # 환경 변수 설정 파일
├── .gitignore # git push 무시
├── Dockerfile # FastAPI Docker 배포 환경
├── README.md
├── docker-compose.yml
└── requirements.txt # 의존성 목록
```
---


## 🤯 트러블슈팅 요약

| 문제 | 원인 | 해결 |
|------|------|------|
| 내용~~ | 내용~~ | 내용~~ |

---

## 👨‍👩‍👧‍👦 팀원 역할

| 이름 | 역할 | GitHub |
|------|------|--------|
| 김성하 | PM / AI 모델링 / 데이터 전처리 / DB 설계 / ERD 설계 / AI 모델링 / FastAPI 서버 | [@julle0123](https://github.com/julle0123) |
| 정수한 | AI 모델링 / 데이터 수집 / 데이터 전처리 / 프롬프트 설계 / AI 모델링 / FastAPI 서버 | - |
| 김수환 | 프론트엔드 구현 / UI 구성 / 디자인 / Spring Boot API / DB 연동  | - |
| 김서연 | 프론트엔드 구현 / UI 구성 / 디자인 /  Spring Boot API / DB 연동  | - |

---
## 📄 라이선스

본 프로젝트는 교육 목적의 팀 프로젝트로 진행되었으며,
외부 사용 시 사전 허가가 필요합니다.

