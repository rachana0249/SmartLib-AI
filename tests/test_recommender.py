"""
Automated Unit and Integration Tests for SmartLib AI Recommender Engine.
"""

import unittest
import os
import pandas as pd
from src.recommender import SmartLibRecommender, preprocess_text, build_corpus_representation


class TestSmartLibRecommender(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.recommender = SmartLibRecommender(data_path="data/library_resources.csv")

    def test_dataset_size_and_schema(self):
        """Verify that the dataset contains at least 100 items with all required columns."""
        df = self.recommender.df
        self.assertGreaterEqual(len(df), 100, "Catalog must contain at least 100 resources.")
        
        required_columns = [
            "resource_id", "title", "authors", "subject", "topic",
            "resource_type", "difficulty_level", "description", "keywords",
            "publication_year", "location_shelf", "total_copies",
            "available_copies", "simulated_rating", "simulated_borrow_count"
        ]
        for col in required_columns:
            self.assertIn(col, df.columns, f"Missing required column: {col}")

    def test_preprocessing(self):
        """Verify text normalization and lowercase conversion."""
        raw = "Machine Learning & AI: 101 -- Systems!"
        cleaned = preprocess_text(raw)
        self.assertEqual(cleaned, "machine learning ai 101 systems")
        self.assertEqual(preprocess_text(""), "")
        self.assertEqual(preprocess_text(None), "")

    def test_cold_start_recommendations(self):
        """Verify cold start output when no history or query is provided."""
        cold = self.recommender.get_cold_start_recommendations(top_n=5)
        self.assertEqual(len(cold), 5)
        self.assertTrue(all(cold["is_cold_start"]))
        self.assertIn("academic_score", cold.columns)
        # Ratings should be valid numbers between 1.0 and 5.0
        self.assertTrue((cold["simulated_rating"] <= 5.0).all())
        self.assertTrue((cold["simulated_rating"] >= 1.0).all())

    def test_empty_query_handling(self):
        """Verify that empty or whitespace query safely triggers cold start."""
        recs, meta = self.recommender.recommend("", top_n=5)
        self.assertTrue(meta["is_empty"])
        self.assertEqual(len(recs), 5)

        recs_spaces, meta_spaces = self.recommender.recommend("    ", top_n=5)
        self.assertTrue(meta_spaces["is_empty"])
        self.assertEqual(len(recs_spaces), 5)

    def test_content_recommendation_and_ranking(self):
        """Verify TF-IDF and Cosine similarity scoring on known technical query."""
        recs, meta = self.recommender.recommend("compiler lexical parsing syntax trees", top_n=5)
        self.assertFalse(meta["is_empty"])
        self.assertGreater(meta["max_similarity"], 0.15)
        self.assertGreaterEqual(len(recs), 1)
        
        top_title = recs.iloc[0]["title"].lower()
        # Should retrieve the Dragon Book or Theory/Compiler text
        self.assertTrue("compiler" in top_title or "computation" in top_title)
        self.assertIn("matching_terms", recs.columns)
        self.assertIn("explanation", recs.columns)

    def test_subject_filter(self):
        """Verify that subject filter strictly restricts returned recommendations."""
        target_subject = "Mathematics"
        recs, _ = self.recommender.recommend(
            query="linear equations calculus",
            top_n=5,
            subject=target_subject
        )
        self.assertGreaterEqual(len(recs), 1)
        for _, row in recs.iterrows():
            self.assertEqual(row["subject"], target_subject)

    def test_availability_filter(self):
        """Verify that availability filter returns only resources with available copies > 0."""
        recs, _ = self.recommender.recommend(
            query="algorithms data structures",
            top_n=10,
            available_only=True
        )
        self.assertGreaterEqual(len(recs), 1)
        for _, row in recs.iterrows():
            self.assertGreater(row["available_copies"], 0)

    def test_difficulty_filter(self):
        """Verify difficulty level filtering."""
        target_diff = "Beginner"
        recs, _ = self.recommender.recommend(
            query="python programming basics",
            top_n=5,
            difficulty=target_diff
        )
        self.assertGreaterEqual(len(recs), 1)
        for _, row in recs.iterrows():
            self.assertEqual(row["difficulty_level"], target_diff)

    def test_unknown_terms_fallback(self):
        """Verify that completely unknown out-of-vocabulary query handles gracefully without crashing."""
        query = "xyzqwertyunknownword12345"
        recs, meta = self.recommender.recommend(query, top_n=5)
        self.assertTrue(meta["is_fallback"])
        self.assertGreaterEqual(len(recs), 1)


if __name__ == "__main__":
    unittest.main()
