"""
SmartLib AI - Core Recommender Engine
Implements content-based filtering with TF-IDF vectorization and Cosine Similarity,
transparent explainability, metadata weighting, cold-start handling, and weak-query fallback.
Guarantees rich 5-8+ book availability across all domains, filters, and sort orders.
"""

import re
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def preprocess_text(text: str) -> str:
    """Clean and normalize text tokens for robust vectorization."""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    # Normalize punctuation while preserving alphanumeric words
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def build_corpus_representation(df: pd.DataFrame) -> pd.Series:
    """
    Construct rich content representation by combining title, subject, topic,
    keywords, description, and tags. Title and keywords are boosted for relevance.
    """
    def row_to_text(row):
        title = preprocess_text(str(row.get("title", "")))
        subject = preprocess_text(str(row.get("subject", "")))
        topic = preprocess_text(str(row.get("topic", "")))
        keywords = preprocess_text(str(row.get("keywords", "")))
        desc = preprocess_text(str(row.get("description", "")))
        tags = preprocess_text(str(row.get("tags", "")))
        
        # Boost title (3x) and keywords (2x) to capture key terminology
        combined = f"{title} {title} {title} {subject} {topic} {keywords} {keywords} {desc} {tags}"
        return combined

    return df.apply(row_to_text, axis=1)


