# PDF 파일 기반 RAG 고급 기법

IBK 증권보고서(삼성전자/SK하이닉스)를 활용한 실전 RAG 파이프라인 강의 교재입니다.
2시간 라이브 강의용으로 설계되었으며, 슬라이드(이론) + 노트북(실습) 구성입니다.

## 프로젝트 구조

```
rag_lecture/
├── rag_lecture_part1_f.ipynb              # Part 1~2: 데이터/평가셋 + PDF 추출 비교 + Base RAG
├── rag_lecture_part2_f.ipynb              # Part 3~5: 하이브리드 검색 + Multi-Query + Reranking
├── IBK 증권보고서_삼성전자_SK하이닉스.pdf     # 실험 데이터 (26페이지)
├── PDF 파일 기반 RAG 고급 기법.pdf          # 강의 슬라이드 (8장)
├── PDF 파일 기반 RAG 고급 기법.pptx         # 강의 슬라이드 원본
├── pyproject.toml                         # Poetry 의존성 정의
├── poetry.lock                            # Poetry 잠금 파일
├── requirements.txt                       # pip 의존성 정의
└── .gitignore
```

> `splits_v2.pkl`은 Part 1 노트북 실행 시 자동 생성되며, `.gitignore`에 의해 저장소에서 제외됩니다.

## 강의 흐름 (총 120분)

| 구간 | 내용 | 슬라이드 | 노트북 | 시간 |
|------|------|---------|--------|------|
| 오프닝 | RAG 개요 + 왜 필요한가 | 1장 | - | 10분 |
| Part 1 | 데이터 소개 + 평가셋 설계 (12개 질문) | - | part1_f | 10분 |
| Part 2 | PDF 추출 3종 비교 (PyMuPDF / 4LLM / VLM) + Chunking | 2~3장 | part1_f | 35분 |
| 쉬는 시간 | - | - | - | 5분 |
| Part 3 | BM25 + Ensemble (하이브리드 검색) | 4장 | part2_f | 20분 |
| Part 4 | Multi-Query Retrieval (질문 확장) | 5장 | part2_f | 15분 |
| Part 5 | Cross-Encoder Reranking (정밀 재정렬) | 6장 | part2_f | 20분 |
| 마무리 | 체크리스트 + Q&A | 7~8장 | - | 5분 |

## 강의 내용

### Part 1: 데이터 & 평가셋 (`part1_f.ipynb` 앞부분)
- IBK 증권보고서 PDF 구조 확인 (26페이지, 표 다수 포함)
- 재무/투자의견/비교 카테고리 12개 질문 + 정답 설계
- 평가 지표: 정확도(exact/partial/fail), 근거성(grounded + 근거 스니펫), 속도

### Part 2: PDF 추출 방식 비교 + Base RAG (`part1_f.ipynb` 뒷부분)
- **PyMuPDFLoader**: Raw 텍스트 추출 (빠르지만 표 구조 손실)
- **PyMuPDF4LLMLoader**: Markdown 변환 (구조 보존 시도)
- **VLM (GPT-4o)**: 이미지 기반 시각적 해석 (표/차트 정확도 최고)
- 동일 페이지(표 포함)에서 3종 로더의 추출 결과 비교
- Chunking 파라미터 실험 (chunk_size: 300 / 700 / 1500)
- 3종 추출본으로 동일 조건 FAISS RAG → 12개 질문 정확도·근거성 비교

### Part 3: 하이브리드 검색 (`part2_f.ipynb` 앞부분)
- **FAISS**: 의미(semantic) 기반 벡터 검색의 한계
- **BM25**: 키워드 빈도 기반 검색 (TF-IDF 개선) 원리
- **EnsembleRetriever + RRF**: 두 검색 결과를 순위 기반 융합
- 동일 질문에 FAISS / BM25 / Ensemble 검색 결과 비교 + 페이지 overlap 분석
- 각 Retriever별 RAG 답변 정확도 비교

### Part 4: Multi-Query Retrieval (`part2_f.ipynb` 중간)
- 표현 불일치(Vocabulary Mismatch) 문제와 해결
- `MultiQueryRetriever.from_llm()`으로 질문 자동 확장
- `llm_chain`으로 확장된 쿼리 직접 확인
- 기본 Retriever vs Multi-Query Retriever 검색 범위 비교
- 로깅(DEBUG)으로 생성된 확장 쿼리 확인

### Part 5: Cross-Encoder Reranking (`part2_f.ipynb` 뒷부분)
- Bi-Encoder(1차 검색) vs Cross-Encoder(2차 정밀 재정렬) 구조 비교
- **bge-reranker-v2-m3**: Rerank 전후 순위 변동 시각화
- top_n 파라미터와 정밀도-재현율 Trade-off
- CPU 기준 문서 수별 Rerank 소요 시간 실측
- Rerank 전/후 RAG 답변 비교

## 데이터셋

### IBK 증권보고서_삼성전자_SK하이닉스.pdf
- **내용**: IBK투자증권 삼성전자·SK하이닉스 실적 리포트
- **페이지**: 26페이지
- **특징**: 분기별 실적 표, 사업부별 매출/영업이익, 투자의견 등
- **주요 수치**:
  - 삼성전자 4Q25 매출액: 93.8조원, 영업이익: 20.1조원
  - SK하이닉스 4Q25 영업이익: 19.17조원
  - 삼성전자 목표주가: 240,000원

## 설치 방법

### Poetry (권장)

```bash
# Poetry 설치 (없는 경우)
curl -sSL https://install.python-poetry.org | python3 -

# 의존성 설치
poetry install

# Jupyter 커널 등록
poetry add ipykernel
poetry run python -m ipykernel install --user --name rag-lecture --display-name "RAG Lecture"
```

### pip

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux

pip install -r requirements.txt
python -m ipykernel install --user --name rag-lecture --display-name "RAG Lecture"
```

### 환경 변수

`.env` 파일에 OpenAI API 키를 설정합니다:

```
OPENAI_API_KEY=sk-...
```

## 실행 순서

1. **rag_lecture_part1_f.ipynb** 를 순서대로 실행
   - Part 1: PDF 확인 + 12개 질문·정답 평가셋 설계
   - Part 2: 3종 추출(PyMuPDF / 4LLM / VLM) → 청킹 → Base RAG 비교
   - `splits_v2.pkl` 자동 저장 (Part 3~5에서 사용)

2. **rag_lecture_part2_f.ipynb** 를 순서대로 실행
   - Part 3: FAISS vs BM25 vs Ensemble 비교
   - Part 4: MultiQueryRetriever 데모 (질문 확장 확인)
   - Part 5: Cross-Encoder Reranking 데모

## 기술 스택

| 분야 | 기술 |
|------|------|
| PDF 추출 | PyMuPDFLoader, PyMuPDF4LLMLoader, VLM (GPT-4o) |
| 텍스트 분할 | RecursiveCharacterTextSplitter |
| 임베딩 | BAAI/bge-m3 (HuggingFace) |
| 벡터 검색 | FAISS |
| 키워드 검색 | BM25 |
| 하이브리드 검색 | EnsembleRetriever (RRF) |
| 질문 확장 | MultiQueryRetriever |
| 리랭킹 | BAAI/bge-reranker-v2-m3 (Cross-Encoder) |
| LLM | GPT-4o (ChatOpenAI) |
| 의존성 관리 | Poetry / pip |

## 라이선스

이 교재는 교육 목적으로 제작되었습니다.
