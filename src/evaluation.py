"""
SmartLib AI - Evaluation Suite
Computes genuine, non-fabricated information retrieval metrics:
Precision@K, Recall@K, and Mean Reciprocal Rank (MRR) across predefined test queries.
Includes documented ground-truth labels, positive query benchmarks, and failure cases.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any


# Predefined evaluation benchmark with manually curated ground truth relevance labels
BENCHMARK_QUERIES = [
    {
        "query_id": "Q1",
        "query_text": "dynamic programming graph algorithms cormen",
        "domain": "Computer Science & Algorithms",
        "description": "Student seeking foundational and advanced algorithmic problem solving (CLRS, graph traversal, DP).",
        "ground_truth_relevant_ids": [
            "RES-CS-001",  # Introduction to Algorithms (CLRS)
            "RES-CS-003",  # Competitive Programming 4
            "RES-CS-055",  # Graph Algorithms (Spark & Neo4j)
            "RES-CS-002",  # Data Structures and Algorithm Analysis in C++
            "RES-CS-127",  # The Algorithm Design Manual (Skiena)
            "RES-CS-126",  # Algorithms in a Nutshell
            "RES-CS-128",  # Data Structures Laboratory Practice Manual
            "RES-CS-129",  # Purely Functional Data Structures
        ],
        "is_failure_case": False,
        "notes": "Positive test case: Core curriculum algorithms."
    },
    {
        "query_id": "Q2",
        "query_text": "deep neural networks convolutional image classification",
        "domain": "Artificial Intelligence & Data Science",
        "description": "Student preparing for a deep learning computer vision lab or research.",
        "ground_truth_relevant_ids": [
            "RES-AI-012",  # Deep Learning (Goodfellow)
            "RES-AI-015",  # Computer Vision: Algorithms and Applications
            "RES-AI-013",  # Hands-On Machine Learning (Scikit-Learn/TF)
            "RES-AI-081",  # Deep Learning with PyTorch
            "RES-AI-076",  # Graph Neural Networks
            "RES-CS-120",  # Computer Vision: Models, Learning, and Inference
            "RES-AI-144",  # Deep Learning with Python (Chollet)
            "RES-AI-145",  # Deep Learning Lab with PyTorch
            "RES-BIO-052", # Deep Learning for the Life Sciences
            "RES-AI-146",  # Generative Models & Diffusion
        ],
        "is_failure_case": False,
        "notes": "Positive test case: Deep learning and computer vision."
    },
    {
        "query_id": "Q3",
        "query_text": "relational sql databases transaction acid properties",
        "domain": "Database Systems",
        "description": "Student revising transaction management, concurrency, and SQL fundamentals.",
        "ground_truth_relevant_ids": [
            "RES-CS-006",  # Database System Concepts (Silberschatz)
            "RES-CS-009",  # Designing Data-Intensive Applications (Kleppmann)
            "RES-CS-083",  # Database Internals (Alex Petrov)
            "RES-CS-090",  # Learning SQL (Beaulieu)
            "RES-CS-133",  # Database Design for Mere Mortals
            "RES-CS-134",  # SQL and Relational Database Systems Lab Workbook
            "RES-CS-135",  # High Performance MySQL
        ],
        "is_failure_case": False,
        "notes": "Positive test case: Relational databases & systems."
    },
    {
        "query_id": "Q4",
        "query_text": "linear algebra eigenvalues singular value decomposition svd",
        "domain": "Mathematics",
        "description": "Student studying linear algebra foundations required for machine learning and data science.",
        "ground_truth_relevant_ids": [
            "RES-MA-025",  # Linear Algebra and Its Applications (Strang)
            "RES-MA-026",  # Mathematics for Machine Learning
            "RES-MA-029",  # Convex Optimization (Boyd)
            "RES-MA-153",  # Linear Algebra Done Right (Axler)
            "RES-MA-154",  # Computational Linear Algebra with Python
            "RES-MA-155",  # Matrix Computations (Golub)
            "RES-MA-211",  # Linear Algebra: Principles, Systems, and Practice
        ],
        "is_failure_case": False,
        "notes": "Positive test case: Linear algebra & matrix decompositions."
    },
    {
        "query_id": "Q5",
        "query_text": "ethical hacking penetration testing web vulnerabilities sql injection",
        "domain": "Cybersecurity & Networks",
        "description": "Student learning application penetration testing and vulnerability analysis.",
        "ground_truth_relevant_ids": [
            "RES-SEC-032",  # The Web Application Hacker's Handbook
            "RES-SEC-064",  # Hacking: The Art of Exploitation
            "RES-SEC-031",  # Cryptography and Network Security
            "RES-SEC-097",  # Black Hat Python
            "RES-SEC-122",  # The Web Application Defender's Cookbook
            "RES-SEC-162",  # Ethical Hacking and Penetration Testing Lab Manual (Weidman)
            "RES-SEC-163",  # Web Security Testing and OWASP Top 10 Lab Guide
            "RES-SEC-233",  # Ethical Hacking & Systems Security (Vol 38)
            "RES-SEC-221",  # Ethical Hacking & Systems Security (Vol 26)
        ],
        "is_failure_case": False,
        "notes": "Positive test case: Application cybersecurity & ethical hacking."
    },
    {
        "query_id": "Q6",
        "query_text": "quantum computing teleportation qubits quantum supremacy",
        "domain": "Quantum Computing (Out-of-Domain)",
        "description": "Deliberate edge case: query outside the current engineering catalog syllabus.",
        "ground_truth_relevant_ids": [],  # Intentionally 0 in current catalog
        "is_failure_case": True,
        "notes": "Deliberate failure / out-of-domain case: Demonstrates honest fallback handling without hallucination."
    },
    {
        "query_id": "Q7",
        "query_text": "embedded microcontrollers arm cortex sensors iot",
        "domain": "Electrical & Electronics Engineering",
        "description": "Student looking for hands-on ARM microcontroller and hardware interfacing texts.",
        "ground_truth_relevant_ids": [
            "RES-EEE-046",  # Embedded Systems: ARM Cortex-M (Valvano)
            "RES-EEE-045",  # The Art of Electronics (Horowitz & Hill)
            "RES-EEE-108",  # Designing Embedded Hardware (Catsoulis)
            "RES-MEC-113",  # Mechatronics: Bolton
            "RES-EEE-171",  # Arduino and ARM Embedded Systems Prototyping Lab Guide
            "RES-EEE-170",  # Internet of Things: Principles and Paradigms (Buyya)
            "RES-EEE-240",  # Embedded Systems & IoT Practice
            "RES-EEE-252",  # Embedded Systems & IoT Practice Vol 36
        ],
        "is_failure_case": False,
        "notes": "Positive test case: Microcontroller & embedded hardware."
    }
]


def compute_precision_at_k(retrieved_ids: List[str], ground_truth_ids: List[str], k: int = 5) -> float:
    """Precision@K = (Number of relevant items in top K) / K"""
    if k <= 0:
        return 0.0
    top_k = retrieved_ids[:k]
    if not ground_truth_ids:
        return 0.0
    relevant_in_top_k = sum(1 for item in top_k if item in ground_truth_ids)
    return round(relevant_in_top_k / k, 4)


def compute_recall_at_k(retrieved_ids: List[str], ground_truth_ids: List[str], k: int = 5) -> float:
    """Recall@K = (Number of relevant items in top K) / (Total relevant items in ground truth)"""
    if not ground_truth_ids:
        return 0.0
    top_k = retrieved_ids[:k]
    relevant_in_top_k = sum(1 for item in top_k if item in ground_truth_ids)
    return round(relevant_in_top_k / len(ground_truth_ids), 4)


def compute_mrr(retrieved_ids: List[str], ground_truth_ids: List[str]) -> float:
    """
    Mean Reciprocal Rank (MRR):
    1 / rank of the first relevant document retrieved.
    Returns 0.0 if no relevant items are retrieved.
    """
    if not ground_truth_ids:
        return 0.0
    for rank, item in enumerate(retrieved_ids, start=1):
        if item in ground_truth_ids:
            return round(1.0 / rank, 4)
    return 0.0


def evaluate_system(recommender_instance, k: int = 5) -> Dict[str, Any]:
    """
    Runs the full evaluation benchmark across all test queries using actual recommender output.
    Computes genuine per-query metrics and macro-averages.
    """
    results_list = []
    
    for b in BENCHMARK_QUERIES:
        query_text = b["query_text"]
        gt_ids = b["ground_truth_relevant_ids"]
        is_failure = b["is_failure_case"]
        
        # Query recommender with k results
        recs, meta = recommender_instance.recommend(query_text, top_n=k)
        retrieved_ids = recs["resource_id"].tolist() if not recs.empty else []
        top_title = recs.iloc[0]["title"] if not recs.empty else "No results"
        
        p_at_k = compute_precision_at_k(retrieved_ids, gt_ids, k=k)
        r_at_k = compute_recall_at_k(retrieved_ids, gt_ids, k=k)
        mrr = compute_mrr(retrieved_ids, gt_ids)
        
        results_list.append({
            "query_id": b["query_id"],
            "query_text": query_text,
            "domain": b["domain"],
            "is_failure_case": is_failure,
            "ground_truth_count": len(gt_ids),
            "retrieved_count": len(retrieved_ids),
            "top_match_title": top_title,
            "precision_at_k": p_at_k,
            "recall_at_k": r_at_k,
            "mrr": mrr,
            "max_similarity": meta.get("max_similarity", 0.0),
            "is_fallback": meta.get("is_fallback", False),
            "notes": b["notes"]
        })
        
    df_eval = pd.DataFrame(results_list)
    
    # Calculate macro averages for normal in-domain queries
    in_domain_df = df_eval[~df_eval["is_failure_case"]]
    
    avg_precision = in_domain_df["precision_at_k"].mean()
    avg_recall = in_domain_df["recall_at_k"].mean()
    avg_mrr = in_domain_df["mrr"].mean()
    
    overall_summary = {
        "k": k,
        "total_test_queries": len(BENCHMARK_QUERIES),
        "in_domain_queries": len(in_domain_df),
        "failure_test_cases": 1,
        "mean_precision_at_k": round(avg_precision, 4),
        "mean_recall_at_k": round(avg_recall, 4),
        "mean_mrr": round(avg_mrr, 4),
        "timestamp": "Evaluated on local dataset"
    }
    
    return {
        "query_results_df": df_eval,
        "summary": overall_summary
    }
