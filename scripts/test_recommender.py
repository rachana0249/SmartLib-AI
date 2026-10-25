import time
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.recommender import SmartLibRecommender

t0 = time.time()
print("Initializing SmartLibRecommender...")
rec = SmartLibRecommender()
print(f"Initialized in {time.time() - t0:.2f} seconds.")

# Test query 1
t1 = time.time()
results, meta = rec.recommend("machine learning neural networks", top_n=5)
print(f"Query executed in {time.time() - t1:.4f} seconds.")
print(f"Max similarity: {meta['max_similarity']}")
print("Top 5 Results:")
for i, row in results.iterrows():
    print(f"[{i+1}] {row['resource_id']}: {row['title']} (Score: {row['similarity_score']:.4f})")
    print(f"    Explanation: {row['explanation']}")
    print(f"    Subject: {row['subject']} | Topic: {row['topic']}")
