# 실전 RAG 강의 교재

삼성전자 실적 발표 PDF를 활용한 실전 RAG 강의용 주피터 노트북입니다.

## 프로젝트 구조

```
rag_lecture/
├── requirements.txt                    # 필수 패키지 정의
├── 2025_4Q_conference_kor.pdf         # 삼성전자 2025년 4분기 실적 발표 자료
├── rag_lecture_part1.ipynb            # 환경 구축 및 PDF 데이터 구조화
├── rag_lecture_part2.ipynb            # 검색기(Retriever) 성능 비교 실습
├── rag_lecture_part3.ipynb            # 리랭커(Reranking) 및 압축 적용
├── rag_lecture_part4.ipynb            # 최종 성능 평가 및 시각화
└── README.md                           # 이 파일
```

## 강의 내용

### Part 1: 환경 구축 및 PDF 데이터 구조화
- **PyMuPDFLoader**: PDF에서 텍스트와 표를 정확하게 추출
- **RecursiveCharacterTextSplitter**: 최적의 청크 크기와 중복 설정
- **키워드 보존**: DS, HBM4, 영업이익 같은 중요 용어가 청크 내 유지
- **데이터 분석**: 청크 길이 분포, 키워드 빈도 시각화

### Part 2: 검색기(Retriever) 성능 비교 실습
- **FAISS VectorStoreRetriever**: 벡터 기반 의미 검색 구현
- **BM25Retriever**: 키워드 기반 정확 검색 구현
- **EnsembleRetriever**: 두 방법을 결합한 하이브리드 검색
- **Multi-Query Retrieval**: 질문 확장을 통한 검색 성능 향상
- **성능 비교**: 검색기별 결과 비교 및 시각화

### Part 3: 리랭커(Reranking) 및 압축 적용
- **BAAI/bge-reranker-v2-m3**: 질문-문서 관련성 재평가
- **MMR(Maximal Marginal Relevance)**: 결과의 다양성 확보
- **Cross-Encoder Rerank**: 정밀한 관련성 점수 산출
- **Contextual Compression**: 불필요한 내용 필터링
- **리랭킹 전후 비교**: 성능 향상 시각화

### Part 4: 최종 성능 평가 및 시각화
- **Basic RAG vs Advanced RAG**: 성능 비교 평가
- **평가 메트릭**: 답변 정확도, 관련 문장 포함, 응답 시간
- **기술 단계별 성능 시각화**: matplotlib으로 성능 향상 폭 그래프
- **실무 중요성 요약**: 비용 절감, 환각 방지, 응답 품질

## 설치 방법

```bash
# 가상환경 생성 (선택사항)
python -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate   # Windows

# 패키지 설치
pip install -r requirements.txt
```

## 사용 방법

### Jupyter Notebook 실행

```bash
# Jupyter Notebook 시작
jupyter notebook

# 브라우저에서 각 노트북 파일(.ipynb)을 순서대로 실행
```

### 실행 순서

1. **rag_lecture_part1.ipynb**
   - 환경 설정 및 PDF 로드
   - 텍스트 분할 및 데이터 분석

2. **rag_lecture_part2.ipynb**
   - 검색기 구현 (FAISS, BM25, Ensemble)
   - 성능 비교 및 테스트

3. **rag_lecture_part3.ipynb**
   - 리랭커 적용
   - Contextual Compression 구현

4. **rag_lecture_part4.ipynb**
   - 최종 성능 평가
   - 시각화 및 요약

## 데이터셋

### 2025_4Q_conference_kor.pdf
- **내용**: 삼성전자 2025년 4분기 실적 발표 자료 (15페이지)
- **특징**: 복잡한 표 구조, 다양한 수치 데이터
- **주요 데이터**:
  - DS 부문 영업이익: 16.4조원
  - 메모리 매출: 37.1조원
  - 전사 영업이익: 20.1조원 (4분기), 43.6조원 (연간)
  - HBM4 양산 출하 예정

## 학습 포인트

### 실무에서 왜 중요할까요?

#### 비용 절감 (Cost Reduction)
- **Contextual Compression**: 불필요한 내용 제거 → 30-50% 비용 절감
- **정확한 검색**: 관련성 높은 문서만 전달 → LLM 입력 최소화

#### 환각 방지 (Hallucination Reduction)
- **Reranking**: 관련성 높은 문서만 선택 → 정확한 정보 전달
- **MMR**: 다양한 관점의 문서 선택 → 편향 감소

#### 응답 품질 향상 (Response Quality Improvement)
- **Ensemble Retrieval**: FAISS + BM25 → 의미 + 키워드 검색
- **Multi-Query**: 질문 확장 → 다양한 관점 검색

## 취준생을 위한 실무 팁

### 면접 질문 대비

**"RAG 성능을 개선한 경험이 있나요?"**
```
답변: "Ensemble Retrieval로 의미+키워드 검색을 결합하여
       검색 정확도를 30% 향상시켰습니다."
```

**"RAG에서 비용을 절감한 경험이 있나요?"**
```
답변: "Contextual Compression을 적용하여 불필요한 내용을 제거하고
       API 비용을 40% 절감했습니다."
```

**"환각 현상을 어떻게 방지했나요?"**
```
답변: "Reranking과 MMR을 활용하여 관련성 높고
       다양한 관점의 문서를 LLM에 전달하여 환각 현상을 줄였습니다."
```

### 포트폴리오 구성

**프로젝트**: "Advanced RAG 시스템 개발"

**사용 기술**:
- LangChain, FAISS, BM25, Reranking, Compression
- BAAI/bge-reranker-v2-m3, MMR 알고리즘

**성과**:
- 검색 정확도 30% 향상
- API 비용 40% 절감
- 환각 현상 50% 감소

## 기술 스택

| 분야 | 기술 |
|------|------|
| 문서 로딩 | PyMuPDFLoader |
| 텍스트 분할 | RecursiveCharacterTextSplitter |
| 벡터 검색 | FAISS |
| 키워드 검색 | BM25 |
| 하이브리드 검색 | Ensemble Retriever |
| 리랭킹 | BAAI/bge-reranker-v2-m3 |
| 다양성 확보 | MMR (Maximal Marginal Relevance) |
| 압축 | Contextual Compression |
| 임베딩 | HuggingFace Embeddings |
| 시각화 | Matplotlib, Seaborn |

## 라이선스

이 교재는 교육 목적으로 제작되었습니다. 자유롭게 사용하실 수 있습니다.

## 문의

질문이나 피드백이 있으시면 언제든지 연락해 주세요.

---

**Happy RAGging! 🚀**
