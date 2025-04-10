# External Attribute Analyzer

This tool analyzes new attributes in updated versions of datasets and identifies potential external tables that could be joined to provide those attributes.

## Installation

1. Clone this repository
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt

## Configuration
Edit the config.py file to specify:

1. The base file (original dataset)

2. New files (updated versions)
 
3. Directory containing candidate tables for joining

4. attribute names to analyze (optional)

## Usage

Run the analysis:

```bash
python main.py
```
output:
 
```bash
==================================================
Analyzing: d:\uni\AdvancedTopics\project2\sinteticDB\IMDB\Versions\imdb_with_financials_l.csv
==================================================

🆕 New attributes detected: Box_Office_Gross, Profitability_Ratio, Production_Budget, Release_Season, Primary_Production_Company

🔍 Analyzing new attribute: `Box_Office_Gross`

Top Candidate Matches:
 → financials.Box_Office_Gross | Jaccard: 1.0000 | Join: left

✅ Best match for `Box_Office_Gross`: financials.Box_Office_Gross → obtained through left join on original_table.Series_Title = financials.Series_Title (Jaccard sim: 1.0000)

🔍 Analyzing new attribute: `Profitability_Ratio`

Top Candidate Matches:
 → financials.Profitability_Ratio | Jaccard: 1.0000 | Join: left

✅ Best match for `Profitability_Ratio`: financials.Profitability_Ratio → obtained through left join on original_table.Series_Title = financials.Series_Title (Jaccard sim: 1.0000)

🔍 Analyzing new attribute: `Production_Budget`

Top Candidate Matches:
 → financials.Production_Budget | Jaccard: 1.0000 | Join: left

✅ Best match for `Production_Budget`: financials.Production_Budget → obtained through left join on original_table.Series_Title = financials.Series_Title (Jaccard sim: 1.0000)

🔍 Analyzing new attribute: `Release_Season`

Top Candidate Matches:
 → financials.Release_Season | Jaccard: 1.0000 | Join: left

✅ Best match for `Release_Season`: financials.Release_Season → obtained through left join on original_table.Series_Title = financials.Series_Title (Jaccard sim: 1.0000)

🔍 Analyzing new attribute: `Primary_Production_Company`

Top Candidate Matches:
 → financials.Primary_Production_Company | Jaccard: 1.0000 | Join: left

✅ Best match for `Primary_Production_Company`: financials.Primary_Production_Company → obtained through left join on original_table.Series_Title = financials.Series_Title (Jaccard sim: 1.0000)
```
