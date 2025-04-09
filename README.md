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