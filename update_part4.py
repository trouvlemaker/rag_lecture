#!/usr/bin/env python3
"""Part 4 노트북 간소화: RAGStage 2단계, retrieve_with_stage 새 파이프라인, 지표/시각화 축소"""
import json

with open("rag_lecture_part4.ipynb") as f:
    nb = json.load(f)

TOP_K, TOP_M, TOP_N = 15, 6, 3

for i, cell in enumerate(nb["cells"]):
    if cell["cell_type"] != "code":
        continue
    src = "".join(cell.get("source", []))

    # 1. RAGStage + EvaluationResult
    if "class RAGStage(Enum):" in src and "BASIC_FAISS" in src:
        new_src = '''# RAG 단계 열거형 (간소화: Basic vs Advanced)
class RAGStage(Enum):
    BASIC = "Basic RAG (Ensemble)"
    ADVANCED = "Advanced RAG (Ensemble+MMR+Reranker+Compression)"

# 평가 결과 데이터 클래스 (핵심 지표: 키워드 매칭)
@dataclass
class EvaluationResult:
    stage: RAGStage
    question: str
    retrieved_docs: List
    retrieval_time: float
    keyword_match_count: int
    keyword_match_rate: float

print("성능 평가 프레임워크 정의 완료!")
print("\\nRAG 단계 (간소화):")
for stage in RAGStage:
    print(f"  - {stage.value}")
'''
        cell["source"] = new_src.split("\n")
        cell["source"] = [line + "\n" for line in cell["source"]]
        if cell["source"]:
            cell["source"][-1] = cell["source"][-1].rstrip("\n")
        print("Updated RAGStage + EvaluationResult")
        continue

    # 2. retrieve_with_stage + evaluate_retrieval
    if "def retrieve_with_stage(" in src and "stage == RAGStage.BASIC_FAISS" in src:
        new_src = '''# 검색 함수 (새 파이프라인: Ensemble k=15 → MMR m=6 → Reranker n=3 → Compress)
def retrieve_with_stage(
    stage: RAGStage,
    question: str,
    top_k: int = 15,
    top_m: int = 6,
    top_n: int = 3,
) -> Tuple[List, float]:
    """각 RAG 단계별 검색 수행 (파이프라인: 1→2→3→4)"""
    start_time = time.time()

    if stage == RAGStage.BASIC:
        results = ensemble_retriever.invoke(question)[:top_n]
    else:
        # ADVANCED: Ensemble → MMR → Reranker → Compress
        faiss_vs = ensemble_retriever.retrievers[0].vectorstore
        candidates = [d for d, _ in faiss_vs.similarity_search_with_score(question, k=top_k)]
        mmr_out = mmr_reranker.rerank(question, candidates, embeddings, k=top_m)
        ce_out = cross_encoder_reranker.rerank(question, mmr_out, top_k=top_n)
        reranked = [mmr_out[idx] for idx, _, _ in ce_out]
        results = compressor.compress(reranked, question)

    retrieval_time = time.time() - start_time
    return results[:top_n], retrieval_time

# 평가 함수 (핵심 지표: 키워드 매칭)
def evaluate_retrieval(
    stage: RAGStage,
    question: str,
    keywords: List[str] = None
) -> EvaluationResult:
    """검색 성능 평가"""
    if keywords is None:
        keywords = ['DS', '영업이익', 'HBM4', '매출', '실적', '2025년 4분기', '삼성전자']
        keywords = [kw for kw in keywords if kw in question]
        if not keywords:
            keywords = ['삼성전자']

    docs, retrieval_time = retrieve_with_stage(stage, question)

    keyword_matches = sum(1 for doc in docs if any(kw in doc.page_content for kw in keywords))
    keyword_match_rate = keyword_matches / len(docs) if docs else 0

    return EvaluationResult(
        stage=stage,
        question=question,
        retrieved_docs=docs,
        retrieval_time=retrieval_time,
        keyword_match_count=keyword_matches,
        keyword_match_rate=keyword_match_rate
    )

print("평가 함수 정의 완료!")
'''
        cell["source"] = [line + "\n" for line in new_src.split("\n")]
        if cell["source"]:
            cell["source"][-1] = cell["source"][-1].rstrip("\n")
        print("Updated retrieve_with_stage + evaluate_retrieval")
        continue

    # 3. 평가 출력 - remove avg_doc_length, compression_rate, fix denominator
    if "result.keyword_match_count" in src and "result.avg_doc_length" in src:
        src = src.replace("print(f\"    - 평균 길이: {result.avg_doc_length:.0f}자\")\n", "")
        src = src.replace("        if result.compressed:\n            print(f\"    - 압축률: {result.compression_rate:.1f}%\")\n", "")
        cell["source"] = src.split("\n")
        cell["source"] = [line + "\n" for line in cell["source"]]
        if cell["source"]:
            cell["source"][-1] = cell["source"][-1].rstrip("\n")
        print("Updated evaluation print")
        continue

    # 4. calculate_stage_summary - simplify to keyword only
    if "def calculate_stage_summary" in src and "평균_검색_시간" in src:
        new_src = '''# 단계별 평균 성능 계산 (핵심 지표: 키워드 매칭)
def calculate_stage_summary(results: List[EvaluationResult]) -> pd.DataFrame:
    stage_data = []
    for stage in RAGStage:
        stage_results = [r for r in results if r.stage == stage]
        if stage_results:
            stage_data.append({
                '단계': stage.value,
                '평균_키워드_매칭_수': np.mean([r.keyword_match_count for r in stage_results]),
                '평균_키워드_매칭_율': np.mean([r.keyword_match_rate for r in stage_results]),
            })
    return pd.DataFrame(stage_data)

df_summary = calculate_stage_summary(all_results)
print("기술 단계별 성능 요약 (Basic vs Advanced):")
print("=" * 60)
print(df_summary.to_string(index=False))
'''
        cell["source"] = [line + "\n" for line in new_src.split("\n")]
        if cell["source"]:
            cell["source"][-1] = cell["source"][-1].rstrip("\n")
        print("Updated calculate_stage_summary")
        continue

    # 5. Fix evaluate_retrieval - remove avg_doc_length, compression_rate from return
    # (already done in #2)

    # 6. Update visualization to single Basic vs Advanced bar chart
    if "for stage in RAGStage" in src and "평균_키워드_매칭" in src and "plt." in src:
        # Find the visualization cell - simplify to 1 bar chart
        if "bar(" in src or "BarContainer" in str(cell.get("outputs", [])):
            new_src = '''# Basic vs Advanced 성능 비교 (막대그래프 1개)
basic_vals = [r.keyword_match_count for r in all_results if r.stage == RAGStage.BASIC]
adv_vals = [r.keyword_match_count for r in all_results if r.stage == RAGStage.ADVANCED]

fig, ax = plt.subplots(figsize=(8, 5))
labels = ['Basic RAG', 'Advanced RAG']
means = [np.mean(basic_vals) if basic_vals else 0, np.mean(adv_vals) if adv_vals else 0]
colors = ['skyblue', 'coral']
bars = ax.bar(labels, means, color=colors, edgecolor='black')
ax.set_ylabel('평균 키워드 매칭 수')
ax.set_title('Basic vs Advanced RAG 성능 비교 (키워드 매칭)')
for b, v in zip(bars, means):
    ax.text(b.get_x() + b.get_width()/2, b.get_height() + 0.05, f'{v:.2f}', ha='center', fontsize=12)
plt.tight_layout()
plt.show()
'''
            cell["source"] = [line + "\n" for line in new_src.split("\n")]
            if cell["source"]:
                cell["source"][-1] = cell["source"][-1].rstrip("\n")
            print("Updated visualization to Basic vs Advanced bar")
        continue

