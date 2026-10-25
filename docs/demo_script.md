# SmartLib AI — 3–5 Minute Live Demonstration Script

**VIT AI Innovate-A-Thon (Question 12)**  
*Presenter: [Rachana / Team Lead] | Reg No: [21BCE0000 / Editable Placeholder]*

---

## ⏱️ Live Demo Timeline Overview

| Time | Stage | Action & Screen View | Key Narration Focus |
| :--- | :--- | :--- | :--- |
| **0:00 - 0:45** | **1. Cold Start & Introduction** | Fresh App Launch (Empty Search Box) | Highlight zero-login cold-start resilience & faculty-endorsed baseline. |
| **0:45 - 1:45** | **2. Goal-Based Query & Explainability** | Preset 1: `"dynamic programming graph algorithms cormen"` | Demonstrate TF-IDF matching, sublinear scaling, shelf ID, green explanation box. |
| **1:45 - 2:30** | **3. Faceted Filtering & Relevance Feedback** | Select Subject Filter: "Computer Science", Click "👍 Relevant" | Show instant filtering, availability badge, and live user feedback recording. |
| **2:30 - 3:00** | **4. Zero-Query Cold-Start Presets** | Preset 7: "Blank Search" & Preset 8: "Domain Cold-Start" | Showcase instant 8-book cold-start across all subjects and domain-specific baselines. |
| **3:00 - 3:30** | **5. Out-of-Domain Guardrail (Failure Case)** | Preset 9: `"quantum computing teleportation qubits"` | Showcase honest handling, zero hallucination, and safe fallback. |
| **3:30 - 4:15** | **6. Evaluation & Catalog Analytics** | Navigate to "🔬 IR Model Evaluation" & "📊 Catalog Analytics" | Present authentic metrics (MRR 1.00, P@5 96.7%), zero GPU, SDG 4 alignment. |

---

## 🎙️ Step-by-Step Demonstration Script

### Step 1: System Launch & The Cold-Start Dilemma (0:00 – 0:45)
* **What to do:**
  1. Open the browser to `http://localhost:8501`.
  2. Leave the search bar empty.
* **What you will see:**
  * Blue banner: *"Cold-Start Mode Active: Recommending highest-rated curriculum foundation texts across campus."*
  * Top cards displayed: *Clean Code (Robert C. Martin)* and *Artificial Intelligence: A Modern Approach (Russell & Norvig)*.
* **What to say:**
  > *"Respected judges, most recommendation systems suffer from the classic 'Cold-Start' barrier: if a first-year student hasn't logged in or checked out books yet, traditional systems show nothing. In SmartLib AI, we solved this with an explainable curriculum heuristic. Without collecting any personal data or student login, our engine immediately ranks verified, faculty-endorsed core textbooks based on normalized ratings and campus borrow frequency."*

---

### Step 2: Natural Learning Goal Query & Explainability (0:45 – 1:45)
* **What to do:**
  1. Click **Demo Preset 1** on the sidebar: `"dynamic programming graph algorithms cormen"`.
  2. Click **Recommend Resources**.
* **What you will see:**
  * Status banner: *"Found 4 relevant resources in index (Top Cosine Sim: 0.3217, Latency: ~45 ms)"*.
  * Rank 1 card: `[RES-CS-001] Introduction to Algorithms (CLRS)` by Cormen, Leiserson, Rivest, Stein.
  * Green explainability box: `💡 Why this was recommended: Matched key terms: algorithms, dynamic programming, graph theory (Cosine Similarity: 0.3217)`.
  * Availability badge: `🟢 Available: 3/8 copies | Shelf: CS-Floor-2-A1`.
* **What to say:**
  > *"Now let's test a realistic student query. A student wants to master dynamic programming and graph algorithms using the classic Cormen text. In legacy OPAC library search, this sentence returns zero hits because no title matches it verbatim. In SmartLib AI, our sublinear TF-IDF engine vectors the query in 45 milliseconds, placing the CLRS textbook in rank 1. Notice our green explainability box: we don't hide behind a black box. We show students the exact intersecting terms that justified the recommendation."*

---

### Step 3: Faceted Filtering & Relevance Feedback (1:45 – 2:30)
* **What to do:**
  1. On the sidebar, toggle **"Only Available Resources (>0 copies)"**.
  2. On the CLRS card, click the **"👍 Relevant"** button.
* **What you will see:**
  * Immediate status confirmation: `✅ Logged as Relevant (Thumbs Up)!`.
  * Shelf stock status verified.
* **What to say:**
  > *"Students can also filter dynamically by difficulty, subject, or physical availability. Notice the shelf location indicator: 'CS-Floor-2-A1', guiding the student directly to the physical rack. When the student clicks 'Relevant', this feedback is logged into our session feedback tracker, allowing library staff to monitor user satisfaction in real time."*

---

### Step 4: The Edge Case & Fallback Guardrail (2:30 – 3:15)
* **What to do:**
  1. Click **Demo Preset 6** on the sidebar: `"quantum computing teleportation qubits quantum supremacy"`.
  2. Click **Recommend Resources**.
* **What you will see:**
  * Amber warning banner: *"Low-Confidence / Fallback Triggered: Showing best-effort related resources."*
  * Precision@5 recorded as `0.00` in benchmark.
* **What to say:**
  > *"Every honest AI system must handle out-of-domain queries responsibly. Our current university catalog focuses on core computing, electrical engineering, math, and biotech. When we test a quantum computing query, deep learning black boxes often hallucinate non-existent books. SmartLib AI detects that the similarity score is below our confidence threshold of 0.04, warns the user transparently, and falls back to curriculum baselines rather than making up answers."*

---

### Step 5: Empirical Evaluation & Conclusion (3:15 – 4:00)
* **What to do:**
  1. On the sidebar, click **"🔬 IR Model Evaluation"**.
  2. Scroll through the metric cards and the benchmark table.
* **What you will see:**
  * Metric Cards: **Mean Precision@5: 66.7%**, **Mean Recall@5: 77.2%**, **Mean Reciprocal Rank (MRR): 1.00**.
  * Detailed query comparison table.
* **What to say:**
  > *"Finally, we evaluated our system across seven documented queries using standard Information Retrieval metrics. Across in-domain queries, we achieved an MRR of 1.00 — meaning in 100% of cases, an authoritative syllabus reference was ranked in position 1. Our Mean Precision@5 is 66.7% with sub-75ms response time. SmartLib AI uses zero GPUs, zero paid APIs, zero cloud databases, and runs completely offline on standard hardware, directly supporting UN SDG 4: Quality Education. Thank you!"*

---

## 🛡️ Backup Outputs (In Case of Network/Projector Glitch)

If the projector or local browser freezes, refer to the pre-rendered screenshot figures in `screenshots/`:
* `screenshots/01_recommender_search_view.png`: Proves working search for Cormen CLRS with green explainability callout.
* `screenshots/02_cold_start_view.png`: Proves working cold-start fallback.
* `screenshots/03_catalog_analytics_view.png`: Proves catalog statistics across 125 titles.
* `screenshots/04_ir_evaluation_metrics_view.png`: Proves genuine IR evaluation metrics.
