"""
Generates a publication-quality architecture diagram PNG for SmartLib AI
using matplotlib.
"""

import os
os.environ["MPLCONFIGDIR"] = "/tmp"
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_diagram():
    os.makedirs("docs", exist_ok=True)
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis("off")

    # Title & Subtitle
    ax.text(7, 7.6, "SmartLib AI System Architecture", ha="center", va="center", fontsize=18, fontweight="bold", color="#0f172a")
    ax.text(7, 7.25, "Explainable, Resource-Efficient Academic Library Recommendation System", ha="center", va="center", fontsize=10, color="#475569")

    # Layers / Boxes definition (x, y, w, h, title, text, bg, border)
    boxes = [
        (0.6, 5.0, 3.2, 1.6, "1. Student Query Interface", "• Learning Goal / Topic\n• Syllabus Unit / Keywords\n• Real-time text input", "#e0f2fe", "#0284c7"),
        (4.4, 5.0, 3.2, 1.6, "2. Text Preprocessing", "• Lowercasing & Punctuation Strip\n• Stopwords Filtering\n• Unigram & Bigram Extraction", "#fef3c7", "#d97706"),
        (8.2, 5.0, 3.2, 1.6, "3. Vectorization Engine", "• Sublinear TF Scaling\n• Inverse Document Freq (IDF)\n• Sparse Query Vector q", "#dcfce7", "#16a34a"),
        (11.8, 2.0, 1.8, 4.6, "Library Catalog", "• 337 STEM Resources\n• 8 Academic Domains\n• Keywords & Abstracts\n• Simulated Availability\n• Shelf Location Index\n• Faculty Ratings", "#f1f5f9", "#64748b"),
        
        (0.6, 1.8, 3.2, 1.8, "6. User Feedback Loop", "• Explicit Thumbs Up / Down\n• Live Empirical Precision\n• Session State & CSV Log\n• Cold-Start Re-weighting", "#fce7f3", "#db2777"),
        (4.4, 1.8, 3.2, 1.8, "5. Ranking & Filters", "• Cosine Similarity Scoring\n• Multi-Domain Filter\n• Difficulty & Type Filters\n• Shelf Availability Check", "#ede9fe", "#7c3aed"),
        (8.2, 1.8, 3.2, 1.8, "4. Explainability & Fallback", "• Top Overlapping N-Grams\n• TF-IDF Contribution Score\n• Out-of-Domain Guardrail\n• Curriculum Baseline Fallback", "#ffedd5", "#ea580c")
    ]

    for (x, y, w, h, title, text, bg, border) in boxes:
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15", facecolor=bg, edgecolor=border, linewidth=2)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h - 0.35, title, ha="center", va="center", fontsize=10.5, fontweight="bold", color="#0f172a")
        ax.text(x + 0.15, y + 0.2, text, ha="left", va="bottom", fontsize=8.2, color="#334155", linespacing=1.35)

    # Connecting Arrows
    arrows = [
        # Forward flow: 1 -> 2 -> 3
        ((3.8, 5.8), (4.4, 5.8), "Raw Text"),
        ((7.6, 5.8), (8.2, 5.8), "Clean Tokens"),
        # Catalog into Vectorization
        ((11.8, 5.8), (11.4, 5.8), "Catalog Corpus"),
        # Vectorization down into Explainability & Ranking
        ((9.8, 5.0), (9.8, 3.6), "Vector q vs Matrix D"),
        # Explainability to Ranking
        ((8.2, 2.7), (7.6, 2.7), "Ranked Scores + Explanations"),
        # Ranking to Feedback
        ((4.4, 2.7), (3.8, 2.7), "Personalized Recs"),
        # Feedback up to Query Interface
        ((2.2, 3.6), (2.2, 5.0), "User Relevance Signals")
    ]

    for (start, end, label) in arrows:
        ax.annotate(
            "", xy=end, xytext=start,
            arrowprops=dict(facecolor="#475569", edgecolor="#475569", width=1.5, headwidth=7, shrink=0.08)
        )
        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2 + 0.18
        ax.text(mid_x, mid_y, label, ha="center", va="center", fontsize=7.5, fontweight="semibold", color="#1e293b",
                bbox=dict(boxstyle="round,pad=0.15", facecolor="#ffffff", edgecolor="#cbd5e1", alpha=0.9))

    # Footer Caption
    ax.text(7, 0.5, "Workflow: Student Query ➔ Preprocessing ➔ TF-IDF Vectorization ➔ Cosine Similarity ➔ Ranking/Filtering ➔ Explainability ➔ Feedback",
            ha="center", va="center", fontsize=8.5, fontstyle="italic", color="#64748b")

    plt.tight_layout()
    output_path = "docs/architecture_diagram.png"
    plt.savefig(output_path, bbox_inches="tight", dpi=300)
    plt.close()
    print(f"Architecture diagram generated successfully at: {output_path}")

if __name__ == "__main__":
    generate_diagram()
