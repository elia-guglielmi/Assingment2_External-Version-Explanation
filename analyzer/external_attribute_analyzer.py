import os
import pandas as pd
from datasketch import MinHash, MinHashLSHEnsemble
from typing import List, Tuple, Dict, Optional
import numpy as np

class ExternalAttributeAnalyzer:
    def __init__(self, num_perm: int = 128):
        self.NUM_PERM = num_perm
    
    def create_minhash(self, values: List[str], num_perm: int = None) -> MinHash:
        """Create a MinHash object from a list of values."""
        if num_perm is None:
            num_perm = self.NUM_PERM
        m = MinHash(num_perm=num_perm)
        for v in values:
            if pd.notna(v):
                m.update(str(v).strip().lower().encode('utf8'))
        return m
    
    def extract_column_dataframes(self, directory: str) -> List[Tuple[str, str, List[str], int, int]]:
        """Extract column information from all CSV files in a directory."""
        results = []
        for filename in os.listdir(directory):
            if filename.endswith(".csv"):
                table_name = filename[:-4]
                df = pd.read_csv(os.path.join(directory, filename))
                for col in df.columns:
                    values = df[col].astype(str).dropna().unique().tolist()
                    results.append((table_name, col, values, len(values), len(df)))
        return results
    
    def get_table(self, candidate_dir: str, name: str) -> pd.DataFrame:
        """Load a table from the candidate directory."""
        name = name + ".csv"
        return pd.read_csv(os.path.join(candidate_dir, name))
    
    def get_most_probable_join_type(self,orig_rows, ext_rows, joined_rows):
        """
        Returns the most probable join type with its relative probability (0-1)
        based solely on row counts, using statistical likelihoods.
    
        Args:
            orig_rows: Rows in left table
            ext_rows: Rows in right table
            joined_rows: Rows in joined result
        
        Returns:
            tuple: (most_probable_join_type, probability)
        """
        # Calculate boundary conditions
        min_rows = min(orig_rows, ext_rows)
        max_rows = max(orig_rows, ext_rows)
        sum_rows = orig_rows + ext_rows
        cross_rows = orig_rows * ext_rows
    
        # Initialize likelihoods (not normalized)
        likelihoods = {
            'inner': 0.0,
            'left': 0.0,
            'right': 0.0,
            'full': 0.0,
            'cross': 1e-9  # negligible base value
        }
        
        # 1. Inner join likelihood (normal distribution around expected matches)
        if min_rows > 0:
            expected_inner = min_rows * 0.5  # Prior assumption: 50% of keys match
            std_inner = min_rows * 0.3       # Reasonable standard deviation
            likelihoods['inner'] = np.exp(-((joined_rows - expected_inner)**2)/(2*std_inner**2))
        
        # 2. Left join likelihood (exponential decay from perfect match)
        likelihoods['left'] = np.exp(-0.5 * abs(joined_rows - orig_rows)/orig_rows) if orig_rows > 0 else 0
        
        # 3. Right join likelihood (exponential decay from perfect match)
        likelihoods['right'] = np.exp(-0.5 * abs(joined_rows - ext_rows)/ext_rows) if ext_rows > 0 else 0
        
        # 4. Full outer join likelihood (triangular distribution)
        if max_rows < sum_rows:
            if joined_rows <= max_rows:
                likelihoods['full'] = joined_rows / sum_rows
            else:
                likelihoods['full'] = (sum_rows - joined_rows) / sum_rows
        
        # 5. Cross join (only possible if exact product)
        if joined_rows == cross_rows:
            likelihoods['cross'] = 1.0
        
        # Normalize to probabilities
        total_likelihood = sum(likelihoods.values())
        probabilities = {k: v/total_likelihood for k, v in likelihoods.items()}
        
        # Return the most probable
        most_probable = max(probabilities.items(), key=lambda x: x[1])
        return most_probable
    

    
    def __overlap(self,column1:pd.DataFrame,column2:pd.DataFrame,sample_size: int = 1000) -> int:
        sample1 = self._get_sample(column1.dropna(), sample_size)
        sample2 = self._get_sample(column2.dropna(), sample_size)
                    
        # Skip if either sample is empty
        if len(sample1) == 0 or len(sample2) == 0:
            return 0
                    
        # Check for overlapping values
        common_values = set(sample1) & set(sample2)
        if len(common_values) > 0:
            overlap_ratio = len(common_values) / min(len(sample1.unique()), len(sample2.unique()))
        else:
            return 0
        return overlap_ratio

    
    def find_joinable_attributes(self, df1: pd.DataFrame, df2: pd.DataFrame, 
                               sample_size: int = 1000, min_overlap: float = 0.1) -> List[Tuple[str, str, float]]:
        """Find potential joinable attributes between two DataFrames."""
        potential_matches = []
        
        # Step 1: Find columns with matching names and compatible dtypes
        common_cols = set(df1.columns) & set(df2.columns)
        for col in common_cols:
            if pd.api.types.is_dtype_equal(df1[col].dtype, df2[col].dtype):
                overlap_ratio=self.__overlap(df1[col],df2[col],sample_size)
                if overlap_ratio >= min_overlap:
                    potential_matches.append((col, col, overlap_ratio))
                #potential_matches.append((col, col, 0))
        
        # Step 2: Find columns with compatible dtypes (even if names don't match)
        for col1 in df1.columns:
            for col2 in df2.columns:
                # Skip if already found or same column pair
                if (col1, col2) in [(x[0], x[1]) for x in potential_matches] or col1 == col2:
                    continue
                
                # Check dtype compatibility
                if pd.api.types.is_dtype_equal(df1[col1].dtype, df2[col2].dtype):
                    # Get samples (handle empty DataFrames)
                    overlap_ratio=self.__overlap(df1[col1],df2[col2],sample_size)
                    if overlap_ratio >= min_overlap:
                        potential_matches.append((col1, col2, overlap_ratio))
            potential_matches.sort(key=lambda x: x[2], reverse=True)
        
        return potential_matches
    
    def _get_sample(self, series: pd.Series, sample_size: int) -> pd.Series:
        """Helper function to get sample from a series."""
        if sample_size <= 0 or len(series) <= sample_size:
            return series
        return series.sample(sample_size)
    
    def analyze_new_attributes(self, base_file: str, new_file: str, candidate_dir: str, new_attributes=[]) -> Dict[str, Dict]:
        """
        Analyze new attributes between base and new files, searching for matches in candidate tables.
        
        Returns:
            Dictionary with analysis results for each new attribute
        """
        # Load datasets
        base_df = pd.read_csv(base_file)
        new_df = pd.read_csv(new_file)
        base_name = os.path.basename(base_file)
        base_name = os.path.splitext(base_name)[0]# Split the filename and extension
        new_name = os.path.basename(new_file)
        new_name = os.path.splitext(new_name)[0]# Split the filename and extension


        # Detect newly added attributes to analyze. 
        # If no attribute has been passed it detects all attribute that are present in the new version but not in the original table
        if new_attributes:
            added_cols=set(new_attributes)
        else:
            base_cols = set(base_df.columns)
            new_cols = set(new_df.columns)
            added_cols = new_cols - base_cols
        
        if not added_cols:
            return {'status': 'no_new_attributes', 'results': {},'new_table':new_name,'original_table':base_name}
        
        # Index external candidate columns with MinHash + LSH Ensemble
        column_entries = self.extract_column_dataframes(candidate_dir)
        minhashes = []
        index_metadata = []
        
        for table_name, col_name, values, size, size_with_na in column_entries:
            mh = self.create_minhash(values)
            minhashes.append(mh)
            index_metadata.append({
                'table': table_name,
                'column': col_name,
                'full_name': f"{table_name}.{col_name}",
                'size': size,
                'keys': [col_name],
                'size_with_na': size_with_na
            })
        
        lsh = MinHashLSHEnsemble(threshold=0.1, num_perm=self.NUM_PERM)
        keys = [m['full_name'] for m in index_metadata]
        sizes = [m['size'] for m in index_metadata]
        combined = list(zip(keys, minhashes, sizes))
        lsh.index(combined)
        
        results = {}
        
        # For each new attribute: search + recommend join
        for new_col in added_cols:
            results[new_col] = {'matches': []}

            new_values = new_df[new_col].astype(str).dropna().unique().tolist()
            if not new_values:
                results[new_col]['warning'] = "No values found"
                continue

            new_attr_minhash = self.create_minhash(new_values)
            candidates = list(lsh.query(new_attr_minhash, len(new_values)))
            
            # Rank candidate tables based on jaccard similarity
            ranked = []
            for meta, mh in zip(index_metadata, minhashes):
                if meta['full_name'] in candidates:
                    sim = new_attr_minhash.jaccard(mh)
                    join_type = self.get_most_probable_join_type(len(base_df), len(new_df), meta['size_with_na'])
                    join_attribute = self.find_joinable_attributes(base_df, self.get_table(candidate_dir, meta['table']))
                    
                    if join_attribute:
                        ranked.append({
                            'table': meta['table'],
                            'column': meta['column'],
                            'jaccard_sim': sim,
                            'join_type': join_type,
                            'join_attributes': join_attribute,
                        })

            ranked.sort(key=lambda x: x['jaccard_sim'], reverse=True)
            results[new_col]['matches'] = ranked
            
            if not ranked:
                results[new_col]['warning'] = "No good matches found"
        
        return {'status': 'success', 'results': results, 'added_columns': list(added_cols),'new_table':new_name,'original_table':base_name}
