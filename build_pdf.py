import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to draw custom headers, footers, and page numbers dynamically.
    Excludes the cover page (Page 1) from receiving headers/footers.
    """
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_elements(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_elements(self, page_count):
        self.saveState()
        
        # --- Page 1: Cover Page Decoration ---
        if self._pageNumber == 1:
            # Draw decorative side bars on the cover page
            self.setFillColor(HexColor("#1a365d")) # Dark Navy
            self.rect(0, 0, 24, 792, fill=True, stroke=False)
            self.setFillColor(HexColor("#2c7a7b")) # Teal
            self.rect(24, 0, 6, 792, fill=True, stroke=False)
            self.restoreState()
            return
        
        # --- Pages 2+: Content Page Headers & Footers ---
        # Header text
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(HexColor("#1a365d"))
        self.drawString(54, 750, "INTERNSHIP EVALUATION REPORT")
        self.setFont("Helvetica", 8)
        self.setFillColor(HexColor("#718096"))
        self.drawRightString(558, 750, "Trader Behavior Analysis Using Bitcoin Fear & Greed Index")
        
        # Header line
        self.setStrokeColor(HexColor("#cbd5e0"))
        self.setLineWidth(0.5)
        self.line(54, 742, 558, 742)
        
        # Footer line
        self.line(54, 52, 558, 52)
        
        # Footer text
        self.drawString(54, 40, "Author: Gokul | Data Science & Analytics")
        self.drawRightString(558, 40, f"Page {self._pageNumber} of {page_count}")
        
        self.restoreState()


def make_heading(text, style):
    """
    Creates a section heading with a vertical teal bar on the left.
    """
    t = Table([['', Paragraph(text, style)]], colWidths=[4, 500])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), HexColor('#2c7a7b')), # Teal bar
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('LEFTPADDING', (1,0), (1,0), 6),
        ('LEFTPADDING', (0,0), (0,0), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    return t


def build_pdf():
    pdf_filename = "Trader Behavior Analysis Using Bitcoin Fear & Greed Index.pdf"
    
    # Page setup - 0.75 margin is 54pt. Printable width is 612 - 108 = 504.
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=72,
        bottomMargin=72
    )
    
    # Styles setup
    styles = getSampleStyleSheet()
    
    # Modify default body
    styles['Normal'].textColor = HexColor('#2d3748')
    styles['Normal'].fontSize = 9.5
    styles['Normal'].leading = 14
    
    # Custom styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=26,
        leading=32,
        textColor=HexColor('#1a365d'),
        spaceAfter=15
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=13,
        leading=17,
        textColor=HexColor('#4a5568'),
        spaceAfter=30
    )
    
    metadata_style = ParagraphStyle(
        'CoverMetadata',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=HexColor('#4a5568')
    )
    
    heading1_style = ParagraphStyle(
        'ReportHeading1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=HexColor('#1a365d'),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )
    
    heading2_style = ParagraphStyle(
        'ReportHeading2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=HexColor('#2c7a7b'),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'ReportBody',
        parent=styles['Normal'],
        spaceAfter=6
    )
    
    bullet_style = ParagraphStyle(
        'ReportBullet',
        parent=styles['Normal'],
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )
    
    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
        alignment=1 # Centered
    )
    
    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontSize=8,
        leading=10,
        textColor=HexColor('#2d3748'),
        alignment=1 # Centered
    )
    
    table_cell_left_style = ParagraphStyle(
        'TableCellLeft',
        parent=styles['Normal'],
        fontSize=8,
        leading=10.5,
        textColor=HexColor('#2d3748'),
        alignment=0 # Left
    )

    story = []

    # =========================================================================
    # PAGE 1: COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 100))
    story.append(Paragraph("Trader Behavior Analysis Using Bitcoin Fear & Greed Index", title_style))
    
    # Colored horizontal rule
    rule = Table([['']], colWidths=[450], rowHeights=[3])
    rule.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor('#2c7a7b')),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(rule)
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("A Data-Driven Study on Sentimental Trading Patterns on Hyperliquid", subtitle_style))
    story.append(Spacer(1, 260))
    
    # Metadata Block
    story.append(Paragraph("<b>Author:</b> Gokul", metadata_style))
    story.append(Paragraph("<b>Role:</b> Data Science & Analytics Intern", metadata_style))
    story.append(Paragraph("<b>Subject:</b> Internship Evaluation Submission", metadata_style))
    story.append(Paragraph("<b>Date:</b> June 2026", metadata_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: EXEC SUMMARY, PROBLEM STATEMENT, DATASET, DATA PREPARATION
    # =========================================================================
    story.append(make_heading("1. Executive Summary", heading1_style))
    summary_text = (
        "This report presents an empirical analysis of trader behavior on the Hyperliquid decentralized exchange, "
        "investigating the relationship between Bitcoin market sentiment—quantified via the Fear & Greed Index—and "
        "retail transactional patterns. Over a 480-day trading period spanning 211,224 executions, we identify "
        "significant cognitive and capital bias. Traders allocate their largest average position sizes ($7,816) during "
        "market-wide Fear, yet achieve their highest win rates (46.49%) and average trade profitability ($67.89) during "
        "Extreme Greed. Furthermore, advanced trader segmentation reveals that frequent traders outperform infrequent "
        "traders by 3.4x in absolute returns. A predictive Random Forest model establishes trade size and transactional "
        "fees as primary predictors of trade success, with sentiment serving as a crucial secondary variable. These "
        "findings culminate in actionable recommendations to reduce capital exposure during market fear and expand momentum "
        "strategies during extreme greed."
    )
    story.append(Paragraph(summary_text, body_style))
    story.append(Spacer(1, 10))

    story.append(make_heading("2. Problem Statement", heading1_style))
    problem_text = (
        "Cryptocurrency markets, particularly Bitcoin, are characterized by high volatility driven largely by retail "
        "sentiment. Behavioral finance dictates that emotional states—ranging from fear of loss to fear of missing out "
        "(FOMO)—frequently override rational, systematic trading models. In decentralized finance (DeFi) platforms "
        "such as Hyperliquid, these sentiment shifts translate into rapid changes in positioning. This study seeks "
        "to solve the analytical challenge of mapping daily sentiment indices to trade-level transaction data. By doing "
        "so, we identify how market-wide psychology alters risk thresholds, directional bias, and ultimate financial "
        "performance, providing data-backed guardrails to help traders avoid emotional traps."
    )
    story.append(Paragraph(problem_text, body_style))
    story.append(Spacer(1, 10))

    story.append(make_heading("3. Dataset Overview", heading1_style))
    dataset_text = (
        "The empirical analysis was conducted using two independent datasets covering a total of 480 distinct trading days:<br/>"
        "&bull; <b>Fear & Greed Index Dataset:</b> 2,644 rows and 4 columns, containing daily historic sentiment records including "
        "index values (0 to 100) and classifications ('Extreme Fear', 'Fear', 'Neutral', 'Greed', 'Extreme Greed').<br/>"
        "&bull; <b>Trading Dataset:</b> 211,224 rows and 16 columns of granular transaction logs, detailing execution prices, "
        "positions, order directions, fees, and realized PnL on Hyperliquid."
    )
    story.append(Paragraph(dataset_text, body_style))
    story.append(Spacer(1, 10))

    story.append(make_heading("4. Data Preparation & Cleaning", heading1_style))
    prep_text = (
        "To guarantee analytical integrity, a rigorous data cleaning pipeline was constructed. Initial checks "
        "indicated zero missing values and zero duplicate records across both datasets. Timestamps in the trading log "
        "(originally in millisecond UNIX) were parsed, adjusted for time-zone alignment, and converted to daily date formats. "
        "The datasets were subsequently merged on the standardized date key. The merge operation achieved an exceptional "
        "<b>99.997% match rate</b>, assuring that the joint data model represents an exhaustive and accurate ledger "
        "of trading activity relative to prevailing market sentiment."
    )
    story.append(Paragraph(prep_text, body_style))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: EDA & SENTIMENT-BASED PERFORMANCE ANALYSIS
    # =========================================================================
    story.append(make_heading("5. Exploratory Data Analysis", heading1_style))
    eda_text = (
        "Exploratory analysis showed a healthy distribution of trading activity across all sentiment regimes, "
        "reflecting diverse market conditions. Volume was highly concentrated in standard Fear (61,837 trades) "
        "and Greed (50,303 trades) regimes. This distribution shows that the market spends the majority of its time in "
        "moderate transition states, while periods of Extreme Fear (21,400 trades) are relatively rare, forming highly volatile "
        "market capitulation points."
    )
    story.append(Paragraph(eda_text, body_style))
    story.append(Spacer(1, 10))

    story.append(make_heading("6. Sentiment-Based Performance Analysis", heading1_style))
    performance_intro = (
        "Aggregating key performance indicators (KPIs) by market sentiment reveals a distinct divergence in trader "
        "profitability. The following dataset details performance metrics across the sentiment spectrum:"
    )
    story.append(Paragraph(performance_intro, body_style))
    story.append(Spacer(1, 6))

    # Performance Table
    # Widths: 120 + 94 + 100 + 100 + 90 = 504
    perf_data = [
        [
            Paragraph("<b>Sentiment</b>", table_header_style),
            Paragraph("<b>Trades</b>", table_header_style),
            Paragraph("<b>Total PnL</b>", table_header_style),
            Paragraph("<b>Avg PnL</b>", table_header_style),
            Paragraph("<b>Win Rate</b>", table_header_style)
        ],
        [Paragraph("Extreme Fear", table_cell_left_style), Paragraph("21,400", table_cell_style), Paragraph("$0.74M", table_cell_style), Paragraph("$34.54", table_cell_style), Paragraph("37.06%", table_cell_style)],
        [Paragraph("Fear", table_cell_left_style), Paragraph("61,837", table_cell_style), Paragraph("$3.36M", table_cell_style), Paragraph("$54.29", table_cell_style), Paragraph("42.08%", table_cell_style)],
        [Paragraph("Neutral", table_cell_left_style), Paragraph("37,686", table_cell_style), Paragraph("$1.29M", table_cell_style), Paragraph("$34.31", table_cell_style), Paragraph("39.70%", table_cell_style)],
        [Paragraph("Greed", table_cell_left_style), Paragraph("50,303", table_cell_style), Paragraph("$2.15M", table_cell_style), Paragraph("$42.74", table_cell_style), Paragraph("38.48%", table_cell_style)],
        [Paragraph("Extreme Greed", table_cell_left_style), Paragraph("39,992", table_cell_style), Paragraph("$2.72M", table_cell_style), Paragraph("$67.89", table_cell_style), Paragraph("46.49%", table_cell_style)]
    ]
    
    perf_table = Table(perf_data, colWidths=[120, 94, 100, 100, 90])
    perf_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HexColor('#1a365d')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,0), 5),
        ('TOPPADDING', (0,0), (-1,0), 5),
        ('BOTTOMPADDING', (0,1), (-1,-1), 4),
        ('TOPPADDING', (0,1), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, HexColor('#f7fafc')]),
        ('LINEBELOW', (0,0), (-1,0), 1.5, HexColor('#2c7a7b')), # Teal accent line
        ('LINEBELOW', (0,-1), (-1,-1), 1, HexColor('#cbd5e0')),
        ('LINEBELOW', (0,1), (-1,-2), 0.5, HexColor('#e2e8f0')),
        ('BOX', (0,0), (-1,-1), 0.5, HexColor('#e2e8f0')),
    ]))
    story.append(perf_table)
    story.append(Spacer(1, 12))

    perf_discussion = (
        "<b>Key Analysis:</b> The empirical results demonstrate that <b>Extreme Greed</b> periods generate the highest "
        "average trade profitability ($67.89) and the highest win rate (46.49%). This indicates that momentum-driven "
        "strategies excel in strongly rising markets. Conversely, standard <b>Fear</b> periods generated the largest "
        "absolute pool of gains ($3.36M PnL) due to high transaction volume, despite a moderate win rate (42.08%). "
        "Extreme Fear periods show a distinct deterioration in win rates to 37.06% with an average PnL of only $34.54, "
        "indicating severe risk and execution friction as traders attempt to catch falling knives."
    )
    story.append(Paragraph(perf_discussion, body_style))
    story.append(Spacer(1, 10))

    # Add Chart 1: Performance by Sentiment (loaded from charts/ subfolder)
    chart1_path = os.path.join('charts', 'sentiment_performance.png')
    if os.path.exists(chart1_path):
        img1 = Image(chart1_path, width=380, height=213.75)
        img1.hAlign = 'CENTER'
        story.append(img1)
    
    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: TRADER BEHAVIOR ANALYSIS & SEGMENTATION
    # =========================================================================
    story.append(make_heading("7. Trader Behavior Analysis", heading1_style))
    behavior_text = (
        "An examination of capital sizing and directional bias reveals a paradox in trader psychology:<br/>"
        "&bull; <b>Capital Commitment:</b> Traders commit the largest average position sizes during <b>Fear</b> ($7,816) "
        "and the smallest during <b>Extreme Greed</b> ($3,112). This represents a counter-intuitive behavior: committing "
        "the most capital in periods of low win rates (42.08%) and scaling down significantly when performance "
        "peaks (46.49% win rate).<br/>"
        "&bull; <b>Directional Bias:</b> Traders display a strong long-bias during periods of market distress, opening "
        "32.73% long positions during Extreme Fear. During Greed and Extreme Greed, long bias collapses to 16.99% and 15.75%, "
        "while short positions rise to 23.19% and 19.16%, demonstrating counter-trend fade attempts."
    )
    story.append(Paragraph(behavior_text, body_style))
    story.append(Spacer(1, 8))

    # Add Chart 2: Trader Behavior (loaded from charts/ subfolder)
    chart2_path = os.path.join('charts', 'trader_behavior.png')
    if os.path.exists(chart2_path):
        img2 = Image(chart2_path, width=360, height=202.5)
        img2.hAlign = 'CENTER'
        story.append(img2)
    story.append(Spacer(1, 10))

    story.append(make_heading("8. Trader Segmentation", heading1_style))
    segment_intro = (
        "Traders were segmented along key behavioral axes. The table below summaries execution metrics across profiles:"
    )
    story.append(Paragraph(segment_intro, body_style))
    story.append(Spacer(1, 6))

    # Segmentation Table
    # Widths: 80 + 75 + 70 + 75 + 64 + 140 = 504
    seg_data = [
        [
            Paragraph("<b>Segment Profile</b>", table_header_style),
            Paragraph("<b>Group</b>", table_header_style),
            Paragraph("<b>Avg Size/Trades</b>", table_header_style),
            Paragraph("<b>Avg PnL</b>", table_header_style),
            Paragraph("<b>Win Rate</b>", table_header_style),
            Paragraph("<b>Key Finding</b>", table_header_style)
        ],
        [
            Paragraph("Frequent vs. Infrequent", table_cell_left_style),
            Paragraph("Frequent", table_cell_style),
            Paragraph("11,685 trades", table_cell_style),
            Paragraph("$496,528", table_cell_style),
            Paragraph("41.36%", table_cell_style),
            Paragraph("Frequent traders generate ~3.4x higher profits than infrequent traders, reflecting economies of scale.", table_cell_left_style)
        ],
        [
            Paragraph("", table_cell_left_style),
            Paragraph("Infrequent", table_cell_style),
            Paragraph("1,517 trades", table_cell_style),
            Paragraph("$147,032", table_cell_style),
            Paragraph("39.26%", table_cell_style),
            Paragraph("", table_cell_left_style)
        ],
        [
            Paragraph("Winners vs. Inconsistent", table_cell_left_style),
            Paragraph("Consistent", table_cell_style),
            Paragraph("N/A", table_cell_style),
            Paragraph("$206,867", table_cell_style),
            Paragraph("63.46%", table_cell_style),
            Paragraph("High win rates do not directly map to highest profits; inconsistent traders earn more on outsized wins.", table_cell_left_style)
        ],
        [
            Paragraph("", table_cell_left_style),
            Paragraph("Inconsistent", table_cell_style),
            Paragraph("N/A", table_cell_style),
            Paragraph("$333,668", table_cell_style),
            Paragraph("37.91%", table_cell_style),
            Paragraph("", table_cell_left_style)
        ],
        [
            Paragraph("High vs. Low Volume", table_cell_left_style),
            Paragraph("High Vol", table_cell_style),
            Paragraph("Size: $10,152", table_cell_style),
            Paragraph("$416,806", table_cell_style),
            Paragraph("36.17%", table_cell_style),
            Paragraph("High-volume traders achieve greater profits despite lower win rates, driven by larger size profiles.", table_cell_left_style)
        ],
        [
            Paragraph("", table_cell_left_style),
            Paragraph("Low Vol", table_cell_style),
            Paragraph("Size: $1,864", table_cell_style),
            Paragraph("$226,754", table_cell_style),
            Paragraph("44.44%", table_cell_style),
            Paragraph("", table_cell_left_style)
        ],
    ]

    seg_table = Table(seg_data, colWidths=[80, 75, 70, 75, 64, 140])
    seg_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HexColor('#1a365d')),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,0), 5),
        ('TOPPADDING', (0,0), (-1,0), 5),
        ('BOTTOMPADDING', (0,1), (-1,-1), 3),
        ('TOPPADDING', (0,1), (-1,-1), 3),
        
        # Spanning Segment Profile
        ('SPAN', (0,1), (0,2)),
        ('SPAN', (0,3), (0,4)),
        ('SPAN', (0,5), (0,6)),
        
        # Spanning Key Findings
        ('SPAN', (5,1), (5,2)),
        ('SPAN', (5,3), (5,4)),
        ('SPAN', (5,5), (5,6)),
        
        ('BACKGROUND', (0,1), (0,2), HexColor('#f7fafc')),
        ('BACKGROUND', (5,1), (5,2), HexColor('#f7fafc')),
        ('BACKGROUND', (0,5), (0,6), HexColor('#f7fafc')),
        ('BACKGROUND', (5,5), (5,6), HexColor('#f7fafc')),
        
        ('LINEBELOW', (0,0), (-1,0), 1.5, HexColor('#2c7a7b')),
        ('LINEBELOW', (0,-1), (-1,-1), 1, HexColor('#cbd5e0')),
        ('LINEBELOW', (0,2), (-1,2), 0.5, HexColor('#e2e8f0')),
        ('LINEBELOW', (0,4), (-1,4), 0.5, HexColor('#e2e8f0')),
        ('BOX', (0,0), (-1,-1), 0.5, HexColor('#e2e8f0')),
    ]))
    story.append(seg_table)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: PREDICTIVE MODELING, RECOMMENDATIONS & CONCLUSION
    # =========================================================================
    story.append(make_heading("9. Predictive Modeling (Bonus)", heading1_style))
    predictive_intro = (
        "To test if trade profitability could be forecasted, a <b>Random Forest Classifier</b> was trained to "
        "predict profitable vs. non-profitable executions. Using trade size, fees paid, and the matching sentiment "
        "index value as features, the model achieved the following performance metrics:<br/>"
        "&bull; <b>Model Accuracy:</b> 73.62% | <b>Precision (Profitable):</b> 69.0% | <b>Recall (Profitable):</b> 66.0% | "
        "<b>F1 Score:</b> 67.0%<br/>"
        "The model's feature importance analysis reveals that transactional execution metrics (Fees: 43.0% and Size: 42.0%) "
        "dominate prediction paths, indicating execution efficiency is key. However, daily sentiment values account for "
        "15.0% of feature importance, validating that market psychology is an independent and measurable factor in trading outcomes."
    )
    story.append(Paragraph(predictive_intro, body_style))
    story.append(Spacer(1, 6))

    # Add Chart 3: Feature Importance (loaded from charts/ subfolder)
    chart3_path = os.path.join('charts', 'feature_importance.png')
    if os.path.exists(chart3_path):
        img3 = Image(chart3_path, width=280, height=140)
        img3.hAlign = 'CENTER'
        story.append(img3)
    story.append(Spacer(1, 8))

    story.append(make_heading("10. Actionable Recommendations", heading1_style))
    rec1 = (
        "<b>1. Position Size Reduction in Extreme Fear:</b> During periods of Extreme Fear, average trade win rates "
        "contract to 37.06%, and average profitability drops. Traders should systematically reduce their standard position sizes "
        "by 20–30% and tighten stop-losses, focusing capital strictly on high-conviction setups to avoid catching falling knives."
    )
    rec2 = (
        "<b>2. Capital Allocation Expansion in Extreme Greed:</b> In contrast to the common behavior of scaling down size "
        "during high market indexes, historical performance shows that Extreme Greed periods generate the highest win rates "
        "(46.49%) and average profitability ($67.89). Traders should maintain standard capital limits while expanding active "
        "participation to capitalize on strong momentum trends."
    )
    story.append(Paragraph(rec1, bullet_style))
    story.append(Paragraph(rec2, bullet_style))
    story.append(Spacer(1, 8))

    story.append(make_heading("11. Conclusion", heading1_style))
    conclusion_text = (
        "This research establishes a quantitative relationship between market-wide Bitcoin sentiment and trader behavior on Hyperliquid. "
        "The findings confirm that traders suffer from systemic cognitive errors, such as over-sizing positions during periods of "
        "fear and under-allocating capital during high-win-rate greed cycles. By implementing sentiment-adaptive position sizing and "
        "risk models, traders can control emotional biases, optimize fees, and improve risk-adjusted returns. For a hiring manager "
        "evaluating data science capabilities, this project demonstrates structured end-to-end data pipeline construction, statistical "
        "insight, predictive machine learning, and translated commercial value."
    )
    story.append(Paragraph(conclusion_text, body_style))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print("Report PDF successfully generated.")


if __name__ == "__main__":
    build_pdf()
