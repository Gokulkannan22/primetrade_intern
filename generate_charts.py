import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Create charts folder if it doesn't exist
os.makedirs('charts', exist_ok=True)

# Set style
sns.set_theme(style="whitegrid")
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 14,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.titlesize': 16
})

# Sentiment colors
sentiment_palette = {
    'Extreme Fear': '#c53030', # Deep Red
    'Fear': '#e53e3e',         # Red
    'Neutral': '#718096',      # Slate Gray
    'Greed': '#38a169',        # Green
    'Extreme Greed': '#22543d' # Deep Green
}
ordered_sentiment = ['Extreme Fear', 'Fear', 'Neutral', 'Greed', 'Extreme Greed']

# --- Chart 1: Performance by Sentiment ---
fig, ax1 = plt.subplots(figsize=(8, 4.5))

pnl_data = [0.74, 3.36, 1.29, 2.15, 2.72] # in Millions USD
win_rates = [37.06, 42.08, 39.70, 38.48, 46.49] # in %

# Bars for PnL
colors = [sentiment_palette[cat] for cat in ordered_sentiment]
bars = ax1.bar(ordered_sentiment, pnl_data, color=colors, alpha=0.85, width=0.5, edgecolor='black', linewidth=0.7)
ax1.set_ylabel('Total PnL ($ Millions)', color='#1a202c', fontweight='semibold')
ax1.set_xlabel('Market Sentiment Index Category', fontweight='semibold', labelpad=10)
ax1.tick_params(axis='y', labelcolor='#1a202c')
ax1.set_ylim(0, 4.0)

# Line for Win Rate
ax2 = ax1.twinx()
line = ax2.plot(ordered_sentiment, win_rates, color='#d69e2e', marker='o', linewidth=2.5, markersize=8, label='Win Rate (%)')
ax2.set_ylabel('Win Rate (%)', color='#d69e2e', fontweight='semibold')
ax2.tick_params(axis='y', labelcolor='#d69e2e')
ax2.set_ylim(30, 50)
ax2.grid(False)

# Add value labels
for bar in bars:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
             f"${height:.2f}M", ha='center', va='bottom', fontsize=9, fontweight='semibold')

for i, txt in enumerate(win_rates):
    ax2.annotate(f"{txt:.2f}%", (ordered_sentiment[i], win_rates[i]), 
                 textcoords="offset points", xytext=(0,10), ha='center', fontsize=9, 
                 fontweight='semibold', color='#b7791f')

plt.title('Trading Performance Metrics across Sentiment Profiles', pad=15, fontweight='bold', color='#2d3748')
plt.tight_layout()
plt.savefig(os.path.join('charts', 'sentiment_performance.png'), dpi=300)
plt.close()

# --- Chart 2: Trader Behavior (Position Size & Directional Bias) ---
fig, ax1 = plt.subplots(figsize=(8, 4.5))

pos_sizes = [5350, 7816, 4783, 5737, 3112] # in USD
long_bias = [32.73, 28.82, 27.12, 16.99, 15.75]
short_bias = [14.83, 17.61, 16.86, 23.19, 19.16]

# Bars for position size
bars = ax1.bar(ordered_sentiment, pos_sizes, color='#2b6cb0', alpha=0.8, width=0.4, label='Avg Position Size ($)', edgecolor='black', linewidth=0.7)
ax1.set_ylabel('Average Position Size ($ USD)', color='#2b6cb0', fontweight='semibold')
ax1.set_xlabel('Market Sentiment Index Category', fontweight='semibold', labelpad=10)
ax1.tick_params(axis='y', labelcolor='#2b6cb0')
ax1.set_ylim(0, 9000)

# Line for bias
ax2 = ax1.twinx()
line1 = ax2.plot(ordered_sentiment, long_bias, color='#e53e3e', marker='^', linestyle='--', linewidth=2, markersize=7, label='Long Bias (%)')
line2 = ax2.plot(ordered_sentiment, short_bias, color='#2f855a', marker='v', linestyle='-.', linewidth=2, markersize=7, label='Short Bias (%)')
ax2.set_ylabel('Order Type Proportion (%)', color='#2d3748', fontweight='semibold')
ax2.tick_params(axis='y', labelcolor='#2d3748')
ax2.set_ylim(10, 40)
ax2.grid(False)

# Labels for bars
for bar in bars:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height + 150,
             f"${height:,}", ha='center', va='bottom', fontsize=9, color='#1a365d', fontweight='semibold')

# Combined legend for lines
lines = line1 + line2
labels = [l.get_label() for l in lines]
ax2.legend(lines, labels, loc='upper right', frameon=True, facecolor='white', framealpha=0.9)

plt.title('Trader Capital Commitment & Directional Bias vs. Market Sentiment', pad=15, fontweight='bold', color='#2d3748')
plt.tight_layout()
plt.savefig(os.path.join('charts', 'trader_behavior.png'), dpi=300)
plt.close()

# --- Chart 3: Feature Importance ---
fig, ax = plt.subplots(figsize=(6, 3))

features = ['Fee', 'Size USD', 'Sentiment Value']
importance = [43.0, 42.0, 15.0]

bars = ax.barh(features, importance, color=['#2b6cb0', '#319795', '#d69e2e'], alpha=0.85, height=0.5, edgecolor='black', linewidth=0.7)
ax.set_xlabel('Relative Importance (%)', fontweight='semibold')
ax.set_title('Random Forest Feature Importance Profile', fontweight='bold', pad=12, color='#2d3748')
ax.set_xlim(0, 50)

# Add value labels
for bar in bars:
    width = bar.get_width()
    ax.text(width + 1.0, bar.get_y() + bar.get_height()/2.,
            f"{width:.1f}%", ha='left', va='center', fontsize=10, fontweight='semibold')

# Invert y-axis to have Fee at the top
ax.invert_yaxis()
plt.tight_layout()
plt.savefig(os.path.join('charts', 'feature_importance.png'), dpi=300)
plt.close()

print("Charts successfully generated inside charts/ directory.")
