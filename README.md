# Trader Behavior Analysis Using Bitcoin Fear & Greed Index

This repository contains the data science internship project analyzing how market sentiment, as measured by the **Bitcoin Fear & Greed Index**, correlates with trader behavior and execution profitability on the **Hyperliquid** decentralized exchange.

The project is structured to evaluate trader psychology, capital commitment, and directional bias across different sentiment regimes, culminating in a predictive model for trade outcomes and actionable strategy recommendations.

---

## 📊 Project Deliverables

1. **Jupyter Notebook (`internship.ipynb`):** The complete end-to-end analytical workflow containing data cleaning, merging, feature engineering, exploratory data analysis, trader segmentation, and machine learning.
2. **Executive Report PDF (`Trader Behavior Analysis Using Bitcoin Fear & Greed Index.pdf`):** A publication-quality, 5-page PDF report designed with a professional corporate slate/teal aesthetic, featuring structured analysis tables and embedded high-resolution figures.
3. **Visualizations (`charts/`):** High-resolution analytical plots generated during EDA and modeling.
   - `sentiment_performance.png`: Duel-axis visualization mapping total PnL and trade win rates across sentiment categories.
   - `trader_behavior.png`: Chart mapping capital allocation (average position size) and directional bias (Long/Short order types).
   - `feature_importance.png`: Feature weight ranking from the Random Forest model.

---

## 🛠️ Methodology

### 1. Data Cleaning & Alignment
- **Fear & Greed Index Dataset:** 2,644 rows, 4 columns. Standardized date formatting.
- **Hyperliquid Trading Dataset:** 211,224 rows, 16 columns.
- **Merge Logic:** Transaction UNIX timestamps (milliseconds) were timezone-aligned and parsed into UTC dates. The datasets were merged on the daily date key, achieving an exceptional **99.997% match rate** across **480 active trading days**. No duplicate or missing values were found.

### 2. Exploratory Data Analysis
- Analyzed transaction distributions across five sentiment bands: *Extreme Fear*, *Fear*, *Neutral*, *Greed*, and *Extreme Greed*.
- Evaluated performance indicators (Total PnL, Win Rate, Average PnL) grouped by sentiment.

### 3. Behavioral & Segmentation Analysis
- **Capital Sizing:** Investigated position sizes relative to sentiment regimes.
- **Directional Bias:** Mapped order types (Open Long vs. Open Short) to sentiment zones to measure trend-following vs. contrarian behavior.
- **Trader Segmentation:** Classified traders into cohorts based on trade frequency (Frequent vs. Infrequent), consistency (Winners vs. Inconsistent), and trade volume (High vs. Low Size) to evaluate structural performance factors.

### 4. Predictive Modeling
- Built a **Random Forest Classifier** to predict trade profitability (Realized PnL > 0) using execution size (USD), transaction fees, and daily sentiment values.
- Analyzed feature importances to determine whether market sentiment holds independent predictive value.

---

## 📈 Key Insights

### 1. The Capital Sizing Paradox
Traders exhibit a distinct cognitive bias by committing their largest average position sizes during **Fear** ($7,816) and their smallest during **Extreme Greed** ($3,112). This is highly inefficient because performance metrics show that win rates and average profitability actually peak during Extreme Greed.

### 2. Sentiment vs. Performance
- **Extreme Greed** generated the highest win rate (**46.49%**) and average trade profitability (**$67.89 PnL**), indicating that momentum-following strategies in strong bullish regimes are highly successful.
- **Extreme Fear** showed the lowest win rate (**37.06%**) and average profitability (**$34.54**), reflecting the risk of catching falling knives.
- **Fear** generated the highest absolute profit pool (**$3.36M PnL**) due to high volume, despite a lower win rate (42.08%).

### 3. Trader Segments & Outcomes
- **Frequent vs. Infrequent:** Frequent traders generate **3.4x higher profits** ($496,528 vs. $147,032 avg PnL), reflecting execution efficiency and scale.
- **Win Rate vs. Absolute Profit:** Consistent winners (63.46% win rate) averaged $206,867 PnL, whereas inconsistent traders (37.91% win rate) achieved $333,668 PnL. This proves that asymmetric payoff distributions (large gains on outlier trades) outweigh simple win percentages.
- **High vs. Low Volume:** High-volume traders earned higher absolute profits ($416,806) despite lower win rates (36.17%) by leveraging larger execution sizing.

### 4. Predictive Model Results
- **Accuracy:** 73.62% | **Precision (Profitable):** 69.0% | **Recall:** 66.0% | **F1 Score:** 67.0%
- **Feature Importance:**
  - Transaction Fee: **43.0%**
  - Trade Size (USD): **42.0%**
  - Sentiment Value: **15.0%**
  - *Implication:* Sizing and execution costs are the main drivers of profitability, but daily sentiment remains a key independent predictive signal.

---

## 💡 Strategy Recommendations

1. **Reduce Position Sizes during Extreme Fear (20–30%):** Win rates contract significantly during market capitulations. Lowering sizing limits and tightening stops during Extreme Fear will preserve capital.
2. **Maintain Sizing & Increase Participation during Extreme Greed:** Momentum-driven markets yield the highest average profitability and win rates. Instead of scaling down, traders should maintain standard sizing and increase market participation to ride the trend.

---

## ⚙️ Environment Setup & Installation

### Prerequisites
- Python 3.8+
- Jupyter Notebook or JupyterLab

### Install Dependencies
To install the required Python packages, run:
```bash
pip install pandas numpy matplotlib seaborn scikit-learn
```

### How to Run
1. Clone this repository:
   ```bash
   git clone https://github.com/Gokulkannan22/primetrade_intern.git
   cd primetrade_intern
   ```
2. Run the Jupyter Notebook to re-execute the analysis:
   ```bash
   jupyter notebook internship.ipynb
   ```
