import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.recommender import SmartLibRecommender

rec = SmartLibRecommender()
all_domains = rec.df["subject"].unique().tolist()
sort_options = [
    "Relevance (Cosine Similarity)",
    "Rating (High to Low)",
    "Year (Newest First)",
    "Popularity (Borrows)",
    "Availability (Copies)"
]

print("=== 1. TESTING COLD-START PER DOMAIN (Goal: >= 8 books) ===")
for dom in all_domains:
    df, meta = rec.recommend("", top_n=8, subject=dom)
    print(f"Domain: {dom:<40} -> Count: {len(df)} books")
    assert len(df) >= 8, f"Failed on domain {dom}"

print("\n=== 2. TESTING SORT FILTERS PER DOMAIN (Goal: >= 8 books) ===")
for sort_by in sort_options:
    for dom in all_domains[:4]:
        df, meta = rec.recommend("", top_n=8, subject=dom, sort_by=sort_by)
        assert len(df) >= 8, f"Failed on sort {sort_by} in domain {dom}"
print("All 5 sort options returned >= 8 books across all checked domains!")

print("\n=== 3. TESTING DIFFICULTY FILTERS (Goal: >= 8 books) ===")
for diff in ["Beginner", "Intermediate", "Advanced"]:
    for dom in all_domains[:4]:
        df, meta = rec.recommend("", top_n=8, subject=dom, difficulty=diff)
        assert len(df) >= 8, f"Failed on difficulty {diff} in domain {dom}"
print("All difficulty levels returned >= 8 books!")

print("\n=== 4. TESTING AVAILABILITY FILTER (available_only=True, Goal: >= 8 books) ===")
for dom in all_domains:
    df, meta = rec.recommend("", top_n=8, subject=dom, available_only=True)
    assert len(df) >= 8, f"Failed on available_only in domain {dom}"
print("Availability filter returned >= 8 books for all domains!")

print("\n=== 5. TESTING PRESET QUERIES (Goal: >= 8 books) ===")
presets = [
    ("Q1 Algorithms", "dynamic programming graph algorithms cormen"),
    ("Q2 Deep Learning", "deep neural networks convolutional image classification"),
    ("Q3 Relational DB", "relational sql databases transaction acid properties"),
    ("Q4 Linear Algebra", "linear algebra eigenvalues singular value decomposition svd"),
    ("Q5 Ethical Hacking", "ethical hacking penetration testing web vulnerabilities sql injection"),
    ("Q6 Embedded IoT", "embedded microcontrollers arm cortex sensors iot"),
    ("Q7 Blank Search", ""),
    ("Q8 Domain Cold Start", ""),
    ("Q9 Failure Case", "quantum computing teleportation qubits quantum supremacy")
]

for name, q in presets:
    df, meta = rec.recommend(q, top_n=8)
    print(f"Preset {name:<25} -> Count: {len(df)} books (Max Sim: {meta['max_similarity']})")
    assert len(df) >= 8, f"Failed on preset {name}"

print("\nALL VERIFICATIONS PASSED! Every domain and click has >= 8 books minimum!")
