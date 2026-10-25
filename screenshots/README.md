# SmartLib AI - Screenshots & Visual Assets

This directory contains visual captures of the SmartLib AI academic dashboard.

## Included High-Resolution Figures

1. **`01_recommender_search_view.png`**
   - **View:** Resource Recommendation Search Hub
   - **Query Tested:** `"dynamic programming graph algorithms cormen"`
   - **Highlights:** Top hit *Introduction to Algorithms (CLRS)* with Cosine Similarity `0.3217`, explainability callout highlighting matched n-grams (`algorithms`, `dynamic programming`, `graph theory`), live latency meter (`48 ms`), physical shelf locator (`CS-Floor-2-A1`), and interactive `Relevant (👍)` feedback button.

2. **`02_cold_start_view.png`**
   - **View:** Cold-Start Initial State
   - **Condition:** No query entered / fresh unauthenticated student session.
   - **Highlights:** Zero-login cold-start notification banner, ranking of faculty-endorsed curriculum baselines (*Clean Code*, *AI: A Modern Approach*) weighted by academic rating and campus checkout frequency.

3. **`03_catalog_analytics_view.png`**
   - **View:** Library Catalog Analytics Dashboard
   - **Highlights:** High-level KPIs (125 Total Titles, 8 Academic Domains, 48.2% Availability Ratio, 4.74 ⭐ Average Rating), horizontal bar charts detailing domain distribution across STEM faculties.

4. **`04_ir_evaluation_metrics_view.png`**
   - **View:** Information Retrieval (IR) Evaluation Benchmark
   - **Highlights:** Genuine, measured metrics: **Mean Precision@5: 66.7%**, **Mean Recall@5: 77.2%**, **Mean Reciprocal Rank (MRR): 1.00**, complete test suite table, and honest failure case analysis (Q6 out-of-domain quantum query).

---

## How to Capture Live Browser Screenshots on macOS

If you run the Streamlit application in a local browser session, you can capture full-resolution native browser screenshots with these steps:

1. **Start the Streamlit Server:**
   ```bash
   ./venv/bin/streamlit run app.py
   ```
2. **Open the Web Browser:**
   Navigate to `http://localhost:8501`.
3. **Capture Focused Screenshots on macOS:**
   - Press `Command (⌘) + Shift + 4`, then tap the `Spacebar`.
   - Hover your mouse over the Google Chrome / Safari window and click once.
   - The screenshot will be saved to your Desktop as a crisp PNG.
   - Rename and move it to this `screenshots/` directory:
     ```bash
     mv ~/Desktop/Screenshot*.png screenshots/01_recommender_search_view.png
     ```
