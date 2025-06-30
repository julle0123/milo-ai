## 📚 목차

- [🧠 프로젝트 소개](#-마음을-기억하는-챗봇-milo)
- [👀 서비스 소개](#-서비스-소개)
- [📅 프로젝트 기간](#-프로젝트-기간)
- [📎 GitHub 주소 (Frontend / Backend / AI)](#-github-주소-frontend--backend--ai)
- [⭐ 주요 기능](#-주요-기능)
- [🔁 서비스 동작 구조](#-서비스-동작-구조)
- [⚙ 시스템 아키텍처](#-시스템-아키텍처)
- [📊 ERD 다이어그램](#-erd-다이어그램)
- [🖥 화면 구성 미리보기](#-화면-구성-미리보기)
- [🛠 기술 스택](#-기술-스택)
- [🧼 데이터 전처리 과정](#-데이터-전처리-과정)
- [📂 FastAPI 서버 디렉토리 구조](#-fastapi-서버-디렉토리-구조)
- [🛠 설치 및 실행 (AI 서버 FastAPI)](#-설치-및-실행-ai-서버-fastapi)
- [📌 사용 예시](#-사용-예시)
- [🤯 트러블슈팅 요약](#-트러블슈팅-요약)
- [👨‍👩‍👧‍👦 팀원 역할](#-팀원-역할)
- [📄 라이선스](#-라이선스)
---

# 🧠 마음을 기억하는 챗봇, Milo  
> (Agent Tool 기반 AI 정서 케어 챗봇 서비스)

<div align="center">
  <img src="https://github.com/user-attachments/assets/699397f4-0360-4981-9ad1-b683d0a29239" width="400px"/>
  <p><b>시작 화면</b>
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

## 📎 GitHub 주소 (Frontend / Backend / AI)
- Frontend : https://github.com/suhwan87/milo-fe <br>
- Backend (Spring) : https://github.com/suhwan87/milo-be <br>
- AI Server (FastAPI) : https://github.com/julle0123/milo-ai

---

## ⭐ 주요 기능

| 구분         | 설명                                                                 |
|--------------|----------------------------------------------------------------------|
| 상담 챗봇     | 감정을 분석하고 위로의 말을 건네는 GPT 기반 상담 챗봇              |
| 역할극 챗봇   | 이름/관계/말투/상황을 설정한 감정 리허설 챗봇                       |
| 감정 리포트   | 일일/월간 감정 흐름 요약 리포트 생성 및 저장                        |
| 회복 문장     | 유사 감정 기반 회복 문장 저장 보관함 구성                          |
| 회복 컨텐츠   | 대화 중 사용자의 감정 변동에 따라 감정 회복 컨텐츠 추천               |
| 시각화 기능   | 감정 이모지 캘린더 / 월간 감정 레이더 차트                         |
| 위험 감지     | 감정 분석 결과 위기 신호 시 안정 응답 + 기관 연결                  |

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

![Image](https://github.com/user-attachments/assets/fd6b5494-61b9-4d5f-880b-b53722c78ba2)

---

## 📊 ERD 다이어그램

![Image](https://github.com/user-attachments/assets/5bac60fe-1517-4ae1-b945-2fb4a214836b)

---

## 🖥 화면 구성 미리보기

<table>
<tr>
  <td align="center"><img src="https://github.com/user-attachments/assets/870979ed-ebfc-422d-a4d0-31590f179da4" width="200"/><br/>로그인</td>
  <td align="center"><img src="https://github.com/user-attachments/assets/1267be99-cc0c-490e-8cc8-350f0e0b997f" width="200"/><br/>메인 화면</td>
  <td align="center"><img src="https://github.com/user-attachments/assets/8c13527b-d711-47de-944e-1cab9f73b29f" width="200"/><br/>비밀번호 찾기</td>
  <td align="center"><img src="https://github.com/user-attachments/assets/9e59fb33-529d-4cd2-9d9c-09f62f4c4392" width="200"/><br/>아이디 찾기</td>
  <td align="center"><img src="https://github.com/user-attachments/assets/2bae1163-dcc2-4117-9bcc-9c92a0294070" width="200"/><br/>회원가입</td>
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
  <td align="center"><img src="https://github.com/user-attachments/assets/093747ae-02be-417b-bf0a-e9a16db6e221" width="200"/><br/>문의하기</td>
  <td align="center"><img src="https://github.com/user-attachments/assets/a1f8c570-74de-41d8-b9f0-60d2c10993de" width="200"/><br/>회원탈퇴</td>
</tr>
</table>
---

## 🛠 기술 스택

| 구분 | 사용 기술 |
|------|-----------|
| **Frontend** | ![](https://img.shields.io/badge/HTML-E34F26?style=for-the-badge&logo=html5&logoColor=white) ![](https://img.shields.io/badge/CSS-1572B6?style=for-the-badge&logo=css3&logoColor=white) ![](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black) ![](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black) ![](https://img.shields.io/badge/Chart.js-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white) <br> ![](https://img.shields.io/badge/axios-5A29E4?style=for-the-badge&logo=axios&logoColor=white) ![](https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white)|
| **Backend** | ![](https://img.shields.io/badge/Java-ED8B00?style=for-the-badge&logo=openjdk&logoColor=white) ![](https://img.shields.io/badge/SpringBoot-6DB33F?style=for-the-badge&logo=springboot&logoColor=white) ![](https://img.shields.io/badge/JPA-007396?style=for-the-badge&logo=hibernate&logoColor=white) ![](https://img.shields.io/badge/SpringSecurity-6DB33F?style=for-the-badge&logo=springsecurity&logoColor=white) ![](https://img.shields.io/badge/Lombok-EC722E?style=for-the-badge&logo=lombok&logoColor=white) <br>![](https://img.shields.io/badge/Swagger-85EA2D?style=for-the-badge&logo=swagger&logoColor=black) ![](https://img.shields.io/badge/RESTful_API-000000?style=for-the-badge) ![](https://img.shields.io/badge/CORS_Global-FFB300?style=for-the-badge) ![](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)|
| **AI Server** | ![](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white) ![](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![](https://img.shields.io/badge/Pydantic-007EC6?style=for-the-badge) ![](https://img.shields.io/badge/SQLAlchemy-FFCA28?style=for-the-badge) ![](https://img.shields.io/badge/Uvicorn-000000?style=for-the-badge) |
| **AI & LLM** | ![](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white) ![](https://img.shields.io/badge/LangChain-000000?style=for-the-badge) ![](https://img.shields.io/badge/AgentTool-0A0A0A?style=for-the-badge) ![](https://img.shields.io/badge/RAG-000000?style=for-the-badge) |
| **Database** | ![](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white) ![](https://img.shields.io/badge/Qdrant-1A1A1A?style=for-the-badge) |
| **Infra / Deploy** | ![](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white) ![](https://img.shields.io/badge/NaverCloud-03C75A?style=for-the-badge&logo=naver&logoColor=white) |
| **개발 도구** | ![](https://img.shields.io/badge/IntelliJ-000000?style=for-the-badge&logo=intellijidea&logoColor=white) ![](https://img.shields.io/badge/VSCode-007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white) ![](https://img.shields.io/badge/Google_Colab-F9AB00?style=for-the-badge&logo=googlecolab&logoColor=white) |
| **기획 / 디자인 도구** | ![](https://img.shields.io/badge/Notion-000000?style=for-the-badge&logo=notion&logoColor=white) ![](https://img.shields.io/badge/Figma-F24E1E?style=for-the-badge&logo=figma&logoColor=white) |
| **협업 도구** | ![](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white) |

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
| 4. 텍스트 분리 | 멀티턴 데이터를 싱글턴 데이터로 분리 |
| 5. 특수문자 제거 | `[^ㄱ-ㅎ가-힣a-zA-Z0-9\s]` 패턴으로 클렌징 |
| 6. 분류용 데이터셋 생성 | 감정 분석 학습용 `text`, `label` 컬럼 구성 |

---
### 🧠 전처리한 데이터를 토대로 만든 감정분류 모델(hugging-face)
- KCELECTRA 활용
- 만들어진 모델로 데이터 전체 감정분류 적용
- https://huggingface.co/Seonghaa/emotion-koelectra  --> 만든 감정분류 모델
---
### 🎯 최종 전처리 샘플

```csv
text,label
"요즘은 너무 지치고 잠도 잘 못 자요.","불안"
"기분이 좋고 뿌듯해요. 다 잘 될 것 같아요.","기쁨"
"그 사람이 또 나를 무시했어. 너무 화가 나.","분노"
```
---
### 🎒 임베딩 후 qdrant 벡터 DB 저장
- openai 3-small-textembedding 모델 활용하여 감정 + 사용자입력 데이터 30만 문장 임베딩
- metadata에 입력에 대한 응답 등을 포함하여 qdrant 벡터 DB에 저장하여 rag에 활용
---

## 📂 FastAPI 서버 디렉토리 구조
--> 프론트와 백엔드는 다른곳에 기록됨.

```
milp-ai/
├──.github
│ └── workflows                        # git-action
├──app
│  ├── api/                            # 라우터 정의
│  │ ├── chat.py                       # 상담 챗봇 API
│  │ ├── chat_end.py                   # 채팅 종료 API
│  │ ├── log.py                        # 로그 저장 API
│  │ ├── report.py                     # 리포트 기록 API
│  │ └── roleplay.py                   # 역할극 API
│  ├── core/                           # 공통 설정 모듈
│  │ ├── client.py                     # openai 설정
│  │ ├── config.py                     # Settings(.env)
│  │ └── db.py                         # DB 연결 / 세션 관리
│  ├── models/                         # SQLAlchemy 모델
│  │ ├── __init__.py                   # Python 패키지 인식용 파일 (import 가능하게 함)
│  │ ├── base.py                       # Base 선언
│  │ ├── chat_log.py                   # 상담 대화 기록DB
│  │ ├── daily_emotion_report.py       # 하루 감정 리포트DB
│  │ ├── monthly_emotion_summary.py    # 월간 감정 리포트DB
│  │ ├── rolecharacter.py              # 역할DB
│  │ ├── role_play_log.py              # 역할 챗봇 대화 기록 DB
│  │ ├── schema.py                     # 공통 Pydantic 스키마
│  │ └── user.py                       # 유저DB
│  ├── prompt/                         # GPT 시스템 프롬프트 정의
│  │ ├── emotion_prompt_emotional.txt  # 공감형(F) 프롬프트
│  │ ├── emotion_prompt_practical.txt  # 조언형(T) 프롬프트
│  │ └── roleplay_prompt.txt           # 역할 챗봇 프롬프트
│  ├── services/                       # 비즈니스 로직 처리
│  │ ├── agent.py                      # AgentTool 기반 응답 생성
│  │ ├── agent_roleplay.py             # 역할극 응답 처리
│  │ ├── emotion_service.py            # 감정 분석/백터화
│  │ ├── memory.py                     # 기억 공간
│  │ ├── rag_service.py                # rag 기능
│  │ └── report_service.py             # 감정 리포트 저장 및 업데이트
│  ├── main.py                         # FastAPI 앱 진입점
├── .env                               # 환경 변수 설정 파일
├── .gitignore                         # git push 무시
├── Dockerfile                         # FastAPI Docker 배포 환경
├── README.md                          # 프로젝트 설명 파일
├── docker-compose.yml                 # 전체 서비스 연동 설정
└── requirements.txt                   # 의존성 목록
```
---
## 🛠 설치 및 실행 (AI 서버 FastAPI)

```bash
# 1. 가상환경 생성 및 활성화 (선택)
python -m venv venv 
source venv/bin/activate

# 2. 라이브러리 설치
pip install -r requirements.txt

# 3. FastAPI 실행
uvicorn main:app --reload --port 8000
```
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

> 여러 상담 데이터와 유사한 대화 3건 추출 후 GPT 프롬프트에 포함

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
- 3일 이상 하루 감정 분석 리포트가 작성 시 감정 아카이브 작성 -> `monthly_emotion_summary_TB`

---

## 🤯 트러블슈팅 요약

| 문제 | 원인 | 해결 |
|------|------|------|
| agent 구성시  create_react_agent()에서 agent_scratchpad 변수에 문제 발생 | 변수가 문자열로 전달되는데, 실제로는 메시지 리스트를 기대하기 때문에 발생, `create_react_agent()`는 특정한 프롬프트 구조를 요구, `agent_scratchpad`는 `MessagesPlaceholder`가 아닌 일반 문자열 플레이스홀더여야 함. | create_react_agent에서 create_openai_functions_agent로 전환 |
| async def 기반으로 서비스 함수 수정 이후, 일부 DB 호출이나 OpenAI API 응답이 정상 동작하지 않음. | SQLAlchemy의 Session 객체는 기본적으로 동기이며, 이를 async 함수에서 그대로 사용할 경우 오류 발생. | 비동기 처리를 도입하되, DB 작업은 여전히 sync 방식으로 유지하거나 AsyncSession을 명확히 도입해야 함. 또는 asyncio.run() 사용을 피하고 명시적으로 await 처리해야 함. |
| TrainingArguments 클래스의 evaluation_strategy 인자에서 오류가 발생 | TrainingArguments 클래스의 evaluation_strategy 인자가 eval_strategy로 변경되어 기존 코드에서 evaluation_strategy를 사용하면 다음과 같은 오류가 발생 | 코드에서 TrainingArguments를 정의할 때 evaluation_strategy를 eval_strategy로 변경하면 문제가 해결! |

---

## 👨‍👩‍👧‍👦 팀원 역할

| 이름 | 역할 | GitHub                                       |
|------|------|----------------------------------------------|
| 김성하 | PM / 데이터 전처리 / DB 설계 / ERD 설계 / AI 모델링 / FastAPI 서버 | [@julle0123](https://github.com/julle0123)   |
| 정수한 | 데이터 수집 / 데이터 전처리 / 프롬프트 설계 / AI 모델링 / FastAPI 서버 | [@s2-honey](https://github.com/s2-honey) |
| 김수환 | 프론트엔드 구현 / UI 구성 / 디자인 / Spring Boot API / DB 연동  | [@suhwan87](https://github.com/suhwan87)     |
| 김서연 | 프론트엔드 구현 / UI 구성 / 디자인 /  Spring Boot API / DB 연동  | [@kimseoyeon21](https://github.com/kimseoyeon21) |

---
## 📄 라이선스

본 프로젝트는 오픈된 학습 자료로 누구나 자유롭게 사용할 수 있습니다.  
