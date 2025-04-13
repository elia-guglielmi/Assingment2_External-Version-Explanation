# Extended IMDB Movie Dataset

## Overview
This dataset extends the IMDB Top 1000 Movies and TV Shows dataset with synthetic data to create a comprehensive movie database with multiple related tables. It includes financial information, director details, actor information, awards data, streaming availability, user ratings, and country-specific release data.

## Dataset Structure

### Base Tables
- **IMDB_Base.csv**: Original dataset containing 800 movies with:
  - Title, year, genre, IMDB rating, etc.

### Synthetic Tables
1. **movie_financials.csv** - Financial metrics
2. **directors.csv** - Director information
3. **actors.csv** - Actor profiles (200 records)
4. **movie_actor_bridge.csv** - Actor-movie relationships (500 records)
5. **awards.csv** - Award nominations (150 records)
6. **streaming.csv** - Platform availability
7. **user_ratings.csv** - User reviews (1000 records)
8. **country_data.csv** - Country-specific releases (300 records)

## Generated Versions
The system creates 43 dataset versions through:

### Join Types
- Left joins (`_l` suffix)
- Inner joins (`_i` suffix)
- Right joins (`_r` suffix)

### Missing Data Variants
- 5% missing values (`_missing_5pct`)
- 15% missing values (`_missing_15pct`)

### Composite Versions
- Financials + Directors combinations
- Comprehensive version with financials, streaming, and ratings

## Generation Process
1. Loads base IMDB dataset
2. Creates synthetic tables using Faker library
3. Performs table joins with different join types
4. Introduces controlled missing data
5. Tracks all versions in `ground_truth_versions.csv`

## Technical Details
- **Language**: Python
- **Libraries**: Pandas, NumPy, Faker
- **Reproducibility**: Random seed = 42
- **Base Records**: 800 movies
- **Total Versions**: 43

## Usage
```python
import pandas as pd

# Load any version
df = pd.read_csv('imdb_with_financials_l.csv')

# Check ground truth
ground_truth = pd.read_csv('ground_truth_versions.csv')