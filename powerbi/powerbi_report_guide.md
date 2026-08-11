# Power BI Implementation Guide: Nassau Candy Profitability & Supply Chain Analytics

**Project Directory**: `C:\Users\ayush\.gemini\antigravity-ide\scratch\nassau_candy_analytics\powerbi`  
**Excel Data Model Source**: [`Nassau_Candy_PowerBI_Model.xlsx`](file:///C:/Users/ayush/.gemini/antigravity-ide/scratch/nassau_candy_analytics/powerbi/Nassau_Candy_PowerBI_Model.xlsx)  
**DAX Measures Library**: [`dax_measures.dax`](file:///C:/Users/ayush/.gemini/antigravity-ide/scratch/nassau_candy_analytics/powerbi/dax_measures.dax)  
**Power Query M Script**: [`power_query_transformations.m`](file:///C:/Users/ayush/.gemini/antigravity-ide/scratch/nassau_candy_analytics/powerbi/power_query_transformations.m)  

---

## 1. Quick Start: 3-Step Import into Power BI Desktop

### Step 1: Import Excel Data Model
1. Open **Power BI Desktop** (installed at `C:\Program Files\Microsoft Power BI Desktop\bin\PBIDesktop.exe`).
2. Click **Get Data** $\rightarrow$ **Excel workbook**.
3. Browse and select: `C:\Users\ayush\.gemini\antigravity-ide\scratch\nassau_candy_analytics\powerbi\Nassau_Candy_PowerBI_Model.xlsx`
4. In the Navigator window, select all 4 sheets:
   - `Fact_Orders`
   - `Dim_Products`
   - `Dim_Factories`
   - `Dim_Geography`
5. Click **Load** (or *Transform Data* to review Power Query steps).

### Step 2: Establish Data Model Relationships (Star Schema)
In the **Model View** tab of Power BI Desktop, verify the following relationships:
- `Fact_Orders[Product Name]` $\rightarrow$ `Dim_Products[Product Name]` (Many-to-One `*:1`, Single Direction)
- `Fact_Orders[Factory]` $\rightarrow$ `Dim_Factories[Factory]` (Many-to-One `*:1`, Single Direction)
- `Fact_Orders[State/Province]` $\rightarrow$ `Dim_Geography[State/Province]` (Many-to-One `*:1`, Single Direction)

---

## 2. Add DAX Measures

1. Create a blank Table named `_Measures` in Power BI (*Home $\rightarrow$ Enter Data $\rightarrow$ Name: `_Measures`*).
2. Click **New Measure** and paste measures from [`dax_measures.dax`](file:///C:/Users/ayush/.gemini/antigravity-ide/scratch/nassau_candy_analytics/powerbi/dax_measures.dax):
   - `Total Sales = SUM(Fact_Orders[Sales])`
   - `Total Gross Profit = SUM(Fact_Orders[Gross Profit])`
   - `Gross Margin % = DIVIDE([Total Gross Profit], [Total Sales], 0)`
   - `Profit per Unit = DIVIDE([Total Gross Profit], [Total Units], 0)`
   - `Revenue Share % = DIVIDE([Total Sales], CALCULATE([Total Sales], ALL(Dim_Products)), 0)`
   - `Profit Share % = DIVIDE([Total Gross Profit], CALCULATE([Total Gross Profit], ALL(Dim_Products)), 0)`
   - `Financial Imbalance Index = [Profit Share %] - [Revenue Share %]`
   - `Cumulative Profit %` & `Pareto Profit Category`
   - `Diagnostic Flag DAX` & `Strategic Quadrant DAX`

---

## 3. Report Pages & Visual Specifications

### Page 1: Executive Overview & Supply Chain Map
- **Top KPI Cards**: Total Revenue (`$141.8K`), Gross Profit (`$93.4K`), Gross Margin % (`65.9%`), Total Units Delivered (`42.1K`), Profit/Unit (`$2.22`).
- **Map Visual (Filled Map / Map)**:
  - Location: `Dim_Geography[State/Province]`
  - Size: `[Total Sales]`
  - Tooltips: `[Total Gross Profit]`, `[Gross Margin %]`, `Fact_Orders[Factory]`.
- **Clustered Column Chart**: `Division` on X-Axis, `[Total Sales]` and `[Total Gross Profit]` on Y-Axis.

### Page 2: Product Profitability & 4-Quadrant Matrix
- **Scatter Chart (Quadrant Matrix)**:
  - X-Axis: `[Total Sales]`
  - Y-Axis: `[Gross Margin %]`
  - Bubble Size: `[Total Units]`
  - Legend: `Dim_Products[Quadrant]`
- **Bar Chart (Top Profits)**: `Dim_Products[Product Name]` on Y-Axis, `[Total Gross Profit]` on X-Axis (Filtered to Top 7).
- **Matrix Table**: `Product Name`, `Division`, `Factory`, `[Total Sales]`, `[Total Gross Profit]`, `[Gross Margin %]`, `[Profit per Unit]`, `Dim_Products[Diagnostic Flag]`.

### Page 3: Division Performance & Imbalance Analysis
- **Bar Chart (Imbalance)**: `Division` on X-Axis, `[Financial Imbalance Index]` on Y-Axis.
- **Box Plot / Violin Visual**: Distribution of `Gross Margin %` by `Division`.

### Page 4: Cost Diagnostics & Interactive Repricing What-If Simulator
- **Scatter Plot**: Manufacturing `[Cost per Unit]` vs `[Gross Margin %]` colored by `[Diagnostic Flag DAX]`.
- **What-If Parameter Slicer**: Create Parameter `Price Increase %` (Range 0% to 50%, increment 1%).
- **Scenario Cards**: `[Simulated Price per Unit]`, `[Simulated Gross Margin %]`, `[Incremental Profit Gain]`.

### Page 5: Pareto (80/20) Concentration
- **Line & Stacked Column Chart**:
  - X-Axis: `Dim_Products[Product Name]` (Sorted by Gross Profit descending)
  - Column Values: `[Total Gross Profit]`
  - Line Values: `[Cumulative Profit %]`
  - Constant Reference Line at 80% on Y-Axis.

### Page 6: Factory Operations & Freight Efficiency
- **Bar Chart**: `Dim_Factories[Factory]` on X-Axis, `[Total Sales]` and `[Total Gross Profit]` on Y-Axis.
- **Donut Chart**: `Fact_Orders[Ship Mode]` by `[Total Sales]`.
- **Decomposition Tree**: Analyze `[Avg Transit Days]` broken down by `Ship Mode` $\rightarrow$ `Region` $\rightarrow$ `Factory`.
