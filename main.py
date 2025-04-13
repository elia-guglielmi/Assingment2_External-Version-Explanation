from analyzer.external_attribute_analyzer import ExternalAttributeAnalyzer
from analyzer.result_printer import ResultPrinter
from config import CONFIGURATIONS
import os

def main():
    # Initialize analyzer and printer
    analyzer = ExternalAttributeAnalyzer(num_perm=128)
    printer = ResultPrinter()
    
    # Process each configuration
    for config in CONFIGURATIONS:
        print(f"\n{'='*50}")
        print(f"Analyzing: {config['new_file']}")
        print(f"{'='*50}\n")
        
        # Perform analysis
        results = analyzer.analyze_new_attributes(
            base_file=config['base_file'],
            new_file=config['new_file'],
            candidate_dir=config['candidate_dir'],
            new_attributes=config['new_attribute']
        )
        
        # Print results
        printer.print_analysis_results(results)

if __name__ == "__main__":
    main()