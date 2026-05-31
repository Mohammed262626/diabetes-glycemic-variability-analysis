# Programmatic Modeling of Glycemic Variability & Post-Prandial Shifts in Diabetic Patients

## 📌 Executive Summary
This project engineered an automated data ingestion and biostatistical pipeline to evaluate glycemic stability and daily metabolic trends across a cohort of 70 diabetic patients. By programmatically parsing 29,278 electronic health records, the analysis exposed severe late-afternoon coverage failures and quantified the exact impact of post-prandial metabolization using a paired-date framework.

### 🚀 Key Discoveries
* **The Pre-Dinner Peak:** Discovered that patient glucose levels peak drastically before dinner (Mean: 244.52 mg/dL), identifying a critical late-afternoon window where long-acting basal insulin efficacy degrades across the population.
* **The Paired Data Paradox:** Proved that while standard group-to-group comparisons show a minor -10.41 mg/dL breakfast shift, isolating date-matched records within individual patients reveals a highly significant true metabolic surge of +33.88 mg/dL ($p < 0.001$).
* **Data Integrity Deficits:** Flagged critical uncalibrated machine transmission errors (readings of 0.0 mg/dL overnight) that would otherwise corrupt baseline clinical predictive modeling.

---

## 🛠️ Tech Stack & Methodology
* **Data Pipeline:** Python (Pandas, NumPy, Glob) for automated Unix file extraction, data type standardization, and date-time index parsing.
* **Inferential Statistics:** SciPy (`scipy.stats`) for global variance analysis (One-Way ANOVA) and dependent sample modeling (Paired T-Test).
* **Post-Hoc Operations:** Statsmodels (`pairwise_tukeyhsd`) for family-wise error rate controlled pairwise comparisons.
* **Data Visualization:** Seaborn and Matplotlib for publication-ready categorical distribution modeling.

---

## 📊 Core Statistical Insights

### 1. Daily Glycemic Baselines
| Clinical Window | Sample ($N$) | Mean Glucose ($\text{mg/dL}$) | Std Dev ($\pm SD$) | Range ($\text{Min - Max}$) |
| :--- | :---: | :---: | :---: | :---: |
| **Pre-breakfast** | 989 | 160.29 | 98.90 | 19.0 - 501.0 |
| **Post-breakfast** | 3,518 | 170.70 | 77.74 | 23.0 - 461.0 |
| **Pre-dinner** | 66 | 244.52 | 104.36 | 25.0 - 476.0 |
| **Post-bedtime** | 904 | 148.77 | 86.73 | 0.0 - 461.0 |

### 2. Inferential Hypothesis Testing
* **Global Variance (One-Way ANOVA):** $F = 43.18$, $p = 6.97 \times 10^{-69}$ $\rightarrow$ **Highly Significant**. Confirms population-level glucose values differ systematically based on the clinical tracking window.
* **Individual Metabolic Shifts (Paired $t$-Test):** $t = -4.29$, $p = 2.39 \times 10^{-05}$ $\rightarrow$ **Highly Significant**. Confirms a predictable, quantifiable post-prandial glycemic surge ($+33.88\text{ mg/dL}$) within patients on matched dates.

*(Embed your generated Boxplot image here to visually showcase the distribution differences across the timeline)*

---

## 📂 How to Reproduce This Analysis
1. Clone this repository.
2. Ensure you have the dependencies installed: `pip install pandas scipy statsmodels seaborn`.
3. Place the raw `data-*` text files in the root directory.
4. Run `python analysis.py` to generate the automated text report and visualization figures.