# Replace 4-subplot visualization with single Basic vs Advanced bar (uses df_summary)
for i, cell in enumerate(nb["cells"]):
    if cell["cell_type"] != "code":
        continue
    src = "".join(cell.get("source", []))
    if "axes[0, 0]" in src and "df_summary['평균_키워드_매칭_율']" in src and "axes[0, 1]" in src:
        new_src = '''# Basic vs Advanced 성능 비교 (막대그래프 1개 - 키워드 매칭)
basic_vals = [r.keyword_match_count for r in all_results if r.stage == RAGStage.BASIC]
adv_vals = [r.keyword_match_count for r in all_results if r.stage == RAGStage.ADVANCED]

fig, ax = plt.subplots(figsize=(8, 5))
labels = ['Basic RAG', 'Advanced RAG']
means = [np.mean(basic_vals) if basic_vals else 0, np.mean(adv_vals) if adv_vals else 0]
colors = ['skyblue', 'coral']
bars = ax.bar(labels, means, color=colors, edgecolor='black')
ax.set_ylabel('평균 키워드 매칭 수')
ax.set_title('Basic vs Advanced RAG 성능 비교 (키워드 매칭)')
for b, v in zip(bars, means):
    ax.text(b.get_x() + b.get_width()/2, b.get_height() + 0.05, f'{v:.2f}', ha='center', fontsize=12)
plt.tight_layout()
plt.show()
'''
        cell["source"] = [line + "\n" for line in new_src.split("\n")]
        if cell["source"]:
            cell["source"][-1] = cell["source"][-1].rstrip("\n")
        print("Replaced 4-subplot with single Basic vs Advanced bar")
        break

