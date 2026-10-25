"""
SmartLib AI - Relevance Feedback Engine
Tracks user explicit feedback (Relevant / Irrelevant / Bookmarked) in session state
and calculates real-time user-perceived Precision.
"""

import json
import os
import pandas as pd
from datetime import datetime

FEEDBACK_FILE = "data/user_feedback_log.json"


class FeedbackTracker:
    """Manages student relevance feedback transparently."""

    def __init__(self, storage_path: str = FEEDBACK_FILE):
        self.storage_path = storage_path
        self.feedback_records = []
        self.load_existing_feedback()

    def load_existing_feedback(self):
        """Load past feedback from JSON log if available."""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    self.feedback_records = json.load(f)
            except Exception:
                self.feedback_records = []

    def record_feedback(self, query: str, resource_id: str, title: str, is_relevant: bool, comment: str = ""):
        """Record a single feedback entry."""
        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "query": query,
            "resource_id": resource_id,
            "title": title,
            "is_relevant": is_relevant,
            "rating_label": "Relevant (Thumbs Up)" if is_relevant else "Not Relevant (Thumbs Down)",
            "comment": comment
        }
        self.feedback_records.append(entry)
        self._save_to_disk()

    def _save_to_disk(self):
        """Persist feedback records to disk."""
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        try:
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump(self.feedback_records, f, indent=2)
        except Exception as e:
            print(f"Warning: could not save feedback: {e}")

    def get_feedback_df(self) -> pd.DataFrame:
        """Return feedback log as a pandas DataFrame."""
        if not self.feedback_records:
            return pd.DataFrame(columns=["timestamp", "query", "resource_id", "title", "rating_label", "comment"])
        return pd.DataFrame(self.feedback_records)

    def compute_feedback_metrics(self) -> dict:
        """Compute live empirical user precision from logged feedback."""
        if not self.feedback_records:
            return {
                "total_feedbacks": 0,
                "relevant_count": 0,
                "irrelevant_count": 0,
                "user_precision": 0.0
            }
        total = len(self.feedback_records)
        relevant = sum(1 for f in self.feedback_records if f["is_relevant"])
        irrelevant = total - relevant
        user_precision = round((relevant / total) * 100, 1)
        return {
            "total_feedbacks": total,
            "relevant_count": relevant,
            "irrelevant_count": irrelevant,
            "user_precision": user_precision
        }
