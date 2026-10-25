"""
Automated Tests for Evaluation Metrics and Feedback Engine.
"""

import unittest
import os
from src.evaluation import (
    compute_precision_at_k,
    compute_recall_at_k,
    compute_mrr,
    evaluate_system
)
from src.recommender import SmartLibRecommender
from src.feedback import FeedbackTracker


class TestEvaluationMetrics(unittest.TestCase):
    def test_precision_at_k(self):
        retrieved = ["A", "B", "C", "D", "E"]
        ground_truth = ["B", "D", "X", "Y"]
        
        # In top 5, B and D are relevant -> 2 / 5 = 0.4
        p5 = compute_precision_at_k(retrieved, ground_truth, k=5)
        self.assertEqual(p5, 0.4)
        
        # In top 2, only B is relevant -> 1 / 2 = 0.5
        p2 = compute_precision_at_k(retrieved, ground_truth, k=2)
        self.assertEqual(p2, 0.5)

        # Empty ground truth should yield 0.0
        self.assertEqual(compute_precision_at_k(retrieved, [], k=5), 0.0)

    def test_recall_at_k(self):
        retrieved = ["A", "B", "C", "D", "E"]
        ground_truth = ["B", "D", "X", "Y"]  # 4 total relevant
        
        # In top 5, 2 of 4 relevant retrieved -> 2 / 4 = 0.5
        r5 = compute_recall_at_k(retrieved, ground_truth, k=5)
        self.assertEqual(r5, 0.5)

    def test_mrr(self):
        # First relevant item is at rank 2 ("B") -> 1/2 = 0.5
        retrieved = ["A", "B", "C", "D", "E"]
        ground_truth = ["B", "D"]
        self.assertEqual(compute_mrr(retrieved, ground_truth), 0.5)

        # First relevant item at rank 1 ("A") -> 1/1 = 1.0
        self.assertEqual(compute_mrr(["A", "B"], ["A"]), 1.0)

        # No relevant items retrieved -> 0.0
        self.assertEqual(compute_mrr(["A", "B"], ["Z"]), 0.0)

    def test_system_benchmark(self):
        """Execute full system benchmark and verify metric properties."""
        rec = SmartLibRecommender(data_path="data/library_resources.csv")
        eval_res = evaluate_system(rec, k=5)
        
        summary = eval_res["summary"]
        self.assertGreaterEqual(summary["mean_precision_at_k"], 0.40)
        self.assertGreaterEqual(summary["mean_recall_at_k"], 0.50)
        self.assertGreaterEqual(summary["mean_mrr"], 0.80)
        self.assertEqual(summary["failure_test_cases"], 1)


class TestFeedbackTracker(unittest.TestCase):
    def setUp(self):
        self.test_feedback_file = "data/test_feedback_tmp.json"
        if os.path.exists(self.test_feedback_file):
            os.remove(self.test_feedback_file)
        self.tracker = FeedbackTracker(storage_path=self.test_feedback_file)

    def tearDown(self):
        if os.path.exists(self.test_feedback_file):
            os.remove(self.test_feedback_file)

    def test_feedback_logging_and_precision(self):
        self.tracker.record_feedback("machine learning", "RES-AI-012", "Deep Learning", is_relevant=True)
        self.tracker.record_feedback("machine learning", "RES-CS-001", "Algorithms", is_relevant=False)
        self.tracker.record_feedback("machine learning", "RES-AI-013", "Hands-On ML", is_relevant=True)

        metrics = self.tracker.compute_feedback_metrics()
        self.assertEqual(metrics["total_feedbacks"], 3)
        self.assertEqual(metrics["relevant_count"], 2)
        self.assertEqual(metrics["irrelevant_count"], 1)
        self.assertEqual(metrics["user_precision"], 66.7)

        df = self.tracker.get_feedback_df()
        self.assertEqual(len(df), 3)


if __name__ == "__main__":
    unittest.main()