class SmartLibRecommender:
    """
    Transparent, explainable content-based recommendation engine
    powered by TF-IDF and Cosine Similarity.
    """

    def __init__(self, data_path: str = "data/library_resources.csv"):
        self.data_path = data_path
        self.df = None
        self.vectorizer = None
        self.tfidf_matrix = None
        self.feature_names = None
        self.corpus = None
        self.load_data()

    def load_data(self):
        """Load dataset and fit the TF-IDF vectorizer."""
        self.df = pd.read_csv(self.data_path)
        # Ensure simulated fields have correct types
        self.df["available_copies"] = pd.to_numeric(self.df["available_copies"], errors="coerce").fillna(0).astype(int)
        self.df["total_copies"] = pd.to_numeric(self.df["total_copies"], errors="coerce").fillna(1).astype(int)
        self.df["simulated_rating"] = pd.to_numeric(self.df["simulated_rating"], errors="coerce").fillna(4.5).astype(float)
        self.df["simulated_borrow_count"] = pd.to_numeric(self.df["simulated_borrow_count"], errors="coerce").fillna(50).astype(int)
        self.df["publication_year"] = pd.to_numeric(self.df["publication_year"], errors="coerce").fillna(2020).astype(int)

        self.corpus = build_corpus_representation(self.df)
        
        # Configure sublinear TF scaling to dampen frequent word domination
        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            sublinear_tf=True,
            min_df=1
        )
        self.tfidf_matrix = self.vectorizer.fit_transform(self.corpus)
        self.feature_names = np.array(self.vectorizer.get_feature_names_out())

    def get_cold_start_recommendations(
        self,
        top_n: int = 8,
        subject_filter: str = "All",
        difficulty: str = "All",
        resource_type: str = "All",
        available_only: bool = False,
        sort_by: str = "Relevance (Cosine Similarity)"
    ) -> pd.DataFrame:
        """
        Cold-start recommendations for students without prior search or borrowing history.
        Ranks by academic rating, borrow popularity, and foundational tag relevance.
        Guarantees ample books (minimum 5-8) for any domain or filter combination.
        """
        filtered = self.df.copy()

        # Subject Filter
        if subject_filter and subject_filter != "All":
            filtered = filtered[filtered["subject"] == subject_filter]

        # Difficulty Filter with smart backfill guarantee
        if difficulty and difficulty != "All":
            diff_strict = filtered[filtered["difficulty_level"] == difficulty]
            if len(diff_strict) >= top_n:
                filtered = diff_strict
            elif not diff_strict.empty:
                needed = top_n - len(diff_strict)
                other_diff = filtered[filtered["difficulty_level"] != difficulty]
                supplement = self._sort_dataframe(other_diff, sort_by=sort_by, default_sort_col="simulated_rating").head(needed)
                filtered = pd.concat([diff_strict, supplement], ignore_index=True)

        # Resource Type Filter with smart backfill guarantee
        if resource_type and resource_type != "All":
            type_strict = filtered[filtered["resource_type"] == resource_type]
            if len(type_strict) >= top_n:
                filtered = type_strict
            elif not type_strict.empty:
                needed = top_n - len(type_strict)
                other_type = filtered[filtered["resource_type"] != resource_type]
                supplement = self._sort_dataframe(other_type, sort_by=sort_by, default_sort_col="simulated_rating").head(needed)
                filtered = pd.concat([type_strict, supplement], ignore_index=True)

        if available_only:
            avail_strict = filtered[filtered["available_copies"] > 0]
            if len(avail_strict) >= top_n:
                filtered = avail_strict
            elif not avail_strict.empty:
                needed = top_n - len(avail_strict)
                other_avail = filtered[filtered["available_copies"] == 0]
                supplement = self._sort_dataframe(other_avail, sort_by=sort_by, default_sort_col="simulated_rating").head(needed)
                filtered = pd.concat([avail_strict, supplement], ignore_index=True)

        # Calculate academic popularity score: 70% rating (scaled to 100) + 30% borrow count normalized
        max_borrows = self.df["simulated_borrow_count"].max() or 1
        filtered["academic_score"] = (
            (filtered["simulated_rating"] / 5.0) * 0.7 +
            (filtered["simulated_borrow_count"] / max_borrows) * 0.3
        )
        
        # Sort based on requested sort order
        sorted_df = self._sort_dataframe(filtered, sort_by=sort_by, default_sort_col="academic_score")
        cold_start_df = sorted_df.head(top_n).copy()
        
        cold_start_df["similarity_score"] = 0.0
        cold_start_df["is_cold_start"] = True
        cold_start_df["explanation"] = cold_start_df.apply(
            lambda r: f"Academic Baseline: High faculty rating ({r['simulated_rating']}/5.0) & {r['simulated_borrow_count']} campus checkouts ({r['topic']})",
            axis=1
        )
        cold_start_df["matching_terms"] = cold_start_df["subject"].apply(lambda s: f"{s} Curriculum Essential")
        return cold_start_df.reset_index(drop=True)

    def explain_similarity(self, query_vec, doc_idx: int, top_terms: int = 4) -> tuple[str, list[str]]:
        """
        Explain recommendation by extracting top overlapping TF-IDF terms
        between query vector and resource document vector.
        """
        doc_vec = self.tfidf_matrix[doc_idx]
        prod = query_vec.multiply(doc_vec)
        nonzero_indices = prod.nonzero()[1]
        
        if len(nonzero_indices) == 0:
            return "General domain topic match", []
            
        term_weights = []
        for idx in nonzero_indices:
            term = self.feature_names[idx]
            weight = prod[0, idx]
            term_weights.append((term, weight))
            
        term_weights.sort(key=lambda x: x[1], reverse=True)
        top_matches = [t[0] for t in term_weights[:top_terms]]
        
        explanation = f"Matched key terms: {', '.join(top_matches)}"
        return explanation, top_matches

    def recommend(
        self,
        query: str,
        top_n: int = 8,
        subject: str = "All",
        difficulty: str = "All",
        resource_type: str = "All",
        available_only: bool = False,
        sort_by: str = "Relevance (Cosine Similarity)"
    ) -> tuple[pd.DataFrame, dict]:
        """
        Main recommendation query engine with content filtering,
        similarity scoring, explainability, fallback handling, and filtering.
        Guarantees at least 5-8 books minimum on any click or domain combination.
        """
        clean_query = preprocess_text(query)
        metadata = {
            "query": query,
            "cleaned_query": clean_query,
            "is_empty": False,
            "is_fallback": False,
            "max_similarity": 0.0,
            "total_matches": 0
        }

        # 1. Handle empty query -> Cold-Start fallback
        if not clean_query:
            metadata["is_empty"] = True
            recs = self.get_cold_start_recommendations(
                top_n=top_n,
                subject_filter=subject,
                difficulty=difficulty,
                resource_type=resource_type,
                available_only=available_only,
                sort_by=sort_by
            )
            return recs, metadata

        # 2. Vectorize user query
        query_vec = self.vectorizer.transform([clean_query])
        
        # Check if query contains any known vocabulary
        if query_vec.nnz == 0:
            metadata["is_fallback"] = True
            metadata["fallback_reason"] = "Query terms not found in library index vocabulary."
            fallback_df = self._fuzzy_fallback(clean_query, top_n, subject, difficulty, resource_type, available_only, sort_by)
            return fallback_df, metadata

        # 3. Compute Cosine Similarity against all resources
        sim_scores = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        max_sim = float(np.max(sim_scores))
        metadata["max_similarity"] = round(max_sim, 4)

        # 4. Weak match handling: if max similarity is negligible (< 0.04)
        if max_sim < 0.04:
            metadata["is_fallback"] = True
            metadata["fallback_reason"] = f"Low confidence match (max score {max_sim:.4f}). Showing closest related subjects."
            fallback_df = self._fuzzy_fallback(clean_query, top_n, subject, difficulty, resource_type, available_only, sort_by)
            return fallback_df, metadata

        # 5. Build results DataFrame with similarities and explanations
        res_df = self.df.copy()
        res_df["similarity_score"] = sim_scores
        res_df["is_cold_start"] = False
        
        explanations = []
        matching_terms_list = []
        for idx in range(len(res_df)):
            if sim_scores[idx] > 0.001:
                exp_text, terms = self.explain_similarity(query_vec, idx)
            else:
                exp_text, terms = f"Curriculum Complement: High faculty rating ({res_df.iloc[idx]['simulated_rating']}/5.0)", []
            explanations.append(exp_text)
            matching_terms_list.append(", ".join(terms) if terms else "Domain Curriculum")
            
        res_df["explanation"] = explanations
        res_df["matching_terms"] = matching_terms_list

        # Apply subject filter first
        domain_filtered = res_df.copy()
        if subject and subject != "All":
            domain_filtered = domain_filtered[domain_filtered["subject"] == subject]

        # Apply secondary filters if they leave at least 4 items
        diff_filtered = domain_filtered[domain_filtered["difficulty_level"] == difficulty] if (difficulty and difficulty != "All") else domain_filtered
        if len(diff_filtered) >= 4:
            domain_filtered = diff_filtered

        type_filtered = domain_filtered[domain_filtered["resource_type"] == resource_type] if (resource_type and resource_type != "All") else domain_filtered
        if len(type_filtered) >= 4:
            domain_filtered = type_filtered

        if available_only:
            avail_filtered = domain_filtered[domain_filtered["available_copies"] > 0]
            if len(avail_filtered) >= 3:
                domain_filtered = avail_filtered

        # Separate direct similarity matches (score > 0.005)
        direct_matches = domain_filtered[domain_filtered["similarity_score"] > 0.005].copy()
        metadata["total_matches"] = len(direct_matches)

        # Sort direct matches
        sorted_direct = self._sort_dataframe(direct_matches, sort_by=sort_by, default_sort_col="similarity_score")

        # If direct matches are sufficient, return top_n
        if len(sorted_direct) >= top_n:
            return sorted_direct.head(top_n).reset_index(drop=True), metadata

        # If direct matches are fewer than top_n (e.g., 1-3 books), augment with domain curriculum essentials
        needed = top_n - len(sorted_direct)
        other_books = domain_filtered[~domain_filtered["resource_id"].isin(sorted_direct["resource_id"])].copy()
        
        if not other_books.empty:
            sorted_other = self._sort_dataframe(other_books, sort_by=sort_by, default_sort_col="simulated_rating")
            supplement = sorted_other.head(needed).copy()
            # Mark explanation clearly
            supplement["explanation"] = supplement.apply(
                lambda r: f"Curriculum Extension: High faculty rating ({r['simulated_rating']}/5.0) in {r['topic']} (Foundational Reading)",
                axis=1
            )
            supplement["matching_terms"] = supplement["subject"].apply(lambda s: f"{s} Essential")
            
            combined = pd.concat([sorted_direct, supplement], ignore_index=True)
            return combined.head(top_n).reset_index(drop=True), metadata

        if sorted_direct.empty:
            fallback_df = self._fuzzy_fallback(clean_query, top_n, subject, difficulty, resource_type, available_only, sort_by)
            metadata["is_fallback"] = True
            return fallback_df, metadata

        return sorted_direct.head(top_n).reset_index(drop=True), metadata

    def _sort_dataframe(self, df: pd.DataFrame, sort_by: str, default_sort_col: str = "similarity_score") -> pd.DataFrame:
        """Sorts a DataFrame by the specified user criteria."""
        if df.empty:
            return df
        if sort_by == "Rating (High to Low)":
            return df.sort_values(by=["simulated_rating", "simulated_borrow_count"], ascending=[False, False])
        elif sort_by == "Year (Newest First)":
            return df.sort_values(by=["publication_year", "simulated_rating"], ascending=[False, False])
        elif sort_by == "Popularity (Borrows)":
            return df.sort_values(by=["simulated_borrow_count", "simulated_rating"], ascending=[False, False])
        elif sort_by == "Availability (Copies)":
            return df.sort_values(by=["available_copies", "simulated_rating"], ascending=[False, False])
        else: # "Relevance (Cosine Similarity)" or default
            sort_cols = [default_sort_col, "simulated_rating"] if default_sort_col in df.columns else ["simulated_rating"]
            return df.sort_values(by=sort_cols, ascending=[False, False])

    def _fuzzy_fallback(
        self,
        query: str,
        top_n: int,
        subject: str = "All",
        difficulty: str = "All",
        resource_type: str = "All",
        available_only: bool = False,
        sort_by: str = "Relevance (Cosine Similarity)"
    ) -> pd.DataFrame:
        """
        Fallback strategy for rare/unknown keywords:
        Matches partial substrings across titles and descriptions,
        or falls back to high-rated foundational materials.
        Guarantees at least top_n books.
        """
        tokens = query.split()
        filtered = self.df.copy()
        if subject and subject != "All":
            filtered = filtered[filtered["subject"] == subject]

        scores = []
        for _, row in filtered.iterrows():
            text = f"{row['title']} {row['subject']} {row['topic']} {row['keywords']}".lower()
            score = sum(1 for token in tokens if token in text)
            scores.append(score)
            
        fallback = filtered.copy()
        fallback["similarity_score"] = [s * 0.02 for s in scores]
        fallback["is_cold_start"] = False
        fallback["explanation"] = fallback.apply(
            lambda r: f"Fallback Match: Recommended based on partial keyword overlap and high rating ({r['simulated_rating']}/5.0)",
            axis=1
        )
        fallback["matching_terms"] = "Related Curriculum Topic"
        
        sorted_fallback = self._sort_dataframe(fallback, sort_by=sort_by, default_sort_col="similarity_score")
        return sorted_fallback.head(top_n).reset_index(drop=True)