# Replace Basic vs Advanced 3-subplot with single bar (uses basic_results, advanced_results)
for i, cell in enumerate(nb["cells"]):
    if cell["cell_type"] != "code":
        continue
    src = "".join(cell.get("source", []))
    if "basic_results" in src and "advanced_results" in src and "axes[0]" in src and "basic_lengths" in src:
        new_src = '''# Basic vs Advanced 시각화 (키워드 매칭만)
basic_results = [r for r in all_results if r.stage == RAGStage.BASIC]
advanced_results = [r for r in all_results if r.stage == RAGStage.ADVANCED]

basic_keywords = [r.keyword_match_count for r in basic_results]
advanced_keywords = [r.keyword_match_count for r in advanced_results]

fig, ax = plt.subplots(figsize=(10, 5))
x = np.arange(len(test_questions))
width = 0.35
ax.bar(x - width/2, basic_keywords, width, label='Basic RAG', color='skyblue', edgecolor='black')
ax.bar(x + width/2, advanced_keywords, width, label='Advanced RAG', color='coral', edgecolor='black')
ax.set_xlabel('질문 번호')
ax.set_ylabel('키워드 매칭 수')
ax.set_title('Basic vs Advanced: 키워드 매칭 비교')
ax.set_xticks(x)
ax.set_xticklabels([str(i+1) for i in range(len(test_questions))])
ax.legend()
ax.grid(True, axis='y', alpha=0.3)
plt.tight_layout()
plt.show()
'''
        cell["source"] = [line + "\n" for line in new_src.split("\n")]
        if cell["source"]:
            cell["source"][-1] = cell["source"][-1].rstrip("\n")
        print("Replaced 3-subplot Basic vs Advanced with keyword-only chart")
        break

# Fix references to old RAGStage names
for i, cell in enumerate(nb["cells"]):
    if cell["cell_type"] != "code":
        continue
    src = "".join(cell.get("source", []))
    # BASIC_FAISS -> BASIC
    if "RAGStage.BASIC_FAISS" in src:
        cell["source"] = [line.replace("RAGStage.BASIC_FAISS", "RAGStage.BASIC") for line in cell["source"]]
        print("Fixed BASIC_FAISS reference")
    # Fix basic_results, advanced_results filters (already use ADVANCED)
    if "r.stage == RAGStage.ADVANCED" in src:
        pass  # OK
    if "r.stage == RAGStage.BASIC_FAISS" in src:
        cell["source"] = [line.replace("RAGStage.BASIC_FAISS", "RAGStage.BASIC") for line in cell["source"]]

with open("rag_lecture_part4.ipynb", "w") as f:
    json.dump(nb, f, ensure_ascii=False, indent=2)

print("Part 4 업데이트 완료!")
