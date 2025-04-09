class ResultPrinter:
    @staticmethod
    def print_analysis_results(results: dict):
        """Print the analysis results in a human-readable format."""
        if results['status'] == 'no_new_attributes':
            print("✅ No new attributes found.")
            return
        
        added_cols = results.get('added_columns', [])
        if not added_cols:
            print("No new attributes to analyze.")
            return
        
        print(f"🆕 New attributes detected: {', '.join(added_cols)}\n")
        
        for new_col, data in results['results'].items():
            print(f"🔍 Analyzing new attribute: `{new_col}`")
            
            if 'warning' in data:
                if data['warning'] == "No values found":
                    print("⚠️ No values found for this attribute. Skipping.\n")
                elif data['warning'] == "No good matches found":
                    print("❌ No good matches found for this attribute.\n")
                continue
            
            if not data['matches']:
                print("❌ No good matches found for this attribute.\n")
                continue
            
            print("\nTop Candidate Matches:")
            for match in data['matches'][:5]:
                print(f" → {match['table']}.{match['column']} | Jaccard: {match['jaccard_sim']:.4f} | Join: {match['join_type'][0]}")

            best = data['matches'][0]
            print(f"\n✅ Best match for `{new_col}`: {best['table']}.{best['column']} → obtained through {best['join_type'][0]} join on original_table.{best['join_attributes'][0][0]} = {best['table']}.{best['join_attributes'][0][1]} (Jaccard sim: {best['jaccard_sim']:.4f})\n")


