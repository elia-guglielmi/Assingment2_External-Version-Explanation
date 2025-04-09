# Example configuration - modify as needed
CONFIGURATIONS = [
    {
        "base_file": "D:/uni/AdvancedTopics/project2/sinteticDB/IMDB/IMDB_Base.csv",
        "new_file": "D:/uni/AdvancedTopics/project2/sinteticDB/IMDB/Versions/imdb_with_financials_l.csv",
        "candidate_dir": "D:/uni/AdvancedTopics/project2/sinteticDB/IMDB/externalTables"
    },
    # Add more configurations as needed
]

# Or to analyze all files in a directory:
"""
import os

BASE_DIR = "sinteticDB/IMDB"
CONFIGURATIONS = [
    {
        "base_file": os.path.join(BASE_DIR, "IMDB_Base.csv"),
        "new_file": os.path.join(BASE_DIR, "Versions", filename),
        "candidate_dir": os.path.join(BASE_DIR, "externalTables")
    }
    for filename in os.listdir(os.path.join(BASE_DIR, "Versions"))
    if filename.endswith(".csv")
]
"""