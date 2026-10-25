import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.recommender import SmartLibRecommender
from src.evaluation import evaluate_system

print("Running SmartLib AI Benchmark Evaluation...")
rec = SmartLibRecommender()
eval_res = evaluate_system(rec, k=5)

print("\n--- PER-QUERY METRICS ---")
print(eval_res["query_results_df"][["query_id", "domain", "precision_at_k", "recall_at_k", "mrr", "max_similarity", "is_fallback"]].to_string())

print("\n--- MACRO SUMMARY (In-Domain Queries) ---")
for k, v in eval_res["summary"].items():
    print(f"{k}: {v}")
